from marshmallow import Schema, fields

class SentenceSchema(Schema):
    sentence_id = fields.Str(dump_only=True)
    sentence_original = fields.Str(required=True)
    sentence_simplified = fields.Str(required=True)
    document_name = fields.Str()
    document_sentence_id = fields.Int()

class SentenceUpdateSchema(Schema):
    sentence_original = fields.Str()
    sentence_simplified = fields.Str()
    document_name = fields.Str()
    document_sentence_id = fields.Int()