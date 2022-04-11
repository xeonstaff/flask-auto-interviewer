from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import Question, db, Question, question_schema, questions_schema

api = Blueprint('api', __name__, url_prefix='/api')

site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/')
def home():
    return render_template('index.html')


@site.route('/profile')
def profile():
    return render_template('profile.html')


@api.route('/questions', methods=['POST'])
@token_required
def create_question(current_user_token):
    question = request.json['question']
    answer = request.json['answer']
    token = current_user_token.token

    print(f'Question created for {current_user_token.token}')

    question = Question(question, answer, user_token=user_token)

    db.session.add(question)
    db.session.commit()

    response = question_schema.dump(question)
    return jsonify(response)
