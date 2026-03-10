import os
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    JSON,
    Float,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine

# ---------------------------------------------------------------------------
# Database URL handling – supports multiple env var names and normalises the
# PostgreSQL driver scheme.
# ---------------------------------------------------------------------------
_db_url = os.getenv(
    "DATABASE_URL",
    os.getenv("POSTGRES_URL", "sqlite:///./app.db")
)
if _db_url.startswith("postgresql+asyncpg://"):
    _db_url = _db_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql+psycopg://")

_connect_args = {}
if _db_url.startswith("postgresql+psycopg://"):
    # Apply SSL unless connecting to localhost (common for local dev)
    if "localhost" not in _db_url and "127.0.0.1" not in _db_url:
        _connect_args["sslmode"] = "require"

engine = create_engine(_db_url, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# ---------------------------------------------------------------------------
# Core tables – prefixed with "la_" to avoid collisions in a shared DB.
# ---------------------------------------------------------------------------
class Workspace(Base):
    __tablename__ = "la_workspaces"

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String(150), nullable=False)
    org_id = Column(PGUUID(as_uuid=True), nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    resources = relationship("Resource", back_populates="workspace")

class Resource(Base):
    __tablename__ = "la_resources"

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    workspace_id = Column(PGUUID(as_uuid=True), ForeignKey("la_workspaces.id"), nullable=False)
    url = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text)
    summary = Column(Text)
    tags = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    workspace = relationship("Workspace", back_populates="resources")
    outgoing_edges = relationship(
        "GraphEdge",
        foreign_keys="GraphEdge.source_id",
        back_populates="source",
        cascade="all, delete-orphan",
    )
    incoming_edges = relationship(
        "GraphEdge",
        foreign_keys="GraphEdge.target_id",
        back_populates="target",
        cascade="all, delete-orphan",
    )

class GraphEdge(Base):
    __tablename__ = "la_graph_edges"

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    source_id = Column(PGUUID(as_uuid=True), ForeignKey("la_resources.id"), nullable=False)
    target_id = Column(PGUUID(as_uuid=True), ForeignKey("la_resources.id"), nullable=False)
    relationship_type = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source = relationship("Resource", foreign_keys=[source_id], back_populates="outgoing_edges")
    target = relationship("Resource", foreign_keys=[target_id], back_populates="incoming_edges")

# Utility function for FastAPI dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
