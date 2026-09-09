import base64
import json
import os
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, time, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CALDAV_URL = os.environ.get("FASTMAIL_CALDAV_URL", "").strip()
CALDAV_USERNAME = os.environ.get("FASTMAIL_USERNAME", "")
CALDAV_PASSWORD = os.environ.get("FASTMAIL_APP_PASSWORD", "")
LOCAL_TIMEZONE = ZoneInfo(os.environ.get("TZ", "Europe/Vienna"))
PORT = int(os.environ.get("PORT", "8090"))
FASTMAIL_CALDAV_HOST = "caldav.fastmail.com"

GERMAN_WEEKDAYS = ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")
ICAL_DATETIME = re.compile(r"^(\d{8})T(\d{6})(Z?)$")


def validate_configuration():
    if not CALDAV_URL or not CALDAV_USERNAME or not CALDAV_PASSWORD:
        raise RuntimeError("Fastmail CalDAV configuration is incomplete")

    parsed = urlparse(CALDAV_URL)
    if parsed.scheme != "https":
        raise RuntimeError("Fastmail CalDAV URL must use HTTPS")
    if parsed.hostname != FASTMAIL_CALDAV_HOST:
        raise RuntimeError(f"Fastmail CalDAV URL must use {FASTMAIL_CALDAV_HOST}")
    if parsed.username is not None or parsed.password is not None:
        raise RuntimeError("Fastmail CalDAV URL must not contain credentials")
    if parsed.port not in (None, 443):
        raise RuntimeError("Fastmail CalDAV URL must use the standard HTTPS port")
    if not parsed.path.startswith("/dav/calendars/"):
        raise RuntimeError("Fastmail CalDAV URL must point to a calendar collection")
    if parsed.query or parsed.fragment:
        raise RuntimeError("Fastmail CalDAV URL must not contain a query or fragment")


def unfold_ical(value):
    return re.sub(r"\r?\n[ \t]", "", value).replace("\r\n", "\n")


def unescape_ical(value):
    return (
        value.replace("\\N", "\n")
        .replace("\\n", "\n")
        .replace("\\,", ",")
        .replace("\\;", ";")
        .replace("\\\\", "\\")
    )


def parse_property(line):
    if ":" not in line:
        return None, {}, ""
    head, value = line.split(":", 1)
    parts = head.split(";")
    parameters = {}
    for parameter in parts[1:]:
        if "=" in parameter:
            key, parameter_value = parameter.split("=", 1)
            parameters[key.upper()] = parameter_value.strip('"')
    return parts[0].upper(), parameters, value


def timezone_for(name):
    if not name:
        return LOCAL_TIMEZONE
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        return LOCAL_TIMEZONE


def parse_ical_datetime(value, parameters):
    if parameters.get("VALUE") == "DATE" or (len(value) == 8 and "T" not in value):
        parsed_date = datetime.strptime(value[:8], "%Y%m%d").date()
        return datetime.combine(parsed_date, time.min, LOCAL_TIMEZONE), True

    match = ICAL_DATETIME.match(value)
    if not match:
        raise ValueError("unsupported iCalendar datetime")

    parsed = datetime.strptime(match.group(1) + match.group(2), "%Y%m%d%H%M%S")
    source_timezone = timezone.utc if match.group(3) == "Z" else timezone_for(parameters.get("TZID"))
    return parsed.replace(tzinfo=source_timezone).astimezone(LOCAL_TIMEZONE), False


def parse_events(calendar_data, window_start, window_end):
    events = []
    current = None

    for line in unfold_ical(calendar_data).splitlines():
        if line == "BEGIN:VEVENT":
            current = {}
            continue
        if line == "END:VEVENT":
            if current is not None:
                event = build_event(current, window_start, window_end)
                if event:
                    events.append(event)
            current = None
            continue
        if current is None:
            continue

        name, parameters, value = parse_property(line)
        if name in {"DTSTART", "DTEND", "SUMMARY", "LOCATION", "URL", "UID", "STATUS"}:
            current[name] = (parameters, value)

    return events


def build_event(properties, window_start, window_end):
    if "DTSTART" not in properties or properties.get("STATUS", ({}, ""))[1].upper() == "CANCELLED":
        return None

    try:
        start, all_day = parse_ical_datetime(properties["DTSTART"][1], properties["DTSTART"][0])
        if "DTEND" in properties:
            end, _ = parse_ical_datetime(properties["DTEND"][1], properties["DTEND"][0])
        else:
            end = start + (timedelta(days=1) if all_day else timedelta(hours=1))
    except (ValueError, TypeError):
        return None

    if end <= window_start or start >= window_end:
        return None

    title = unescape_ical(properties.get("SUMMARY", ({}, "Termin"))[1]) or "Termin"
    location = unescape_ical(properties.get("LOCATION", ({}, ""))[1])
    event_url = properties.get("URL", ({}, ""))[1]
    uid = properties.get("UID", ({}, ""))[1]

    time_label = "Ganztägig" if all_day else start.strftime("%H:%M")
    if not all_day and end.date() == start.date() and end > start:
        time_label += "–" + end.strftime("%H:%M")

    return {
        "id": uid + start.isoformat(),
        "title": title,
        "location": location,
        "url": event_url,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "allDay": all_day,
        "dateLabel": f"{GERMAN_WEEKDAYS[start.weekday()]}, {start.strftime('%d.%m.')}",
        "timeLabel": time_label,
    }


def fetch_events(days):
    now = datetime.now(LOCAL_TIMEZONE)
    window_start = datetime.combine(now.date(), time.min, LOCAL_TIMEZONE)
    window_end = window_start + timedelta(days=days)
    caldav_start = window_start.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    caldav_end = window_end.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    body = f'''<?xml version="1.0" encoding="utf-8" ?>
<c:calendar-query xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">
  <d:prop>
    <d:getetag />
    <c:calendar-data><c:expand start="{caldav_start}" end="{caldav_end}" /></c:calendar-data>
  </d:prop>
  <c:filter>
    <c:comp-filter name="VCALENDAR">
      <c:comp-filter name="VEVENT"><c:time-range start="{caldav_start}" end="{caldav_end}" /></c:comp-filter>
    </c:comp-filter>
  </c:filter>
</c:calendar-query>'''.encode()

    credentials = base64.b64encode(f"{CALDAV_USERNAME}:{CALDAV_PASSWORD}".encode()).decode()
    request = urllib.request.Request(
        CALDAV_URL,
        data=body,
        method="REPORT",
        headers={
            "Authorization": "Basic " + credentials,
            "Content-Type": "application/xml; charset=utf-8",
            "Depth": "1",
            "User-Agent": "dynacat-caldav-bridge/1.0",
        },
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        document = ET.fromstring(response.read())

    events = []
    for node in document.findall(".//{urn:ietf:params:xml:ns:caldav}calendar-data"):
        if node.text:
            events.extend(parse_events(node.text, window_start, window_end))

    unique_events = {event["id"]: event for event in events}
    result = sorted(unique_events.values(), key=lambda event: event["start"])
    return [event for event in result if datetime.fromisoformat(event["end"]) > now]


def bounded_query_integer(query, name, default, minimum, maximum):
    raw_value = query.get(name, [str(default)])[0]
    try:
        value = int(raw_value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must be an integer") from error
    return max(minimum, min(value, maximum))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self.send_json(200, {"status": "ok"})
            return
        if parsed.path != "/events":
            self.send_json(404, {"error": "not found"})
            return

        try:
            query = parse_qs(parsed.query)
            days = bounded_query_integer(query, "days", 30, 1, 90)
            limit = bounded_query_integer(query, "limit", 8, 1, 50)
            events = fetch_events(days)[:limit]
            self.send_json(200, {"events": events, "count": len(events)})
        except ValueError as error:
            self.send_json(400, {"error": str(error)})
        except urllib.error.HTTPError as error:
            self.send_json(502, {"error": f"Fastmail returned HTTP {error.code}"})
        except Exception as error:
            print(f"CalDAV request failed: {type(error).__name__}: {error}", flush=True)
            self.send_json(502, {"error": "CalDAV request failed"})

    def send_json(self, status, payload):
        encoded = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format_string, *args):
        print(f"{self.client_address[0]} - {format_string % args}", flush=True)


if __name__ == "__main__":
    validate_configuration()
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
