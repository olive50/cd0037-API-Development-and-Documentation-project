import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:abc@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        # in order to test creat new question
        self.new_question = {
            "question": "What is an Exemple of python micro framwork?",
            "answer": "Flask",
            "category": "1",
            "difficulty": 1
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_categories(self):
        resources = self.client().get('/categories')
        data = json.loads(resources.data)

        self.assertEqual(resources.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(data['categories']), 5)

    def test_retrieve_questions(self):

        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['questions'])
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(len(data['questions']), 10)

        self.assertGreater(data['total_questions'], 15)

        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
        self.assertIsInstance(data['categories'], dict)
        self.assertEqual(data['current_category'], 'All')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
