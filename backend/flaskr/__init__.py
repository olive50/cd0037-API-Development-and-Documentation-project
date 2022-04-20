import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_resources(request, selection, item_per_page):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * item_per_page
    end = start + item_per_page

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories")
    def retrieve_categories():
        '''
        Handle GET requests
        for all available categories.
        '''
        categories = Category.query.order_by(Category.id).all()
        dict_categories = {
            category.id: category.type for category in categories}
        print(dict_categories)
        if len(dict_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': dict_categories})

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def retrieve_questions():
        '''
        Handle GET requests for questions,
        including pagination (every 10 questions).
        '''
        try:

            page = request.args.get('page', 1, type=int)
            # paginate(page=None, per_page=None, error_out=True, max_per_page=None)¶
            questions = Question.query.order_by(Question.id).paginate(
                page=page, per_page=QUESTIONS_PER_PAGE, error_out=True)
            categories = Category.query.order_by(Category.id).all()

            questions_cleaned = [question.format()
                                 for question in questions.items]
            categories_cleaned = {
                category.id: category.type for category in categories}

            if len(questions_cleaned) == 0:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'questions': questions_cleaned,
                    'total_questions': questions.total,
                    'categories': categories_cleaned,
                    'current_category': 'All',
                })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questtion(question_id):
        """DELETE question using a question ID.

        Keyword arguments:
        question_id -- id fo question to delete
        Return: json object
        """
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify(
                {
                    "success": True,
                    'deleted': question_id
                }
            )

        except:
            abort(422)

    # add or search question

    @app.route('/questions', methods=['POST'])
    def add_question():
        '''Endpoint create a new questions, or search  by word if the body of the request
         contain a value for the searshTerm key.

        '''
        body = request.get_json()

        if "searchTerm" in body:
            term_to_searsh = body['searchTerm'].strip()
            found_questions = Question.query.filter(Question.question.ilike(
                f'%{term_to_searsh}%')).all()
            cleaned_questions = [question.format()
                                 for question in found_questions]

            return jsonify({
                "success": True,
                "questions": cleaned_questions
            })

        else:  # else if the body dont contain searshTerm
            if (body['question'].strip() == "") or (body['answer'].strip() == ""):
                abort(400)
            try:
                new_question = Question(question=body['question'].strip(), answer=body['answer'].strip(),
                                        category=body['category'], difficulty=body['difficulty'])
                new_question.insert()
            except:
                abort(422)
            return jsonify({
                "success": True,
                "added": new_question.id
            })

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        '''
            GET endpoint to get questions based on category.
        '''
        selection = Question.query.filter_by(category=str(category_id)).all()

        questions_list = paginate_resources(
            request, selection, QUESTIONS_PER_PAGE)

        if len(questions_list) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions_list,
            'total_questions': len(selection),
            'categories': Category.query.get(category_id).format(),
            'current_category': category_id
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """endpoint. to get questions to play the quiz

        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
        """

        data = request.json
        try:
            request_category = data['quiz_category']['id']
        except:
            abort(400)

        if request_category == 0:
            questions_quiz = Question.query.all()
        else:
            questions_quiz = Question.query.filter_by(
                category=str(request_category)).all()

        questions = [question.format() for question in questions_quiz]
        try:
            prev_questions = data['previous_questions']
        except:
            abort(400)
        pruned_questions = []
        for question in questions:
            if question['id'] not in prev_questions:
                pruned_questions.append(question)
        if len(pruned_questions) == 0:
            return jsonify({
                'success': True
            })
        question = random.choice(pruned_questions)
        return jsonify({
            'success': True,
            'question': question
        })

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found verify your url"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify(error=str(error)), 500

    return app
