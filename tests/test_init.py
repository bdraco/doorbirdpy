from doorbirdpy import DoorBird
from doorbirdpy.schedule_entry import DoorBirdScheduleEntry

from requests.exceptions import HTTPError
from requests.models import Response
from requests.structures import CaseInsensitiveDict

import pytest
import requests
import requests_mock

MOCK_HOST = "127.0.0.1"
MOCK_USER = "user"
MOCK_PASS = "pass"
URL_TEMPLATE = "http://{}:{}@{}:80{}"


def test_ready(requests_mock):
    requests_mock.register_uri(
        "get",
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/info.cgi"),
        text='{"BHA": {"RETURNCODE": "1", "VERSION": [{"FIRMWARE": "000125", "BUILD_NUMBER": "15870439", "WIFI_MAC_ADDR": "1234ABCD", "RELAYS": ["1", "2", "ghchdi@1", "ghchdi@2", "ghchdi@3", "ghdwkh@1", "ghdwkh@2", "ghdwkh@3"], "DEVICE-TYPE": "DoorBird D2101V"}]}}',
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    ready, code = db.ready()
    assert ready is True
    assert code == 200


def test_energize_relay(requests_mock):
    requests_mock.register_uri(
        "get",
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/open-door.cgi"),
        text='{"BHA": {"RETURNCODE": "1"}}',
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.energize_relay() is True


def test_turn_light_on(requests_mock):
    requests_mock.register_uri(
        "get",
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/light-on.cgi"),
        text='{"BHA": {"RETURNCODE": "1"}}',
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.turn_light_on() is True


def test_schedule(requests_mock):
    requests_mock.register_uri(
        "get",
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/schedule.cgi"),
        text='[{"input": "doorbell", "param": "1", "output": [{"event": "notify", "param": "", "schedule": {"weekdays": [{"to": "107999", "from": "108000"}]}}, {"event": "http", "param": "0", "schedule": {"weekdays": [{"to": "107999", "from": "108000"}]}}]}, {"input": "motion", "param": "", "output": [{"event": "notify", "param": "", "schedule": {"weekdays": [{"to": "107999", "from": "108000"}]}}, {"event": "http", "param": "5", "schedule": {"weekdays": [{"to": "107999", "from": "108000"}]}}]}, {"input": "relay", "param": "1", "output": []}]',
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert len(db.schedule()) == 3


def test_get_schedule_entry(requests_mock):
    requests_mock.register_uri(
        "get",
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/schedule.cgi"),
        text='[{"input": "doorbell", "param": "1", "output": [{"event": "notify", "param": "", "schedule": {"weekdays": [{"to": "107999", "from": "108000"}]}}, {"event": "http", "param": "0", "schedule": {"weekdays": [{"to": "107999", "from": "108000"}]}}]}, {"input": "motion", "param": "", "output": [{"event": "notify", "param": "", "schedule": {"weekdays": [{"to": "107999", "from": "108000"}]}}, {"event": "http", "param": "5", "schedule": {"weekdays": [{"to": "107999", "from": "108000"}]}}]}, {"input": "relay", "param": "1", "output": []}]',
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert isinstance(db.get_schedule_entry("doorbell", "1"), DoorBirdScheduleEntry)


def test_doorbell_state_false(requests_mock):
    requests_mock.register_uri(
        "get",
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/monitor.cgi"),
        text="doorbell=0\r\n",
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.doorbell_state() is False


def test_doorbell_state_true(requests_mock):
    requests_mock.register_uri(
        "get",
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/monitor.cgi"),
        text="doorbell=1\r\n",
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.doorbell_state() is True


def test_motion_sensor_state_false(requests_mock):
    requests_mock.register_uri(
        "get",
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/monitor.cgi"),
        text="motionsensor=0\r\n",
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.motion_sensor_state() is False


def test_motion_sensor_state_true(requests_mock):
    requests_mock.register_uri(
        "get",
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/monitor.cgi"),
        text="motionsensor=1\r\n",
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.motion_sensor_state() is True


def test_info(requests_mock):
    requests_mock.register_uri(
        "get",
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/info.cgi"),
        text='{"BHA": {"RETURNCODE": "1", "VERSION": [{"FIRMWARE": "000125", "BUILD_NUMBER": "15870439", "WIFI_MAC_ADDR": "1234ABCD", "RELAYS": ["1", "2", "ghchdi@1", "ghchdi@2", "ghchdi@3", "ghdwkh@1", "ghdwkh@2", "ghdwkh@3"], "DEVICE-TYPE": "DoorBird D2101V"}]}}',
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    data = db.info()
    assert data == {
        "BUILD_NUMBER": "15870439",
        "DEVICE-TYPE": "DoorBird D2101V",
        "FIRMWARE": "000125",
        "RELAYS": [
            "1",
            "2",
            "ghchdi@1",
            "ghchdi@2",
            "ghchdi@3",
            "ghdwkh@1",
            "ghdwkh@2",
            "ghdwkh@3",
        ],
        "WIFI_MAC_ADDR": "1234ABCD",
    }