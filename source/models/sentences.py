from source.db import db

class SentenceModel(db.Model):
    __tablename__ = "sentences"

    sentence_id = db.Column(db.Integer, primary_key=True)
    sentence_original = db.Column(db.String(500), unique=False, nullable=False)
    sentence_simplified = db.Column(db.String(500), unique=False, nullable=False)
    document_name = db.Column(db.String(100), unique=False, nullable=False)
    document_sentence_id = db.Column(db.Integer, nullable=True)
    valid = db.Column(db.Boolean, default=True)
    validations = db.relationship('ValidationModel', backref=db.backref('sentences'))

    def __init__(self, sentence_original,
                 sentence_simplified,
                 document_name,
                 document_sentence_id, sentence_id=None, valid=True):
        if sentence_id:
            self.sentence_id = sentence_id
        self.sentence_original = sentence_original
        self.sentence_simplified = sentence_simplified
        self.document_name = document_name
        self.document_sentence_id = document_sentence_id
        self.valid = valid


class ValidationModel(db.Model):
    __tablename__ = "validations"

    validation_id = db.Column(db.Integer, primary_key=True)
    sentence_manual = db.Column(db.String(500), unique=False, nullable=False)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentences.sentence_id'))

    def __init__(self, sentence_manual,
                 sentence_id, validation_id=None):
        if validation_id:
            self.validation_id = validation_id
        self.sentence_manual = sentence_manual
        self.sentence_id = sentence_id

