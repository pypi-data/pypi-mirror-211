
# zoom-python
![](https://img.shields.io/badge/version-0.1.0-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*zoom-python* is an API wrapper for Zoom, written in Python.  
This library uses Oauth2 for authentication.
## Installing
```
pip install zoom-python
```
### Usage
```python
from zoom.client import Client
client = Client(client_id, client_secret)
```
To obtain and set an access token, follow this instructions:
1. **Get authorization URL**
```python
url = client.authorization_url(redirect_uri)
```
2. **Get access token using code**
```python
response = client.get_access_token(code)
```
3. **Set access token**
```python
client.set_token(access_token)
```
If your access token expired, you can get a new one using refresh token:
```python
response = client.refresh_access_token(refresh_token)
```
And then set access token again...
Read more about Zoom Oauth: https://developers.zoom.us/docs/integrations/oauth/

#### - Get current user
```python
user = client.get_current_user()
```
#### - List Users
```python
users = client.list_users()
```
### Meetings
#### - List meetings
```python
meetings = client.list_meetings()
```
#### - Get a meeting
```python
meeting = client.get_meeting(meeting_id)
```
#### - Create Meeting
```python
meeting = client.create_meeting(
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
    )
```
More info: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingCreate

#### - Add meeting registrant (this feature requires premium auth)
```python
meeting = client.add_meeting_registrant(
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
    )
```
More info: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantCreate
