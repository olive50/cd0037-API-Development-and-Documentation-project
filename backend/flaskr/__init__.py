import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


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

    @app.route('/questions', methods=['POST'])
    def add_question():
        """
        Endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear at the end of the last page
        of the questions list in the "List" tab.
        """
        body = request.json
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        search_term = body.get('searchTerm', None)

        if search_term:
            search_question(search_term)
        else:
            if (question.strip() == "") or (answer.strip() == ""):
                # no content , do not create empty question
                abort(400)

            try:
                new_question = Question(question, answer, category, difficulty)
                new_question.insert()
            except:
                # Issue creating new question?  422 means understood the request but couldn't do it
                abort(422)

            return jsonify({
                "success": True,
                "added": new_question.id
            })

    def search_question(search_term):
        try:
            # Search the term
            questions = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(search_term)))
            questions_formatted = [question.format() for question in questions]

            return jsonify({
                "success": True,
                "questions": questions_formatted
            })
        except Exception:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

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

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
