// matrix_room_cleaner.go

// Purpose: Redact old events (> MAX_AGE_DAYS) in a Matrix room on Dendrite/Synapse.
// Sources (spec):
//   - https://spec.matrix.org/v1.11/client-server-api/#get_matrixclientv3sync
//   - https://spec.matrix.org/v1.11/client-server-api/#get_matrixclientv3roomsroomidmessages
//   - https://spec.matrix.org/v1.11/client-server-api/#post_matrixclientv3roomsroomidredacteventidtxnid
package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"
	"io"
)

type SyncResp struct {
	NextBatch string `json:"next_batch"`
}

type Event struct {
	EventID          string `json:"event_id"`
	Type             string `json:"type"`
	OriginServerTS   int64  `json:"origin_server_ts"`
}

type MessagesResp struct {
	Chunk []Event `json:"chunk"`
	End   string  `json:"end"`
}

func getenv(k, def string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return def
}

func mustEnv(k string) string {
	v := os.Getenv(k)
	if v == "" {
		fmt.Fprintf(os.Stderr, "missing required env: %s\n", k)
		os.Exit(2)
	}
	return v
}

func authReq(method, rawURL, token string, body io.Reader) (*http.Request, error) {
	req, err := http.NewRequest(method, rawURL, body)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")
	return req, nil
}

func doJSON[T any](client *http.Client, req *http.Request, out *T) error {
	res, err := client.Do(req)
	if err != nil {
		return err
	}
	defer res.Body.Close()

	// Handle 429 rate limit
	if res.StatusCode == 429 {
		ra := res.Header.Get("Retry-After")
		if s, _ := strconv.Atoi(strings.TrimSpace(ra)); s > 0 {
			time.Sleep(time.Duration(s) * time.Second)
		} else {
			time.Sleep(2 * time.Second)
		}
		return errors.New("rate limited")
	}
	if res.StatusCode < 200 || res.StatusCode >= 300 {
		b, _ := io.ReadAll(res.Body)
		return fmt.Errorf("%s -> %d: %s", req.URL.String(), res.StatusCode, string(b))
	}
	if out == nil {
		_, _ = io.Copy(io.Discard, res.Body)
		return nil
	}
	dec := json.NewDecoder(res.Body)
	return dec.Decode(out)
}

func main() {
	base := strings.TrimRight(mustEnv("MATRIX_BASE"), "/")
	token := mustEnv("MATRIX_TOKEN")
	roomID := mustEnv("ROOM_ID")

	maxAgeDays, _ := strconv.Atoi(getenv("MAX_AGE_DAYS", "7"))
	limit, _ := strconv.Atoi(getenv("BATCH_LIMIT", "500"))              // messages page size
	maxRedactions, _ := strconv.Atoi(getenv("MAX_REDACTIONS", "10000")) // safety cap per run
	sleepMs, _ := strconv.Atoi(getenv("SLEEP_MS", "25"))                // tiny pause between redactions

	cutoff := time.Now().Add(-time.Duration(maxAgeDays) * 24 * time.Hour).UnixMilli()

	client := &http.Client{Timeout: 30 * time.Second}

	// 1) Get next_batch from /sync (timeout=0)
	syncURL := fmt.Sprintf("%s/_matrix/client/v3/sync?timeout=0", base)
	req, _ := authReq(http.MethodGet, syncURL, token, nil)

	var sresp SyncResp
	for {
		if err := doJSON(client, req, &sresp); err != nil {
			if strings.Contains(err.Error(), "rate limited") {
				continue
			}
			die(err)
		}
		break
	}
	nextBatch := sresp.NextBatch
	if nextBatch == "" {
		die(errors.New("empty next_batch from /sync"))
	}

	// 2) Backpaginate messages dir=b
	from := url.QueryEscape(nextBatch)
	roomEsc := url.PathEscape(roomID)
	redacted := 0

	for {
		msgURL := fmt.Sprintf("%s/_matrix/client/v3/rooms/%s/messages?dir=b&limit=%d&from=%s", base, roomEsc, limit, from)
		req, _ := authReq(http.MethodGet, msgURL, token, nil)

		var mresp MessagesResp
		if err := doJSON(client, req, &mresp); err != nil {
			if strings.Contains(err.Error(), "rate limited") {
				continue
			}
			die(err)
		}
		chunk := mresp.Chunk
		if len(chunk) == 0 {
			break
		}

		// redact candidates (< cutoff, non-state)
		for _, ev := range chunk {
			if ev.EventID == "" || strings.HasPrefix(ev.Type, "m.room.") {
				continue
			}
			if ev.OriginServerTS >= cutoff {
				continue
			}
			txnID := "redact-" + strings.TrimPrefix(ev.EventID, "$")
			redURL := fmt.Sprintf("%s/_matrix/client/v3/rooms/%s/redact/%s/%s",
				base, roomEsc, url.PathEscape(ev.EventID), url.PathEscape(txnID))
			body := strings.NewReader(`{"reason":"auto-retention"}`)
			rreq, _ := authReq(http.MethodPost, redURL, token, body)

			// retry on 429 inside doJSON
			for {
				if err := doJSON[map[string]any](client, rreq, nil); err != nil {
					if strings.Contains(err.Error(), "rate limited") {
						continue
					}
					// log and continue
					fmt.Fprintf(os.Stderr, "redact failed %s: %v\n", ev.EventID, err)
				}
				break
			}
			redacted++
			if sleepMs > 0 {
				time.Sleep(time.Duration(sleepMs) * time.Millisecond)
			}
			if redacted >= maxRedactions {
				fmt.Printf("Safety cap reached (MAX_REDACTIONS=%d)\n", maxRedactions)
				fmt.Printf("Redacted=%d\n", redacted)
				return
			}
		}

		if mresp.End == "" {
			break
		}
		from = url.QueryEscape(mresp.End)
	}

	fmt.Printf("Done. Redacted=%d (older than %d days)\n", redacted, maxAgeDays)
}

func die(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
