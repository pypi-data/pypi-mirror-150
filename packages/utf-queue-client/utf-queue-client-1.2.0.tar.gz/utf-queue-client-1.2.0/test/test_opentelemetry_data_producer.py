from utf_queue_client.clients.opentelemetry_data_producer import (
    OpenTelemetryDataProducer,
)
from utf_queue_client.exceptions import ValidationError
import pytest


def test_data_producer_empty_url():
    with pytest.raises(RuntimeError):
        _ = OpenTelemetryDataProducer()


def test_data_producer_central_queue(
    request,
    amqp_url,
    queue_consumer,
):
    producer = OpenTelemetryDataProducer(
        url=amqp_url, producer_app_id=request.node.name
    )
    producer.publish_telemetry_data("LOGS", b"1234")
    queue_consumer.expect_messages(1)
    producer.publish_telemetry_data("METRICS", b"1234")
    queue_consumer.expect_messages(2)
    producer.publish_telemetry_data("TRACES", b"1234")
    queue_consumer.expect_messages(3)
    with pytest.raises(ValidationError):
        producer.publish_telemetry_data("SOMETHING", b"1234")
