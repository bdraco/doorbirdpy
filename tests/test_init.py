from doorbirdpy import DoorBird
from doorbirdpy.schedule_entry import DoorBirdScheduleEntry

MOCK_HOST = "127.0.0.1"
MOCK_USER = "user"
MOCK_PASS = "pass"
URL_TEMPLATE = "http://{}:{}@{}:80{}"


def test_ready(requests_mock):
    with open("tests/info.json") as f:
        requests_mock.register_uri(
            "get",
            URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/info.cgi"),
            text=f.read(),
        )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    ready, code = db.ready()
    assert ready is True
    assert code == 200


def test_http_url():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    url = db._url(
        path="/test",
        args=[
            ("arg1", "value1"),
            ("arg2", "value2"),
        ],
    )
    assert url == f"http://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:80/test?arg1=value1&arg2=value2"


def test_http_url_custom_port():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS, port=8080)
    url = db._url("/test")
    assert url == f"http://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:8080/test"


def test_https_url():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS, secure=True)
    url = db._url("/test")
    assert url == f"https://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:443/test"


def test_https_url_custom_port():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS, secure=True, port=8443)
    url = db._url("/test")
    assert url == f"https://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:8443/test"


def test_rtsp_url():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.rtsp_live_video_url.startswith(f"rtsp://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:554")


def test_rtsp_http_url():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.rtsp_over_http_live_video_url.startswith(f"rtsp://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:8557")


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
    with open("tests/schedule.json") as f:
        requests_mock.register_uri(
            "get",
            URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/schedule.cgi"),
            text=f.read(),
        )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert len(db.schedule()) == 3


def test_get_schedule_entry(requests_mock):
    with open("tests/schedule_get_entry.json") as f:
        requests_mock.register_uri(
            "get",
            URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/schedule.cgi"),
            text=f.read(),
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
    with open("tests/info.json") as f:
        requests_mock.register_uri(
            "get",
            URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/info.cgi"),
            text=f.read(),
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


def test_reset(requests_mock):
    requests_mock.register_uri("get", URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/restart.cgi"))

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.restart() is True
