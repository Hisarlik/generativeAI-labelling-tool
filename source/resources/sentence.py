from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from source.db import db
from source.models.sentences import SentenceModel
from source.schemas import SentenceSchema, SentenceUpdateSchema

sentblueprint = Blueprint("Sentences", "sentences", description="CRUD oraciones")


@sentblueprint.route("/sentence/<string:sent_id>")
class Sentence(MethodView):
    @sentblueprint.response(200, SentenceSchema)
    def get(self, sent_id):
        return SentenceModel.query.get_or_404(sent_id)


    def delete(self, sent_id):
        emp = SentenceModel.query.get_or_404(sent_id)
        db.session.delete(emp)
        db.session.commit()
        return {"message": "Sentence deleted."}

    @sentblueprint.arguments(SentenceUpdateSchema)
    @sentblueprint.response(200, SentenceSchema)
    def put(self, sent_data, sent_id):
        sentence = SentenceModel.query.get(sent_id)

        if sentence:
            sentence.sentence_original = sent_data["sentence_original"]
            sentence.sentence_simplified = sent_data["sentence_simplified"]
            sentence.document_name = sent_data["document_name"]
            sentence.document_sentence_id = sent_data["document_sentence_id"]
        else:
            sentence = SentenceModel(sentence_id=sent_id, **sent_data)

        db.session.add(sentence)
        db.session.commit()

        return


@sentblueprint.route("/sentences")
class GetSentences(MethodView):
    @sentblueprint.response(200, SentenceSchema(many=True))
    def get(self):
        return SentenceModel.query.all()


@sentblueprint.route("/sentence")
class CreateSent(MethodView):
    @sentblueprint.arguments(SentenceSchema)
    @sentblueprint.response(201, SentenceSchema)
    def post(self, sent_data):
        sentence = SentenceModel(**sent_data)
        try:
            db.session.add(sentence)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating a sentence.")

        return