from source.db import db


class SentenceModel(db.Model):
    __tablename__ = "sentences"

    sentence_id = db.Column(db.Integer, primary_key=True)
    sentence_original = db.Column(db.String(500), unique=True, nullable=False)
    sentence_simplified = db.Column(db.String(500), unique=True, nullable=False)
    document_name = db.Column(db.String(100), unique=True, nullable=False)
    document_sentence_id = db.Column(db.Integer, nullable=True)

    def __init__(self, sentence_original,
                 sentence_simplified,
                 document_name,
                 document_sentence_id, sentence_id=None):
        if sentence_id:
            self.sentence_id = sentence_id
        self.sentence_original = sentence_original
        self.sentence_simplified = sentence_simplified
        self.document_name = document_name
        self.document_sentence_id = document_sentence_id
