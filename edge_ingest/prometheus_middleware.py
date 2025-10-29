from prometheus_client import Counter, Histogram, Gauge

ingested_events = Counter("edge_ingested_events_total", "Total ingested messages", ["site", "status"])
ingest_latency = Histogram("edge_ingest_latency_seconds", "Latency to process a message")
ingest_errors = Counter("edge_ingest_errors_total", "Total ingest errors")
queue_depth = Gauge("edge_queue_depth", "Approx subscription backlog")

# Expose these from app.py for use during processing

