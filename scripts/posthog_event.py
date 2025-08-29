
import os, time, json, uuid, urllib.request

API_KEY = os.environ.get("POSTHOG_API_KEY")
HOST = os.environ.get("POSTHOG_HOST", "https://app.posthog.com")
if not API_KEY:
    print("Set POSTHOG_API_KEY to send an event, skipping.")
    raise SystemExit(0)

url = f"{HOST}/capture/"
event = {
    "api_key": API_KEY,
    "event": "pipeline_run",
    "properties": {"source": "demo", "ts": int(time.time())},
    "distinct_id": str(uuid.uuid4()),
}

data = json.dumps(event).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as resp:
    print("PostHog response:", resp.status, resp.read().decode())
