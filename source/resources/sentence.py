from flask import render_template, request,redirect, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
from source.db import db
from source.models.sentences import LoginForm, User, RegisterationForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
from werkzeug.security import generate_password_hash, check_password_hash

from source.models.sentences import SentenceModel, ValidationModel, WordModel
from source.schemas import SentenceSchema, SentenceUpdateSchema

sentblueprint = Blueprint("Sentences", "sentences",
                          description="CRUD oraciones")


@sentblueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('another_sentence') == 'Comenzar':
            results = db.session.scalars(db.session.query(ValidationModel.sentence_id)).all()
            print(results)
            sentence = db.session.query(SentenceModel).filter(~SentenceModel.sentence_id.in_(results)).order_by(func.random()).first()
            return redirect("/sent/"+str(sentence.sentence_id))
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")

@sentblueprint.route('/login', methods=['GET', 'POST'])
def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('dashboard'))
            return '<h1>Invalid username or password</h1>'
            #return '<h1>' + form.username.data + '' + form.password.data + '</h1>'
        return render_template('login.html', form=form)


login_manager = LoginManager()
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@sentblueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterationForm()
    print(form)
    if form.is_submitted():
        hashed_password = generate_password_hash(form.password.data, method= 'sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New user has been created </h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('signup.html', form=form)

@sentblueprint.route('/sent/<string:sent_id>',methods=['GET', 'POST'])
def get_sentences(sent_id):
    if request.method == 'POST':
        # Retrieve the text from the textarea
        sentence_manual = request.form.get('sentence_manual')
        word_original1 = request.form.get('word_original1')
        word_simple1 = request.form.get('word_simple1')
        word_original2 = request.form.get('word_original2')
        word_simple2 = request.form.get('word_simple2')
        word_original3 = request.form.get('word_original3')
        word_simple3 = request.form.get('word_simple3')
        valid = request.form.get('valid')

        ## Validation object
        validation_data = dict(sentence_manual=sentence_manual, sentence_id=sent_id)
        validation = ValidationModel(**validation_data)



        ## Test if exists
        result = db.session.query(ValidationModel).filter(ValidationModel.sentence_id == sent_id)

        ## Validations
        for row in result:
            if row:
                abort(500, message="La simplificación de esta oración ya existe")

        try:
            db.session.add(validation)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating a validation.")


        ## Words
        if word_original1 or word_original2 or word_original3:
            word_data = dict(word_original1=word_original1,
                             word_simple1=word_simple1,
                             word_original2=word_original2,
                             word_simple2=word_simple2,
                             word_original3=word_original3,
                             word_simple3=word_simple3,
                             sentence_id=sent_id)
            print(word_data)
            word = WordModel(**word_data)

            try:
                db.session.add(word)
                db.session.commit()
            except SQLAlchemyError as e:
                print(e)
                abort(500, message="An error occurred while creating a word synonyms.")


        ## Update valid sentence
        sentence = db.session.query(SentenceModel).get(sent_id)
        sentence.valid = bool(valid)
        db.session.commit()

        results = db.session.scalars(db.session.query(ValidationModel.sentence_id)).all()
        print(results)
        sentence = db.session.query(SentenceModel).filter(~SentenceModel.sentence_id.in_(results)).order_by(
            func.random()).first()
        return redirect("/sent/" + str(sentence.sentence_id))

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