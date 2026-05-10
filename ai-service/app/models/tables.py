"""
SQLAlchemy ORM models mirroring the Prisma schema (read-only from FastAPI side,
except for embedding writes).
"""

import enum
from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID
from sqlalchemy.orm import DeclarativeBase, relationship


def _utcnow():
    return datetime.utcnow()


class Base(DeclarativeBase):
    pass


class Difficulty(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class SubmissionStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    ACCEPTED = "ACCEPTED"
    WRONG_ANSWER = "WRONG_ANSWER"
    TIME_LIMIT = "TIME_LIMIT"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    COMPILATION_ERROR = "COMPILATION_ERROR"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

    submissions = relationship("Submission", back_populates="user")
    skill_embeddings = relationship("SkillEmbedding", back_populates="user")
    knowledge_states = relationship("KnowledgeState", back_populates="student")
    mab_states = relationship("MabState", back_populates="student")
    fsrs_cards = relationship("FsrsCard", back_populates="student")
    event_logs = relationship("EventLog", back_populates="user")


class Problem(Base):
    __tablename__ = "problems"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum(Difficulty, name="Difficulty", schema="public"), nullable=False, default=Difficulty.MEDIUM)
    course_id = Column("courseId", UUID(as_uuid=True), ForeignKey("courses.id"), nullable=True)
    created_at = Column("createdAt", DateTime, server_default=func.now())
    updated_at = Column("updatedAt", DateTime, server_default=func.now(), onupdate=func.now())

    submissions = relationship("Submission", back_populates="problem")
    embedding = relationship("ProblemEmbedding", back_populates="problem", uselist=False)
    problem_concepts = relationship("ProblemConcept", back_populates="problem")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column("userId", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    problem_id = Column("problemId", UUID(as_uuid=True), ForeignKey("problems.id"), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String, nullable=False)
    status = Column(Enum(SubmissionStatus, name="SubmissionStatus", schema="public"), nullable=False, default=SubmissionStatus.PENDING)
    runtime = Column(Integer, nullable=True)
    memory = Column(Integer, nullable=True)
    created_at = Column("createdAt", DateTime, server_default=func.now())

    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")


class ProblemEmbedding(Base):
    __tablename__ = "problem_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True)
    problem_id = Column("problemId", UUID(as_uuid=True), ForeignKey("problems.id"), unique=True, nullable=False)
    embedding = Column(ARRAY(Float))
    embedding_vec = Column(Vector(384))
    updated_at = Column("updatedAt", DateTime, server_default=func.now(), onupdate=func.now())

    problem = relationship("Problem", back_populates="embedding")


class SkillEmbedding(Base):
    __tablename__ = "skill_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column("userId", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    skill_name = Column("skillName", String, nullable=False)
    embedding = Column(ARRAY(Float))
    embedding_vec = Column(Vector(384))
    score = Column(Float, default=0)
    updated_at = Column("updatedAt", DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="skill_embeddings")


# ============================================================
# Adaptive Learning Models
# ============================================================


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    topic_group = Column(String(100), nullable=True)
    difficulty_tier = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    knowledge_states = relationship("KnowledgeState", back_populates="concept")
    problem_concepts = relationship("ProblemConcept", back_populates="concept")
    fsrs_cards = relationship("FsrsCard", back_populates="concept")
    prerequisite_for = relationship(
        "KnowledgeGraphEdge",
        foreign_keys="KnowledgeGraphEdge.from_concept_id",
        back_populates="from_concept",
    )
    has_prerequisites = relationship(
        "KnowledgeGraphEdge",
        foreign_keys="KnowledgeGraphEdge.to_concept_id",
        back_populates="to_concept",
    )


class KnowledgeGraphEdge(Base):
    __tablename__ = "knowledge_graph_edges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_concept_id = Column(Integer, ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False)
    to_concept_id = Column(Integer, ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False)
    relation_type = Column(String(20), default="PREREQUISITE")
    weight = Column(Float, default=1.0)

    from_concept = relationship("Concept", foreign_keys=[from_concept_id], back_populates="prerequisite_for")
    to_concept = relationship("Concept", foreign_keys=[to_concept_id], back_populates="has_prerequisites")


class ProblemConcept(Base):
    __tablename__ = "problem_concepts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False)
    is_primary = Column("is_primary", Boolean, default=False)

    problem = relationship("Problem", back_populates="problem_concepts")
    concept = relationship("Concept", back_populates="problem_concepts")


class KnowledgeState(Base):
    """BKT state per (student, concept) pair — Layer 1"""
    __tablename__ = "knowledge_states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False)
    p_mastery = Column(Float, default=0.1, nullable=False)
    p_l0 = Column(Float, default=0.1, nullable=False)
    p_transit = Column(Float, default=0.2, nullable=False)
    p_guess = Column(Float, default=0.15, nullable=False)
    p_slip = Column(Float, default=0.1, nullable=False)
    n_attempts = Column(Integer, default=0)
    n_correct = Column(Integer, default=0)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow, server_default=func.now())

    student = relationship("User", back_populates="knowledge_states")
    concept = relationship("Concept", back_populates="knowledge_states")


class EloRating(Base):
    """Elo rating for students and problems — Layer 2"""
    __tablename__ = "elo_ratings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    entity_type = Column(String(10), nullable=False)  # 'STUDENT' or 'PROBLEM'
    concept_id = Column(Integer, nullable=True)
    rating = Column(Float, default=1200.0, nullable=False)
    k_value = Column(Float, default=25.0, nullable=False)
    trend = Column(Float, default=0.0, nullable=False)
    n_attempts = Column(Integer, default=0)
    rating_history = Column("rating_history", JSON, default=[])
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow, server_default=func.now())


class MabState(Base):
    """Multi-Armed Bandit state per (student, arm) — Layer 3"""
    __tablename__ = "mab_states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    arm_id = Column(String, nullable=False)
    arm_type = Column(String(10), nullable=False)  # 'CONCEPT' or 'PROBLEM'
    alpha = Column(Float, default=1.0, nullable=False)
    beta = Column(Float, default=1.0, nullable=False)
    n_pulls = Column(Integer, default=0)
    total_reward = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow, server_default=func.now())

    student = relationship("User", back_populates="mab_states")


class FsrsCard(Base):
    """FSRS spaced repetition card per (student, concept) — Layer 4"""
    __tablename__ = "fsrs_cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False)
    difficulty = Column(Float, default=5.0, nullable=False)
    stability = Column(Float, default=1.0, nullable=False)
    retrievability = Column(Float, default=1.0, nullable=False)
    state = Column(String(15), default="NEW")
    due_date = Column(DateTime, server_default=func.now(), nullable=False)
    last_review = Column(DateTime, nullable=True)
    reps = Column(Integer, default=0)
    lapses = Column(Integer, default=0)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow, server_default=func.now())

    student = relationship("User", back_populates="fsrs_cards")
    concept = relationship("Concept", back_populates="fsrs_cards")


# === Evaluation & Experiment Models ===


class EventLog(Base):
    """Event log for evaluation data collection"""
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event = Column(String(50), nullable=False)
    data = Column(JSON, default={})
    session_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="event_logs")


class ExperimentGroup(Base):
    """Experiment group assignment for A/B testing"""
    __tablename__ = "experiment_groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    group_name = Column(String(20), nullable=False)
    assigned_at = Column(DateTime, server_default=func.now())
