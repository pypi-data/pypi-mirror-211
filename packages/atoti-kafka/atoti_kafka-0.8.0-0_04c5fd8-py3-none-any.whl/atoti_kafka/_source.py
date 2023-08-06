from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import atoti as tt
from atoti._sources.data_source import DataSource


class KafkaDataSource(DataSource):
    @property
    def key(self) -> str:
        return "KAFKA"

    def load_kafka_into_table(
        self,
        table: tt.Table,
        *,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        batch_duration: int,
        consumer_config: Mapping[str, str],
    ) -> None:
        """Consume a Kafka topic and stream its records in an existing table."""
        params: dict[str, Any] = {
            "bootstrapServers": bootstrap_servers,
            "topic": topic,
            "consumerGroupId": group_id,
            "keyDeserializerClass": "org.apache.kafka.common.serialization.StringDeserializer",
            "batchDuration": batch_duration,
            "additionalParameters": consumer_config,
        }
        self.load_data_into_table(
            table.name,
            scenario_name=table.scenario,
            source_params=params,
        )


def load_kafka(
    table: tt.Table,
    /,
    bootstrap_server: str,
    topic: str,
    *,
    group_id: str,
    batch_duration: int,
    consumer_config: Mapping[str, str],
) -> None:
    KafkaDataSource(
        load_data_into_table=table._java_api.load_data_into_table
    ).load_kafka_into_table(
        table,
        bootstrap_servers=bootstrap_server,
        topic=topic,
        group_id=group_id,
        batch_duration=batch_duration,
        consumer_config=consumer_config,
    )
