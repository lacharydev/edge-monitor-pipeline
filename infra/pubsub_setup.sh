#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="$1"                # learned-pact-475307-g8
TOPIC="telemetry.raw"
SUBSCRIPTION="edge-ingest-sub"

gcloud config set project "${PROJECT_ID}"

# Topic & subscription
gcloud pubsub topics create "${TOPIC}" || true
gcloud pubsub subscriptions create "${SUBSCRIPTION}" \
  --topic="${TOPIC}" \
  --ack-deadline=20 || true

echo "Pub/Sub ready: topic=${TOPIC}, subscription=${SUBSCRIPTION}"

