
from flask import Flask, request, abort, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import randrange as rg

from models import setup_db, Question, Category
from flask_cors.decorator import cross_origin

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the DONEs
  '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    '''
  @DONE:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    @cross_origin()
    def get_categories():
        try:
            categories = Category.query.all()
            list_categories = {
                category.id: category.type for category in categories}
        except BaseException:
            abort(400)
        return jsonify({
            "success": True,
            "code": 200,
            "massage": "OK",
            "categories": list_categories,
            "nbr_categories": len(list_categories)
        })

    '''
  @DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions', methods=['GET', 'POST'])
    @cross_origin()
    def get_questions():
        if request.method == 'GET':
            page = int(request.args.get('page'))
            list_questions = Question.query.all()
            if page < 1 or page > 1 + \
                    len(list_questions) // QUESTIONS_PER_PAGE:  # case where page is not found
                abort(404)
            questions = [q.format() for q in list_questions]
            questions = questions[(page - 1) *
                                  QUESTIONS_PER_PAGE:page * QUESTIONS_PER_PAGE]
            result_categories = json.loads(get_categories().data)
            return jsonify({
                'questions': questions,
                'totalQuestions': len(list_questions),
                'categories': result_categories['categories'],
                'currentCategory': questions[0]['category'],
                'success': True,
                'code': 200,
                'message': 'OK'
            })
        elif request.method == 'POST':
            data = request.get_json()
            search_term = data.get('searchTerm')
            questions = Question.query.filter(
                Question.question.ilike(
                    "%" + search_term + "%")).all()
            if questions == []:
                abort(404)
            questions_to_send = [q.format() for q in questions]
            return jsonify({
                'questions': questions_to_send,
                'totalQuestions': len(questions_to_send),
                'currentCategory': questions_to_send[0]['category'],
                'success': True,
                'code': 200,
                'message': 'OK'
            })
        else:
            abort(405)
    '''
  @DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    @cross_origin()
    def delete_questions(id):
        try:
            question = Question.query.get(id)
            if question is None:
                abort(404)
            id = question.id
            question.delete()
        except BaseException:
            abort(405)
        list_questions = Question.query.all()
        questions = [q.format() for q in list_questions]
        return jsonify({
            "success": True,
            "code": 200,
            "message": "OK",
            "categories": questions,
            "id": id

        })

    '''
  @DONE:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/newquestions', methods=['POST'])
    @cross_origin()
    def add_question():
        data = request.get_json()
        if 'question' in data.keys() and 'answer' in data.keys(
        ) and 'category' in data.keys() and 'difficulty' in data.keys():
            question = Question(
                data['question'],
                data['answer'],
                data['category'],
                data['difficulty'])
            question.insert()
        else:
            abort(400)

        return jsonify({
            'success': True,
            'code': 200,
            'message': 'question inserted'})
    '''
  @DONE:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    '''
  @DONE:
  Create a GET endpoint to get questions based on category. `/categories/${id}/questions`

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    @cross_origin()
    def get_questions_by_category(id):
        NBR_CATEGORIES = len(Category.query.all())
        if id > NBR_CATEGORIES:
            abort(404)
        if id < 1:
            abort(422)
        list_questions = Question.query.filter(Question.category == id).all()

        if list_questions is None:  # case where page is not found
            abort(404)
        questions = [q.format() for q in list_questions]
        return jsonify({
            'questions': questions,
            'totalQuestions': len(list_questions),
            'currentCategory': questions[0]['category'],
            'success': True,
            'code': 200,
            'message': 'OK'
        })

    '''
  @DONE:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    @cross_origin()
    def get_question_quizz():
        categories = Category.query.all()
        id_categories = [c.format()['id'] for c in categories]
        type_categories = [c.format()['type'] for c in categories]
        data = request.get_json()

        if 'quiz_category' not in data.keys() or 'previous_questions' not in data.keys():
            abort(400)
        previous_questions = data.get('previous_questions')
        if data.get('quiz_category')['id'] == 0:

            list_questions = Question.query.all()

        else:
            if int(data.get('quiz_category')['id']) not in id_categories:
                abort(404)
            if data.get('quiz_category')['type'] not in type_categories:
                abort(404)
            list_questions = Question.query.filter(
                Question.category == data.get('quiz_category')['id']).all()
        list_questions = [q.format() for q in list_questions]

        next_questions = []
        for q in list_questions:
            if q['id'] not in previous_questions:
                next_questions.append(q)
        if next_questions != []:
            i = rg(0, len(next_questions))
            currentQuestion = next_questions[i]
        else:
            currentQuestion = None
        return jsonify({
            'success': True,
            'message': 'OK',
            'code': 200,
            'question': currentQuestion,
            'previousQuestions': previous_questions
        })

     # this POST endpoint take category and add new category
    @app.route('/newcategories', methods=['POST'])
    @cross_origin()
    def add_category():
        data = request.get_json()
        cat = data.get('category')
        category = Category(type=cat)
        category.insert()
        categories = category.query.all()
        categories = [c.format() for c in categories]
        return jsonify({
            'success': True,
            'message': 'OK',
            'code': 200,
            'category': category.format(),
            'categories': categories
        })
    '''
  @DONE:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found!'}), 404

    @app.errorhandler(422)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable!'}), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'not alowed'

        }), 405

    @app.errorhandler(500)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Problem in Server crash !'

        }), 500
    return app
