"""
SQLAlchemy ORM models mirroring the Prisma schema (read-only from FastAPI side,
except for embedding writes).
"""

import enum

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
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
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import DeclarativeBase, relationship


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


class Problem(Base):
    __tablename__ = "problems"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum(Difficulty, name="Difficulty", schema="public"), nullable=False, default=Difficulty.MEDIUM)
    course_id = Column("courseId", UUID(as_uuid=True), ForeignKey("courses.id"), nullable=True)
    tags = Column(ARRAY(String), default=[])
    created_at = Column("createdAt", DateTime, server_default=func.now())
    updated_at = Column("updatedAt", DateTime, server_default=func.now(), onupdate=func.now())

    submissions = relationship("Submission", back_populates="problem")
    embedding = relationship("ProblemEmbedding", back_populates="problem", uselist=False)


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
