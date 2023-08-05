"""Models used by the DJ client."""
import enum
from typing import Dict, List, Optional

from pydantic import BaseModel


class Engine(BaseModel):
    """
    Represents an engine
    """

    name: str
    version: Optional[str]


class MaterializationConfig(BaseModel):
    """
    A node's materialization config
    """

    engine: Engine
    schedule: str
    config: Dict


class NodeMode(str, enum.Enum):
    """
    DJ node's mode
    """

    DRAFT = "draft"
    PUBLISHED = "published"


class SourceColumn(BaseModel):
    """
    A column used in creation of a source node
    """

    name: str
    type: str
    attributes: Optional[str]
    dimension: Optional[str]


class UpdateNode(BaseModel):
    """
    Fields for updating a node
    """

    display_name: Optional[str]
    description: Optional[str]
    mode: Optional[NodeMode]
    primary_key: Optional[List[str]]
    query: Optional[str]

    # source nodes only
    catalog: Optional[str]
    schema_: Optional[str]
    table: Optional[str]
    columns: Optional[List[SourceColumn]] = []


class QueryState(str, enum.Enum):
    """
    Different states of a query.
    """

    UNKNOWN = "UNKNOWN"
    ACCEPTED = "ACCEPTED"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"
    FAILED = "FAILED"

    @classmethod
    def list(cls) -> List[str]:
        """
        List of available query states as strings
        """
        return list(map(lambda c: c.value, cls))  # type: ignore


class Column(BaseModel):
    """
    Represents a column
    """

    name: str
    type: str


class Tag(BaseModel):
    """
    Node tags
    """

    name: str
    display_name: str
    tag_type: str


END_JOB_STATES = [QueryState.FINISHED, QueryState.CANCELED, QueryState.FAILED]
