from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Any

from dotenv import load_dotenv
from neo4j import Driver, GraphDatabase, RoutingControl
from neo4j.exceptions import Neo4jError


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"


def _required_environment_variable(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True, slots=True)
class Neo4jSettings:
    """Connection settings loaded from environment variables."""

    uri: str
    username: str
    password: str
    database: str

    @classmethod
    def from_env(cls, env_file: str | Path = DEFAULT_ENV_FILE) -> "Neo4jSettings":
        load_dotenv(dotenv_path=env_file, override=False)
        return cls(
            uri=_required_environment_variable("NEO4J_URI"),
            username=_required_environment_variable("NEO4J_USERNAME"),
            password=_required_environment_variable("NEO4J_PASSWORD"),
            database=os.getenv("NEO4J_DATABASE", "neo4j").strip() or "neo4j",
        )


class Neo4jDatabase:
    """Own the Neo4j driver and expose small, explicit query helpers."""

    def __init__(self, settings: Neo4jSettings) -> None:
        self.settings = settings
        self._driver: Driver = GraphDatabase.driver(
            settings.uri,
            auth=(settings.username, settings.password),
        )

    @classmethod
    def from_env(cls, env_file: str | Path = DEFAULT_ENV_FILE) -> "Neo4jDatabase":
        return cls(Neo4jSettings.from_env(env_file))

    def close(self) -> None:
        self._driver.close()

    def run(
        self,
        cypher: str,
        parameters: dict[str, Any] | None = None,
        *,
        database: str | None = None,
        write: bool = False,
    ) -> list[dict[str, Any]]:
        """Run one Cypher statement and return records as plain dictionaries."""

        records, _, _ = self._driver.execute_query(
            cypher,
            parameters_=parameters or {},
            database_=database or self.settings.database,
            routing_=RoutingControl.WRITE if write else RoutingControl.READ,
        )
        return [record.data() for record in records]

    def ping(self) -> dict[str, Any]:
        """Verify the server handshake and a query against the target database."""

        self._driver.verify_connectivity()
        records, summary, _ = self._driver.execute_query(
            "RETURN 1 AS ok",
            database_=self.settings.database,
            routing_=RoutingControl.READ,
        )
        if len(records) != 1:
            raise RuntimeError("Neo4j ping returned an unexpected record count")
        record = records[0]
        return {
            "ok": record["ok"] == 1,
            "database": self.settings.database,
            "server": summary.server.agent,
            "address": str(summary.server.address),
        }

    def __enter__(self) -> "Neo4jDatabase":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()


def main() -> None:
    try:
        with Neo4jDatabase.from_env() as database:
            result = database.ping()
    except (Neo4jError, OSError, ValueError) as error:
        raise SystemExit(f"Neo4j connection failed: {error}") from error

    print(
        "Neo4j connection OK "
        f"(database={result['database']}, server={result['server']}, "
        f"address={result['address']})"
    )


if __name__ == "__main__":
    main()
