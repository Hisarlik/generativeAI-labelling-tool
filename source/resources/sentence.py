from flask import render_template, request,redirect, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
from source.db import db
import random
from source.models.sentences import SentenceModel, ValidationModel
from source.schemas import SentenceSchema, SentenceUpdateSchema

sentblueprint = Blueprint("Sentences", "sentences",
                          description="CRUD oraciones")


@sentblueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('another_sentence') == 'another':
            sentence = db.session.query(SentenceModel).order_by(func.random()).first()
            return redirect("/sent/"+str(sentence.sentence_id))
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")




@sentblueprint.route('/sent/<string:sent_id>',methods=['GET', 'POST'])
def get_sentences(sent_id):
    if request.method == 'POST':
        # Retrieve the text from the textarea
        sentence_manual = request.form.get('sentence_manual')
        valid = request.form.get('valid')
        validation_data = dict(sentence_manual=sentence_manual, sentence_id=sent_id)
        validation = ValidationModel(**validation_data)
        result = db.session.query(ValidationModel).filter(ValidationModel.sentence_id == sent_id)
        print("res",result)
        for row in result:
            if row:
                abort(500, message="La simplificación de esta oración ya existe")

        try:
            db.session.add(validation)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating a validation.")

        sentence = db.session.query(SentenceModel).get(sent_id)
        sentence.valid = bool(valid)
        db.session.commit()

        return render_template('index.html')
    sentence = SentenceModel.query.get_or_404(sent_id)
    return render_template('sentence_validation.html', sentence=sentence)



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
            sentence.valid = sent_data["valid"]
        else:
            sentence = SentenceModel(sentence_id=sent_id, **sent_data)

        db.session.add(sentence)
        db.session.commit()

        return


@sentblueprint.route('/sentences')
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