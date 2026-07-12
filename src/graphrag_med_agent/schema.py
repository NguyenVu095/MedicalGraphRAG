"""Constraints and indexes for the medical knowledge graph."""

from __future__ import annotations

from neo4j.exceptions import Neo4jError

from .database import Neo4jDatabase


SCHEMA_STATEMENTS: tuple[tuple[str, str], ...] = (
    (
        "medical_concept_id_unique",
        """
        CREATE CONSTRAINT medical_concept_id_unique IF NOT EXISTS
        FOR (node:MedicalConcept) REQUIRE node.id IS UNIQUE
        """,
    ),
    (
        "document_id_unique",
        """
        CREATE CONSTRAINT document_id_unique IF NOT EXISTS
        FOR (node:Document) REQUIRE node.id IS UNIQUE
        """,
    ),
    (
        "chunk_id_unique",
        """
        CREATE CONSTRAINT chunk_id_unique IF NOT EXISTS
        FOR (node:Chunk) REQUIRE node.id IS UNIQUE
        """,
    ),
    (
        "medical_concept_normalized_name_idx",
        """
        CREATE INDEX medical_concept_normalized_name_idx IF NOT EXISTS
        FOR (node:MedicalConcept) ON (node.normalized_name)
        """,
    ),
    (
        "medical_concept_code_idx",
        """
        CREATE INDEX medical_concept_code_idx IF NOT EXISTS
        FOR (node:MedicalConcept) ON (node.code)
        """,
    ),
    (
        "document_checksum_idx",
        """
        CREATE INDEX document_checksum_idx IF NOT EXISTS
        FOR (node:Document) ON (node.checksum)
        """,
    ),
    (
        "chunk_document_position_idx",
        """
        CREATE INDEX chunk_document_position_idx IF NOT EXISTS
        FOR (node:Chunk) ON (node.document_id, node.position)
        """,
    ),
    (
        "medical_concept_fulltext",
        """
        CREATE FULLTEXT INDEX medical_concept_fulltext IF NOT EXISTS
        FOR (node:MedicalConcept)
        ON EACH [node.name, node.normalized_name, node.aliases]
        """,
    ),
    (
        "chunk_text_fulltext",
        """
        CREATE FULLTEXT INDEX chunk_text_fulltext IF NOT EXISTS
        FOR (node:Chunk) ON EACH [node.text]
        """,
    ),
)


def initialize_schema(database: Neo4jDatabase) -> list[str]:
    """Apply the idempotent schema and return the processed object names."""

    applied: list[str] = []
    for name, statement in SCHEMA_STATEMENTS:
        database.run(statement, write=True)
        applied.append(name)
    return applied


def main() -> None:
    try:
        with Neo4jDatabase.from_env() as database:
            ping = database.ping()
            applied = initialize_schema(database)
            constraints = database.run(
                "SHOW CONSTRAINTS YIELD name RETURN name ORDER BY name"
            )
            indexes = database.run(
                "SHOW INDEXES YIELD name, type, state "
                "RETURN name, type, state ORDER BY name"
            )
    except (Neo4jError, OSError, ValueError) as error:
        raise SystemExit(f"Neo4j schema initialization failed: {error}") from error

    print(
        f"Schema initialized on database={ping['database']} "
        f"({len(applied)} statements, {len(constraints)} constraints, "
        f"{len(indexes)} indexes)."
    )


if __name__ == "__main__":
    main()
