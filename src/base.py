import os
import time
from typing import Generator, Optional, Tuple

import requests
from bs4 import BeautifulSoup  # type: ignore
from requests import Response  # type: ignore
from twilio.rest import Client  # type: ignore


class BaseWebsiteMonitor(object):
    _headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/39.0.2171.95 Safari/537.36"
        )
    }

    _no_alert_flag = 0
    _alert_flag = 1
    _error_flag = -1

    def __init__(self, url: str, verbose: bool) -> None:
        self.url = url
        self.verbose = verbose

    @property
    def current_time(self) -> int:
        return self._current_time

    @property
    def start_time(self) -> int:
        return self._start_time

    @property
    def max_seconds(self) -> int:
        return self._max_seconds

    @property
    def max_hours(self) -> float:
        return self._max_seconds / 60.0

    @property
    def running_seconds(self) -> int:
        return self.current_time - self.start_time

    @property
    def running_hours(self) -> float:
        return self.running_seconds / 60.0

    @property
    def running_message(self) -> str:
        if self.max_hours > 1.0:
            message = (
                f"Monitor has been running for {self.running_hours:.2f} / {self.max_hours:.2f} hours. "
                f"Running website check number {self.n_checks}."
            )
        else:
            message = (
                f"Monitor has been running for {self.running_seconds:.0f} / {self.max_seconds:.0f} seconds. "
                f"Running website check number {self.n_checks}."
            )
        return message

    def _reload(self) -> BeautifulSoup:
        response = requests.get(self.url, headers=self._headers)
        return BeautifulSoup(response.text, "lxml")

    def _alert_condition(self, soup: BeautifulSoup) -> bool:
        """
        This needs to be implemented in the subclass.
        You need to use passed soup object and return true if you want to send a notification, and false otherwise.
        For example, if you are monitoring a website for stock, you need to return true when they have stock,
        and false when they do not.
        """
        raise NotImplementedError()

    def _check_alert_condition(self, soup: BeautifulSoup) -> int:
        try:
            is_alert = self._alert_condition(soup)
            is_error = False
        except:
            is_error = True

        if is_error:
            return self._error_flag
        elif is_alert:
            return self._alert_flag
        else:
            return self._no_alert_flag

    def _initialize_monitoring_variables(self, max_seconds):
        self._start_time = time.time()
        self._current_time = time.time()
        self._max_seconds = max_seconds
        self.n_checks = 0

    def _step(self, pause_seconds: int) -> None:
        time.sleep(pause_seconds)

        self._current_time = time.time()
        self.n_checks += 1
        if self.verbose:
            print(self.running_message)

    def monitor(self, max_seconds: int, pause_seconds: int) -> Generator:
        self._initialize_monitoring_variables(max_seconds=max_seconds)

        while self.running_seconds < self.max_seconds:
            self._step(pause_seconds=pause_seconds)

            soup = self._reload()
            result = self._check_alert_condition(soup=soup)

            yield result


def send_sms(txt):
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    from_mobile = os.environ["TWILIO_FROM_MOBILE"]
    to_mobile = os.environ["TWILIO_TO_MOBILE"]

    client = Client(account_sid, auth_token)

    return client.messages.create(body=txt, from_=from_mobile, to=to_mobile)
