import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

import bridge


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return self.body


class BridgeTests(unittest.TestCase):
    def setUp(self):
        bridge.LOCAL_TIMEZONE = ZoneInfo("Europe/Vienna")

    def test_parse_timed_all_day_and_cancelled_events(self):
        window_start = datetime(2026, 9, 9, tzinfo=bridge.LOCAL_TIMEZONE)
        window_end = window_start + timedelta(days=7)
        calendar = """BEGIN:VCALENDAR
BEGIN:VEVENT
UID:timed
DTSTART;TZID=Europe/Vienna:20260910T093000
DTEND;TZID=Europe/Vienna:20260910T103000
SUMMARY:Besprechung
END:VEVENT
BEGIN:VEVENT
UID:all-day
DTSTART;VALUE=DATE:20260911
DTEND;VALUE=DATE:20260912
SUMMARY:Urlaub
END:VEVENT
BEGIN:VEVENT
UID:cancelled
DTSTART;TZID=Europe/Vienna:20260912T090000
STATUS:CANCELLED
SUMMARY:Abgesagt
END:VEVENT
END:VCALENDAR"""

        events = bridge.parse_events(calendar, window_start, window_end)

        self.assertEqual([event["id"].split("2026", 1)[0] for event in events], ["timed", "all-day"])
        self.assertEqual(events[0]["timeLabel"], "09:30–10:30")
        self.assertEqual(events[1]["timeLabel"], "Ganztägig")

    def test_fetch_events_deduplicates_calendar_responses(self):
        event_date = datetime.now(bridge.LOCAL_TIMEZONE).date() + timedelta(days=1)
        start = event_date.strftime("%Y%m%d") + "T090000Z"
        end = event_date.strftime("%Y%m%d") + "T100000Z"
        calendar = f"""BEGIN:VCALENDAR
BEGIN:VEVENT
UID:duplicate
DTSTART:{start}
DTEND:{end}
SUMMARY:Termin
END:VEVENT
END:VCALENDAR"""
        calendar_xml = escape(calendar)
        response = f"""<?xml version="1.0"?>
<d:multistatus xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">
  <d:response><d:propstat><d:prop><c:calendar-data>{calendar_xml}</c:calendar-data></d:prop></d:propstat></d:response>
  <d:response><d:propstat><d:prop><c:calendar-data>{calendar_xml}</c:calendar-data></d:prop></d:propstat></d:response>
</d:multistatus>""".encode()

        with (
            patch.object(bridge, "CALDAV_URL", "https://caldav.fastmail.com/dav/calendars/user/example/calendar"),
            patch.object(bridge, "CALDAV_USERNAME", "user"),
            patch.object(bridge, "CALDAV_PASSWORD", "secret"),
            patch("bridge.urllib.request.urlopen", return_value=FakeResponse(response)),
        ):
            events = bridge.fetch_events(30)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "Termin")

    def test_configuration_requires_fastmail_https_calendar_url(self):
        valid_url = "https://caldav.fastmail.com/dav/calendars/user/example/calendar"
        cases = (
            ("http://caldav.fastmail.com/dav/calendars/user/example/calendar", "must use HTTPS"),
            ("https://example.com/dav/calendars/user/example/calendar", "must use caldav.fastmail.com"),
            ("https://caldav.fastmail.com/dav/principals/user/example", "calendar collection"),
        )

        with patch.object(bridge, "CALDAV_USERNAME", "user"), patch.object(bridge, "CALDAV_PASSWORD", "secret"):
            with patch.object(bridge, "CALDAV_URL", valid_url):
                bridge.validate_configuration()
            for url, message in cases:
                with (
                    self.subTest(url=url),
                    patch.object(bridge, "CALDAV_URL", url),
                    self.assertRaisesRegex(RuntimeError, message),
                ):
                    bridge.validate_configuration()

    def test_query_values_are_bounded_and_invalid_values_fail(self):
        self.assertEqual(bridge.bounded_query_integer({}, "days", 30, 1, 90), 30)
        self.assertEqual(bridge.bounded_query_integer({"days": ["0"]}, "days", 30, 1, 90), 1)
        self.assertEqual(bridge.bounded_query_integer({"days": ["100"]}, "days", 30, 1, 90), 90)
        with self.assertRaisesRegex(ValueError, "days must be an integer"):
            bridge.bounded_query_integer({"days": ["invalid"]}, "days", 30, 1, 90)


if __name__ == "__main__":
    unittest.main()
