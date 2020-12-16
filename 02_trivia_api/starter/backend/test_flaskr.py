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
        #self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'moknine2020','localhost:5432', self.database_name)
        self.database_path = os.environ['DATABASE_TEST_PATH']
		setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE 
    Write at least one test for each test for successful operation and for expected errors.
    """
    # test for get request ('/categories') end point
    def test_get_categories(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        

    def test__not_get_categories(self):
        res=self.client().get('/categories1')
        
        self.assertEqual(res.status_code,404)

 # test for get request ('/questions') end point
    def test_get_questions(self):
        res=self.client().get('/questions?page=1')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['message'],'OK')

    def test__not_get_questions(self):
        res=self.client().get('/questions?page=100')
        
        self.assertEqual(res.status_code,404)
     
# test for get request ('/categories/<int:id>/questions') end point
    def test_get_questions_cat(self):
        res=self.client().get('/categories/2/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['message'],'OK')
        self.assertEqual(data['currentCategory'],2)

    def test__not_get_questions_cat(self):
        res=self.client().get('/categories/100/questions')
        self.assertEqual(res.status_code,404)   
        res=self.client().get('/categories/0/questions')
        self.assertEqual(res.status_code,422)   

# test for delete request ('/questions/<int:id>') end point
    def test_del_questions(self):
        id=Question.query.first().id
        print('ID is :',id)
        res=self.client().delete('/questions/{}'.format(id))
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['message'],'OK')
        

    def test__not_del_questions(self):
        res=self.client().get('/questions/100000')
        self.assertEqual(res.status_code,405)   
        res=self.client().get('/questions/0')
        self.assertEqual(res.status_code,405)   
        
# test for POST request ('/newquestions') end point
    def test_add_questions(self):
        res=self.client().post('/newquestions',json={"question":"quel_est_votre_nom?","answer":"Zakhama_Yosri","category":"1","difficulty":"2"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['message'],'question inserted')
        

    def test__not_add_questions(self):
        res=self.client().post('/newquestions',json={"question":"quel_est_votre_nom?","answer":"Zakhama_Yosri","category":"h","difficulty":"2"})
        self.assertEqual(res.status_code,500)   
        res=self.client().post('/newquestions',json={"question":"quel_est_votre_nom?","answer":"Zakhama_Yosri","category":"2","difficulty":"hard"})
        self.assertEqual(res.status_code,500)   
        res=self.client().post('/newquestions',json={"answer":"Zakhama_Yosri","category":"2","difficulty":"1"})
        self.assertEqual(res.status_code,400)   
        
# test for POST request ('/questions') end point
    def test_search_questions(self):
        res=self.client().post('/questions',json={"searchTerm":""})
        data=json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'],'OK')
        

    def test__not_search_questions(self):
        res=self.client().post('/questions',json={"searchTerm":"*?-?*"})
        data=json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found!')

# test for POST request ('/quizzes') end point
    def test_quizzes(self):
        res=self.client().post('/quizzes',json={"quiz_category":{"id":5,"type":"History"},"previous_questions":[5]})
        data=json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'],'OK')
        

    def test__not_quizzes(self):
        res=self.client().post('/quizzes',json={"quiz_category":{"id":1500,"type":"History"},"previous_questions":[5]})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)   
        self.assertEqual(data['message'],'Not Found!')
        
        res=self.client().post('/quizzes',json={"quiz_category":{"id":5,"type":"anythink"},"previous_questions":[5]})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)   
        self.assertEqual(data['message'],'Not Found!')
        
        res=self.client().post('/quizzes',json={"quiz_categor":{"id":15,"type":"History"},"previous_questions":[5]})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,400)   
        self.assertEqual(data['message'],'Bad request')
        
    def test_add_category(self):
        res=self.client().post('/newcategories',json={"category":"Films"})
        data=json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'],'OK')
        

    def test__not_add_category(self):
        res=self.client().post('/newcategories')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,500)   
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()