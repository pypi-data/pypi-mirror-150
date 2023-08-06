from otel_extensions import (
    TelemetryOptions,
    init_telemetry_provider,
    flush_telemetry_data,
)
from contextlib import contextmanager
import os

telemetry_initialized = False

SERVICE_NAME = "UTF-Queue-Client-CLI"


@contextmanager
def setup_telemetry():
    global telemetry_initialized
    if not telemetry_initialized:
        options = TelemetryOptions(
            OTEL_SERVICE_NAME=SERVICE_NAME,
            OTEL_EXPORTER_OTLP_ENDPOINT=os.environ.get(
                "OTEL_EXPORTER_OTLP_ENDPOINT",
                "https://otel-receiver-http.dev.silabs.net",
            ),
            OTEL_EXPORTER_OTLP_PROTOCOL=os.environ.get(
                "OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf"
            ),
        )
        init_telemetry_provider(options)
        telemetry_initialized = True
    yield
    flush_telemetry_data()
