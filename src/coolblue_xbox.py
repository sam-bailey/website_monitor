import argparse
import os
import time

import requests
from bs4 import BeautifulSoup  # type: ignore
from twilio.rest import Client  # type: ignore

from base import BaseWebsiteMonitor, send_sms


class CoolBlueXboxMonitor(BaseWebsiteMonitor):
    def __init__(self, verbose: bool):
        super().__init__(
            url="https://www.coolblue.nl/product/867421/xbox-series-x.html",
            verbose=verbose,
        )

    def _alert_condition(self, soup: BeautifulSoup) -> bool:
        order_block = soup.main.find("div", class_="js-desktop-order-block")
        search_string = order_block.find(text="Beschikbaar vanaf 9 november")
        return search_string is None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor coolblue for the new xbox series x stock.")
    parser.add_argument("--send-sms", dest="send_sms", action="store_true")
    parser.add_argument("--no-sms", dest="send_sms", action="store_false")
    parser.set_defaults(send_sms=False)
    args = parser.parse_args()
    if args.send_sms:
        print("Will send an sms if stock is in.")
        print("Just sent a test sms, if you didn't get it, things are probably not working properly")
        send_sms("Monitoring for xbox series x on coolblue starting")
    else:
        print("Wont send an sms if stock is in. Need to monitor manually here.")

    cool_blue_xbox = CoolBlueXboxMonitor(verbose=True)

    for result in cool_blue_xbox.monitor(max_seconds=20, pause_seconds=5):
        if result == 0:
            continue
        elif result == 1:
            message = "Stock is in!! Go to https://www.coolblue.nl/product/867421/xbox-series-x.html"
            print(message)
            if args.send_sms:
                send_sms(message)
            break
        else:
            message = "Error in the monitor! Check it out..."
            print(message)
            if args.send_sms:
                send_sms(message)
            break
