import os, json, time
import threading
from fastapi import FastAPI
from google.cloud import pubsub_v1
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from prometheus_middleware import ingested_events, ingest_latency, ingest_errors, queue_depth

PROJECT_ID = os.environ["PROJECT_ID"]
SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", "edge-ingest-sub")
METRICS_PORT = int(os.environ.get("METRICS_PORT", "8000"))

app = FastAPI(title="Edge Ingest")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

def process_message(msg):
    start = time.time()
    try:
        payload = json.loads(msg.data.decode("utf-8"))
        site = payload.get("site", "unknown")
        status = payload.get("status", "UNKNOWN")
        # Example “edge compute”: simple rule
        if status == "FAIL" and payload.get("temp_c", 0) > 40:
            # In a real pipeline, trigger alert/edge action here
            pass
        ingested_events.labels(site=site, status=status).inc()
        msg.ack()
    except Exception:
        ingest_errors.inc()
        msg.nack()
    finally:
        ingest_latency.observe(time.time() - start)

def subscriber_thread():
    subscriber = pubsub_v1.SubscriberClient()
    sub_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    streaming_pull_future = subscriber.subscribe(sub_path, callback=process_message)
    try:
        streaming_pull_future.result()
    except:  # noqa
        streaming_pull_future.cancel()

def backlog_updater():
    # Update queue_depth gauge periodically
    from google.cloud.pubsub_v1 import SubscriberClient
    sub_client = SubscriberClient()
    sub_path = sub_client.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    while True:
        try:
            # Approximate: pull 0 to fetch stats via request (not exact)
            queue_depth.set(0)  # Left simple; advanced: use metrics from Cloud Monitoring
        except:  # noqa
            pass
        time.sleep(15)

def start_background_threads():
    threading.Thread(target=subscriber_thread, daemon=True).start()
    threading.Thread(target=backlog_updater, daemon=True).start()

@app.on_event("startup")
def on_startup():
    start_background_threads()

