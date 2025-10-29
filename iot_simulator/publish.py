import json, os, random, time
from datetime import datetime, timezone
from google.cloud import pubsub_v1

PROJECT_ID = os.environ.get("PROJECT_ID")
TOPIC_ID = os.environ.get("TOPIC_ID", "telemetry.raw")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

DEVICE_IDS = [f"sensor-{i:03d}" for i in range(1, 11)]

def make_event():
    return {
        "device_id": random.choice(DEVICE_IDS),
        "site": random.choice(["SFO", "PDX", "NYC"]),
        "temp_c": round(random.uniform(15, 45), 2),
        "humidity": round(random.uniform(20, 90), 1),
        "status": random.choice(["OK", "WARN", "FAIL"]),
        "ts": datetime.now(timezone.utc).isoformat()
    }

def main():
    while True:
        event = make_event()
        data = json.dumps(event).encode("utf-8")
        future = publisher.publish(topic_path, data)
        future.result(timeout=30)
        print("Published:", event)
        time.sleep(0.25)  # 4 msgs/sec. Tweak as needed.

if __name__ == "__main__":
    if not PROJECT_ID:
        raise SystemExit("Set PROJECT_ID env var")
    main()

