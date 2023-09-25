from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
class Simplification(Base):
    __tablename__ = "simplification"
    instance_id = Column(Integer, primary_key=True)
    original_sentence = Column(String)
    model_simplification_sentence = Column(String)
    document_sentence_id = Column(Integer)
    document_name = Column(Integer)
    length_sentence = Column(Integer)

    def __init__(self, original_sentence,
                 model_simplification_sentence,
                 document_sentence_id,
                 document_name,
                 length_sentence):

        self.original_sentence = original_sentence
        self.model_simplification_sentence = model_simplification_sentence
        self.document_sentence_id = document_sentence_id
        self.document_name = document_name
        self.length_sentence = length_sentence

    def __repr__(self):
        return f'Simplification({self.original_sentence}, {self.document_sentence_id}, {self.document_name})'

    def __str__(self):
        return self.original_sentence
