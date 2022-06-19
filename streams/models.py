from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, backref, declarative_base

Model = declarative_base()


class Question(Model):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    body = Column(Text(), nullable=False)
    email = Column(String(120), nullable=False)


class Answer(Model):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    question = relationship('Question', backref=backref('answers', lazy=False))
    body = Column(Text(), nullable=False)
