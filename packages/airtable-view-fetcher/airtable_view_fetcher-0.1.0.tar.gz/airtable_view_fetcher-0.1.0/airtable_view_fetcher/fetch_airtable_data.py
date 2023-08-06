import re
import json
import sys
from datetime import datetime
import pytz
import requests


def fetch_airtable_data(url):
    # Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }

    # Create session
    session = requests.Session()

    # Get the view fetch URL and cookies
    response = session.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the HTML content
        html = response.text

        # Extract URL with params
        url_with_params_pattern = r'urlWithParams: "(.*?)"'
        url_with_params_match = re.search(url_with_params_pattern, html)
        url_with_params = url_with_params_match.group(1) if url_with_params_match else None

        # Decode Unicode characters
        decoded_url = bytes(url_with_params, "utf-8").decode("unicode_escape")

        # Extract the headers variable using regex
        match = re.search(r"var headers = ({.*?});", html, re.DOTALL)

        if match:
            headers_dict = match.group(1)
            headers_dict = {**json.loads(headers_dict),
                            'x-time-zone': datetime.now(pytz.timezone('UTC')).strftime('%Z')}
            final_resp = session.get(f"https://airtable.com{decoded_url}", headers=headers_dict)
            print(final_resp.text)
        else:
            print("Headers variable not found.")

    else:
        print("Failed to retrieve HTML from URL. Status code:", response.status_code)


def main():
    if len(sys.argv) < 2:
        print("Please provide the shared view URL as a command-line argument.")
    else:
        shared_view_url = sys.argv[1]
        fetch_airtable_data(shared_view_url)


if __name__ == '__main__':
    main()
