# 🛰️ Edge-Monitor-Pipeline

**Edge-to-Cloud Telemetry Pipeline** built with **FastAPI, Google Cloud Pub/Sub, Prometheus, and Grafana**.

This project simulates IoT devices publishing telemetry to the cloud, processes it at an *edge service* (FastAPI subscriber), and exposes observability metrics that are visualized in Grafana.  
It demonstrates modern **Network & Edge Architecture** patterns — real-time data ingestion, edge compute, and observability — ideal for roles like *Network & Edge Solutions Architect* at Intel.

---

## 🧭 Architecture Overview

```text
┌───────────────┐
│ IoT Devices   │  (Python simulator)
│  temp/humidity│
└──────┬────────┘
       │  Pub/Sub (topic: telemetry.raw)
       ▼
┌──────────────────────┐
│  Edge Ingest (FastAPI)│  ← performs edge logic, exposes /metrics
│  • subscribes to edge-ingest-sub     │
│  • transforms + aggregates           │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Prometheus + Grafana│  ← scrapes metrics & visualizes latency, throughput
└──────────────────────┘

Features

Real-time telemetry via Google Cloud Pub/Sub

Edge processing implemented in FastAPI (subscriber model)

Prometheus metrics for events, latency, errors, and queue depth

Grafana dashboards for visual analytics

Secure service-account authentication using
GOOGLE_APPLICATION_CREDENTIALS

⚙️ Setup Instructions
1. Prerequisites

Python 3.10 +

Docker & Docker Compose

A Google Cloud project → learned-pact-475307-g8

Service account with roles:

Pub/Sub Publisher

Pub/Sub Subscriber

(Pub/Sub Admin if creating topics/subs via code)

2. Environment Variables
export PROJECT_ID="learned-pact-475307-g8"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/gcp_keys/learned-pact-475307-g8-aa8e678152d7.json"

3. Infrastructure Setup
bash infra/pubsub_setup.sh "$PROJECT_ID"


Creates:

Topic → telemetry.raw

Subscription → edge-ingest-sub

🧩 Components
▶ IoT Simulator (Publisher)

Simulates 10 sensors publishing JSON messages.

cd iot_simulator
python3 -m pip install google-cloud-pubsub
python3 publish.py


Example output:

Published: {'device_id': 'sensor-003', 'site': 'SFO', 'temp_c': 37.4, 'status': 'OK'}

▶ Edge Ingest Service (Subscriber + Metrics)
cd edge_ingest
python3 -m pip install -r requirements.txt

export PROJECT_ID="learned-pact-475307-g8"
export SUBSCRIPTION_ID="edge-ingest-sub"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/gcp_keys/learned-pact-475307-g8-aa8e678152d7.json"

uvicorn app:app --host 0.0.0.0 --port 8000


Endpoints:

Health → /healthz

Metrics → /metrics

▶ Observability Stack
cd infra
docker compose up -d


Services:

Prometheus → http://localhost:9090

Grafana → http://localhost:3000
 (admin/admin)

In Grafana → Add Data Source → URL = http://prometheus:9090
Import or build dashboards using:

rate(edge_ingested_events_total[1m])

histogram_quantile(0.9, sum(rate(edge_ingest_latency_seconds_bucket[5m])) by (le))

increase(edge_ingest_errors_total[5m])

sum by (site,status) (increase(edge_ingested_events_total[5m]))

📊 Example Metrics
Metric	Description
edge_ingested_events_total{site,status}	Count of ingested messages
edge_ingest_latency_seconds	Histogram of processing latency
edge_ingest_errors_total	Total ingest errors
edge_queue_depth	Approximate backlog depth
🧠 How It Works

IoT Simulator publishes random sensor data to telemetry.raw.

Edge Ingest Service subscribes via Pub/Sub, processes each message, and updates Prometheus metrics.

Prometheus scrapes metrics from /metrics every 5 seconds.

Grafana visualizes live throughput, latency, and error rates.

🧪 Test Scenarios

Increase simulator rate → observe higher throughput in Grafana

Inject invalid JSON → verify edge_ingest_errors_total increments

Stop Edge Ingest temporarily → check backlog growth

🧰 Tech Stack
Layer	Technology
Edge API	FastAPI, Uvicorn
Messaging	Google Cloud Pub/Sub
Metrics	Prometheus Client
Visualization	Grafana
Deployment	Docker Compose / Cloud Run
Language	Python 3.10+
🔒 Security & IAM

Credentials are not baked into Docker images.

Authentication provided via environment variable GOOGLE_APPLICATION_CREDENTIALS.

Principle of least privilege (Pub/Sub Publisher + Subscriber roles only).

🧭 Next Steps

Deploy edge_ingest to Cloud Run or GKE Edge Node.

Add BigQuery sink for historical analytics.

Integrate Grafana alerts (e.g., latency > 0.5 s or error > 5%).

Optionally build a Copilot/LLM-based analyzer that summarizes edge telemetry anomalies.

📄 License

MIT License — feel free to fork and extend.

👩‍💻 Author

Lakshmi Achary
📍 Sacramento, CA
🔗 linkedin.com/in/lakshmi-achary
