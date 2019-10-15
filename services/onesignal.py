"""Onesignal API client."""

import json

import requests

import settings

# TODO(juan) move to async connections, ala http3.

_ONESIGNAL_API_URL = 'https://onesignal.com/api/v1'


def get_apps():
    """Get registered apps in onesignal.

    Returns:
        JSON object with registered apps in account.
    """
    headers = {'Authorization': f'Basic {settings.ONESIGNAL_AUTH_KEY}'}
    return requests.get(f'{_ONESIGNAL_API_URL}/apps', headers=headers).json()


def get_app(app_id):
    """Get a specific app registered in onesignal.

    Args:
        app_id: app id to be requested.
    Returns:
        JSON object with registered apps in account.
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {settings.ONESIGNAL_AUTH_KEY}'
    }
    return requests.get(
        f'{_ONESIGNAL_API_URL}/apps/{app_id}',
        headers=headers).json()


def send_notification():
    """Send a notification to all users.

    Returns:
        JSON object.
    """
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'Basic {settings.ONESIGNAL_REST_KEY}'
    }
    payload = {"app_id": settings.ONESIGNAL_APP_ID,
               "included_segments": ["All"],
               "contents": {"en": "English Message"}}
    return requests.post(
        f'{_ONESIGNAL_API_URL}/notifications',
        headers=headers, data=json.dumps(payload)).json()
