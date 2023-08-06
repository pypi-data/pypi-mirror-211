from pathlib import Path
from typing import Optional

import atoti as tt
from atoti_core import BaseSessionBound, Plugin


class SnowflakePlugin(Plugin):
    def init_session(self, session: BaseSessionBound, /) -> None:
        if not isinstance(session, tt.Session):
            return

        session._java_api.gateway.jvm.io.atoti.directquery.snowflake.SnowflakePlugin.init()

    @property
    def jar_path(self) -> Optional[Path]:
        return Path(__file__).parent / "data" / "atoti-directquery-snowflake.jar"
