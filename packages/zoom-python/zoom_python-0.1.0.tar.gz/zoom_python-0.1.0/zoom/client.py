import base64
import json
from urllib.parse import urlencode

import requests

from zoom.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    URL = "https://api.zoom.us/v2/"
    AUTH_URL = "https://zoom.us/oauth/"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.REDIRECT_URI = redirect_uri

    def authorization_url(self, redirect_uri=None, state=None):
        if redirect_uri is not None:
            self.REDIRECT_URI = redirect_uri
        params = {"client_id": self.CLIENT_ID, "redirect_uri": self.REDIRECT_URI, "response_type": "code"}
        if state:
            params["state"] = state
        return self.AUTH_URL + "authorize?" + urlencode(params)

    def auth_headers(self):
        encoded_credentials = base64.b64encode(f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode("utf-8")).decode("utf-8")
        self.headers["Authorization"] = f"Basic {encoded_credentials}"
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"

    def get_access_token(self, code):
        body = {"code": code, "grant_type": "authorization_code", "redirect_uri": self.REDIRECT_URI}
        self.auth_headers()
        return self.post("token", auth_url=True, data=body)

    def refresh_access_token(self, refresh_token):
        body = {"refresh_token": refresh_token, "grant_type": "refresh_token"}
        self.auth_headers()
        return self.post("token", auth_url=True, data=body)

    def set_token(self, access_token):
        self.headers.update(Authorization=f"Bearer {access_token}")

    def get_current_user(self):
        return self.get("users/me")

    def list_users(self):
        return self.get("users")

    def list_meetings(self):
        return self.get("users/me/meetings")

    def get_meeting(self, meeting_id):
        return self.get(f"meetings/{meeting_id}")

    def create_meeting(
        self,
        topic: str,
        duration: int,
        start_time: str,
        type: int = 2,
        agenda: str = None,
        default_password: bool = False,
        password: str = None,
        pre_schedule: bool = False,
        schedule_for: str = None,
        timezone: str = None,
        recurrence: dict = None,
        settings: dict = None,
    ):
        args = locals()
        body = self.set_form_data(args)
        return self.post("users/me/meetings", data=json.dumps(body))

    def add_meeting_registrant(
        self,
        meeting_id,
        email: str,
        first_name: str,
        last_name: str = None,
        address: str = None,
        city: str = None,
        state: str = None,
        zip: str = None,
        country: str = None,
        phone: str = None,
        comments: str = None,
        industry: str = None,
        job_title: str = None,
        org: str = None,
        no_of_employees: str = None,
        purchasing_time_frame: str = None,
        role_in_purchase_process: str = None,
        language: str = None,
        auto_approve: bool = None,
    ):
        args = locals()
        print(type(args))
        print(args)
        body = self.set_form_data(args)
        return self.post(f"meetings/{meeting_id}/registrants", data=json.dumps(body))

    def add_webinar_registrant(
        self,
        webinar_id,
        email: str,
        first_name: str,
        last_name: str = None,
        address: str = None,
        city: str = None,
        state: str = None,
        zip: str = None,
        country: str = None,
        phone: str = None,
        comments: str = None,
        industry: str = None,
        job_title: str = None,
        org: str = None,
        no_of_employees: str = None,
        purchasing_time_frame: str = None,
        role_in_purchase_process: str = None,
        language: str = None,
        auto_approve: bool = None,
    ):
        args = locals()
        body = self.set_form_data(args)
        return self.post(f"webinars/{webinar_id}/registrants", data=json.dumps(body))

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def put(self, endpoint, **kwargs):
        response = self.request("PUT", endpoint, **kwargs)
        return self.parse(response)

    def patch(self, endpoint, **kwargs):
        response = self.request("PATCH", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, auth_url=False, **kwargs):
        return requests.request(
            method, self.AUTH_URL + endpoint if auth_url else self.URL + endpoint, headers=self.headers, **kwargs
        )

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r

    def set_form_data(self, args):
        data = {}
        for arg in args:
            if args[arg] is not None and arg != "self":
                data.update({f"{arg}": args[arg]})
        return data
