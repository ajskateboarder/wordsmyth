from __future__ import annotations


class CAPTCHAError(Exception):
    """Detected by Amazon and requires a CAPTCHA to proceed"""

    def __init__(self, browser_id: str | None) -> None:
        self.browser_id = browser_id


class AccountProtectionError(CAPTCHAError):
    """Detected by Amazon upon logging in and requires a CAPTCHA to proceed"""
