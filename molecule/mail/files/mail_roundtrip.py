#!/usr/bin/env python3
"""SMTP submission plus IMAP fetch roundtrip for a virtual mailbox.

Delivers a message through the submission port and reads it back over IMAP.
This exercises the parts no single-role scenario covers: SASL against the
dovecot auth socket, the rspamd milter, and LMTP delivery into the maildir.
"""

from __future__ import annotations

import imaplib
import os
import smtplib
import ssl
import sys
import time
import uuid
from email.message import EmailMessage


def env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        if default is not None:
            return default
        raise SystemExit(f"missing environment variable {name}")
    return value


def insecure_context() -> ssl.SSLContext:
    """The test runs against a snakeoil certificate on 127.0.0.1."""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context


def submit(host: str, port: int, user: str, password: str, subject: str, timeout: int) -> None:
    message = EmailMessage()
    message["From"] = user
    message["To"] = user
    message["Subject"] = subject
    message.set_content("Molecule roundtrip verification message.\n")

    with smtplib.SMTP(host, port, timeout=timeout) as smtp:
        smtp.ehlo()
        smtp.starttls(context=insecure_context())
        smtp.ehlo()
        smtp.login(user, password)
        smtp.send_message(message)


def fetch(host: str, port: int, user: str, password: str, subject: str, timeout: int) -> str:
    """Poll the mailbox until the message shows up or the deadline passes."""
    deadline = time.time() + timeout
    last_error = "no matching message"

    while time.time() < deadline:
        try:
            with imaplib.IMAP4(host, port, timeout=timeout) as imap:
                imap.starttls(ssl_context=insecure_context())
                imap.login(user, password)
                for mailbox in ("INBOX", "Junk"):
                    status, _ = imap.select(mailbox)
                    if status != "OK":
                        continue
                    status, data = imap.search(None, "HEADER", "Subject", subject)
                    if status == "OK" and data and data[0].split():
                        return mailbox
        except (imaplib.IMAP4.error, OSError) as exc:
            last_error = str(exc)
        time.sleep(2)

    raise SystemExit(f"message '{subject}' never arrived: {last_error}")


def main() -> None:
    host = env("MAIL_HOST", "127.0.0.1")
    user = env("MAIL_USER")
    password = env("MAIL_PASSWORD")
    smtp_port = int(env("MAIL_SMTP_PORT", "587"))
    imap_port = int(env("MAIL_IMAP_PORT", "143"))
    timeout = int(env("MAIL_TIMEOUT", "60"))

    subject = f"molecule-roundtrip-{uuid.uuid4().hex}"

    submit(host, smtp_port, user, password, subject, timeout)
    mailbox = fetch(host, imap_port, user, password, subject, timeout)

    print(f"delivered to {mailbox}")
    sys.exit(0)


if __name__ == "__main__":
    main()
