import os
import json
import time
import argparse
import requests

from requests.adapters import HTTPAdapter


session = requests.Session()
session.mount('https://', HTTPAdapter())
session.mount('http://', HTTPAdapter())


def generate_request_json_file(file_name):
    content_dict = {
        "method": "Request method valid options: GET, OPTIONS, HEAD, POST, PUT, PATCH, or DELETE.",
        "url": "URL for the Request.",
        "params": "(optional) Dictionary to send in the query string for the Request.",
        "json": "(optional) Dictionary to send in the body of the Request.",
        "headers": "(optional) Dictionary of HTTP Headers to send with the Request.",
        "cookies": "(optional) Dictionary to send with the Request.",
    }

    json.dump(content_dict, open(file_name, "w", encoding="utf8"), indent=4)

    print("Request file", file_name, "generated.\nCheck the file for more information.\n")


def run_request(request_file, response_file):
    with open(request_file, "r", encoding="utf8") as request_file_fp:
        with open(response_file, "w", encoding="utf8") as response_file_fp:
            try:
                requests_params = json.load(request_file_fp)

                response = session.request(
                    method=requests_params["method"].upper(),
                    url=requests_params["url"],
                    params=requests_params.get("params") or {},
                    json=requests_params.get("json") or {},
                    headers=requests_params.get("headers") or {},
                    cookies=requests_params.get("cookies") or {}
                )

                response_dict = {
                    "url": response.url,
                    "ok": response.ok,
                    "status_code": response.status_code,
                    "response_time_sec": response.elapsed.total_seconds(),
                    "response_data": {
                        "response": response.json(),
                        "headers": dict(response.headers),
                        "cookies": dict(response.cookies)
                    },
                    "request_data": {
                        "headers": dict(response.request.headers)
                    }
                }

                json.dump(response_dict, response_file_fp, indent=4)

                print("URL :", requests_params["url"], end=", ")
                print("Method :", requests_params["method"].upper(), end=", ")
                print("Status :", "OK" if response_dict["ok"] else "BAD", end=", ")
                print("Status Code :", response_dict["status_code"], end=", ")
                print("Response Time :", response_dict["response_time_sec"], "sec")
            except Exception as e:
                try:
                    json.dump({"error": str(e)}, response_file_fp, indent=4)
                except:
                    pass
                print(e.args)


def main(request_file, response_file):
    try:
        print("\nExpected Request JSON File :", request_file)
        print("Expected Response JSON File :", response_file)

        if input("Do you want live reload? [Y/n] ").strip().lower() != 'n':
            modification_time = os.stat(request_file).st_mtime

            print("\nWatching for changes in file", request_file, ".....")
            print("Press Ctrl+C to quit")

            try:
                while True:
                    time.sleep(1)
                    if modification_time != os.stat(request_file).st_mtime:
                        modification_time = os.stat(request_file).st_mtime
                        run_request(request_file, response_file)
            except KeyboardInterrupt:
                print("Keyboard Interrupted. Closing...")
        else:
            while True:
                if input("r[to send request] / q[quit] : ").strip().lower() == 'q':
                    break
                run_request(args.request, args.response)
    finally:
        session.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='REST Api Tester in Python')

    parser.add_argument(
        '--generate', action='store',
        type=str,
        help="Generate a sample request json file."
    )

    parser.add_argument(
        '--request', action='store',
        type=str,
        help="Specify request json file."
    )

    parser.add_argument(
        '--response', action='store',
        type=str,
        help="Specify response json file."
    )

    args = parser.parse_args()

    if args.generate != None:
        generate_request_json_file(args.generate)

    if args.request != None:
        request_file = args.request
    else:
        if args.generate != None:
            request_file = args.generate
        else:
            request_file = "request.json"

    if args.response != None:
        response_file = args.response
    else:
        response_file = "response.json"

    if not os.path.isfile(request_file):
        if input("Request JSON file does not exist. Do you want to generate it? [Y/n] ").lower().strip() == 'n':
            exit()

        generate_request_json_file(request_file)

    main(request_file , response_file)
