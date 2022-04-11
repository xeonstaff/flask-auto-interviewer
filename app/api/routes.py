from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Question, question_schema, questions_schema, user_schema, users_schema

api = Blueprint('api', __name__, url_prefix='/api')

# routes for questions/answers


@api.route('/questions', methods=['POST'])
@token_required
def create_question(current_user_token):
    question = request.json['question']
    answer = request.json['answer']
    user_token = current_user_token.token

    print(f'Question made for {current_user_token.token}')

    question = Question(question, answer, user_token=user_token)

    db.session.add(question)
    db.session.commit()

    response = question_schema.dump(question)
    return jsonify(response)


@api.route('/questions', methods=['GET'])
@token_required
def get_question(current_user_token):
    a_user = current_user_token.token
    contacts = Question.query.filter_by(user_token=a_user).all()
    response = questions_schema.dump(contacts)
    return jsonify(response)


@api.route('/questions/<id>', methods=['GET'])
@token_required
def get_single_question(current_user_token, id):
    contact = Question.query.get(id)
    response = question_schema.dump(contact)
    return jsonify(response)


@api.route('/questions/<id>', methods=['POST', 'PUT'])
@token_required
def update_question(current_user_token, id):
    question = Question.query.get(id)
    question.question = request.json['question']
    question.answer = request.json['answer']
    question.user_token = current_user_token.token

    db.session.commit()
    response = question_schema.dump(question)
    return jsonify(response)


@api.route('/questions/<id>', methods=['DELETE'])
@token_required
def delete_question(current_user_token, id):
    question = Question.query.get(id)
    db.session.delete(question)
    db.session.commit()
    response = question_schema.dump(question)
    return jsonify(response)


# routes for profile information
@api.route('/userprofile', methods=['POST'])
@token_required
def create_profile(current_user_token):
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    linkedin = request.json['linkedin']
    other_link_name = request.json['other_link_name']
    other_link = request.json['other_link']
    summary = request.json['summary']
    # token = current_user_token.token

    print('Profile created!')

    user_profile = User(first_name, last_name, linkedin, other_link_name, other_link, summary)
    # token=token
    db.session.add(user_profile)
    db.session.commit()

    response = user_schema.dump(user_profile)
    return jsonify(response)


@api.route('/userprofile', methods=['GET'])
@token_required
def get_userprofile(current_user_token):
    a_user = current_user_token.token
    user_profile = User.query.filter_by(token=a_user).all()
    response = users_schema.dump(user_profile)
    return jsonify(response)


@api.route('/userprofile/<id>', methods=['GET'])
@token_required
def get_single_user_profile(current_user_token, id):
    user_profile = User.query.get(id)
    response = user_schema.dump(user_profile)
    return jsonify(response)


@api.route('/userprofile/<id>', methods=['POST', 'PUT'])
@token_required
def update_profile(current_user_token, id):
    user_profile = User.query.get(id)
    user_profile.linkedin = request.json['linkedin']
    user_profile.other_link_name = request.json['other_link_name']
    user_profile.other_link = request.json['other_link']
    user_profile.summary = request.json['summary']
    user_profile.token = current_user_token.token

    db.session.commit()
    response = user_schema.dump(user_profile)
    return jsonify(response)


@api.route('/userprofile/<id>', methods=['DELETE'])
@token_required
def delete_profile(current_user_token, id):
    user_profile = User.query.get(id)
    db.session.delete(user_profile)
    db.session.commit()
    response = user_schema.dump(user_profile)
    return jsonify(response)
