from pathlib import Path
from typing import Optional

import atoti as tt
from atoti_core import BaseSessionBound, Plugin

from ._source import load_kafka


class KafkaPlugin(Plugin):
    def init_session(self, session: BaseSessionBound, /) -> None:
        if not isinstance(session, tt.Session):
            return

        session._java_api.gateway.jvm.io.atoti.loading.kafka.KafkaPlugin.init()
        session._load_kafka = load_kafka

    @property
    def jar_path(self) -> Optional[Path]:
        return Path(__file__).parent / "data" / "atoti-kafka.jar"
