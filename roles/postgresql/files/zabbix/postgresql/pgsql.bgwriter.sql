-- Keep the existing monitoring JSON keys across PostgreSQL versions.
DO LANGUAGE plpgsql $$
DECLARE
    res text;
BEGIN
    IF current_setting('server_version_num')::integer >= 170000 THEN
        SELECT row_to_json(t)::text INTO res
        FROM (
            SELECT c.num_timed AS checkpoints_timed,
                c.num_requested AS checkpoints_req,
                c.write_time AS checkpoint_write_time,
                c.sync_time AS checkpoint_sync_time,
                current_setting('block_size')::bigint * c.buffers_written AS buffers_checkpoint,
                current_setting('block_size')::bigint * b.buffers_clean AS buffers_clean,
                b.maxwritten_clean,
                io.buffers_backend,
                io.buffers_backend_fsync,
                current_setting('block_size')::bigint * b.buffers_alloc AS buffers_alloc
            FROM pg_stat_bgwriter b
            CROSS JOIN pg_stat_checkpointer c
            CROSS JOIN (
                -- PostgreSQL 18 reports bytes directly; 17 reports writes * op_bytes.
                -- JSON field access avoids referring to columns absent in either version.
                SELECT coalesce(sum(coalesce(
                    (to_jsonb(i) ->> 'write_bytes')::numeric,
                    i.writes * (to_jsonb(i) ->> 'op_bytes')::numeric
                )), 0) AS buffers_backend,
                    coalesce(sum(i.fsyncs), 0) AS buffers_backend_fsync
                FROM pg_stat_io i
                WHERE i.backend_type = 'client backend' AND i.object = 'relation'
            ) io
        ) t;
    ELSE
        SELECT row_to_json(t)::text INTO res
        FROM (
            SELECT checkpoints_timed,
                checkpoints_req,
                checkpoint_write_time,
                checkpoint_sync_time,
                current_setting('block_size')::bigint * buffers_checkpoint AS buffers_checkpoint,
                current_setting('block_size')::bigint * buffers_clean AS buffers_clean,
                maxwritten_clean,
                current_setting('block_size')::bigint * buffers_backend AS buffers_backend,
                buffers_backend_fsync,
                current_setting('block_size')::bigint * buffers_alloc AS buffers_alloc
            FROM pg_stat_bgwriter
        ) t;
    END IF;
    PERFORM set_config('zbx_tmp.bgwriter_json_res', res, false);
END $$;

SELECT current_setting('zbx_tmp.bgwriter_json_res');
