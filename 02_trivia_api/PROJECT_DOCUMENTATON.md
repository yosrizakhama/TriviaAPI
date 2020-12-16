### Full Stack Trivia API Backend

### Getting Started
                
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.
My work is to complete this Trivia App and create an API for this app.

### Installing Dependencies

#### preference  Python 3.7 but you can use Python 3.8 but in this case you must write this command : pip install werkzeug==0.14.1

### if you have problem with SQLAchemy you can write this command : pip install sqlachemy --update

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)



#### PIP Dependencies

Install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.
if your PYTHON > 3.7 
    pip install werkzeug==0.14.1
    pip install sqlachemy --update

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Running WEB APP
#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```


## Required Tasks

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```


### API Documentation ###

### ERROR Handling ###

1 - Format of error : JSON
    {
        "error": ...,
        "message": ".......",
        "success": false
    }
    2 - List of errors : 400, 404, 405, 422 and 500

            
            ```first end point```

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


request example :
    curl http://127.0.0.1:5000/categories
result :
type : json
{
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "nbr_categories": 6,
  "success": true
}



            ```Second end point```
            
GET '/questions'

  -This endpoint  handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint  return a list of questions, 
  number of total questions, current category, categories. 
  
  -Request argument : page (integer) refer to the number of the page where the user want to show the questions. example : if page=2 the request return questions ordered between 11 and 20
  
  -Return : json object
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": 3,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }],
  "totalQuestions": 19,
  'success':True,
  'code':200,
  'message':'OK'
}

Request example : curl -X GET http://127.0.0.1:5000/questions?page=2 
  
        ```Third end point```
        
   - GET '/categories/id/questions'
    - This endpoint return questions based on category.
    - Request parameter : id of category must be between 1 and 6, otherwise return error 404 if id>6 or 422 if id<1
    - Result : Json Object
    {
      "code": 200,
      "currentCategory": 1,
      "message": "OK",
      "questions": [
        {
          "answer": "The Liver",
          "category": 1,
          "difficulty": 4,
          "id": 20,
          "question": "What is the heaviest organ in the human body?"
        },
        {
          "answer": "Alexander Fleming",
          "category": 1,
          "difficulty": 3,
          "id": 21,
          "question": "Who discovered penicillin?"
        },
        {
          "answer": "Blood",
          "category": 1,
          "difficulty": 4,
          "id": 22,
          "question": "Hematology is a branch of medicine involving the study of what?"
        }
      ],
      "success": true,
      "totalQuestions": 3
  }
  - Request example : curl -X GET http://127.0.0.1:5000/categories/1/questions
  
            ```Forth end point```
            
    - DELETE '/questions/id'
    - This endpoint delete question if exist where question.id = id return all questions if not exist return error message.
    - Request parameter : id
    -Result : Json Object
    {
      "categories": [
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        }
      ],
      "code": 200,
      "message": "OK",
      "success": true
    }
    - Request example : curl -X DELETE http://localhost:5000/questions/2
    
                ```Sixth end point``` 
  
  - POST '/newquestions'
  - this end point POST a new question, which  require the question and answer text, category, and difficulty score.
  - DATA = Json {'question':...,'answer':.....,'category':......,'difficulty':....}
  - example  of request with CURL :
    curl -H "Content-Type: application/json" -X POST -d {\"question\":\"quel_est_votre_nom?\",\"answer\":\"Zakhama_Yosri\",\"category\":\"1\",\"difficulty\":\"2\"} http://127.0.0.1:5000/newquestions
  - Response :
  {
    "code": 200,
    "message": "question inserted",
    "success": true
  }
  
                ``` Seventh EndPoint ```
  - POST '/questions'
  - this endpoint  get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
  - DATA = json {'searchTerm':'.......'}
  - example  of request with CURL :
    curl -H "Content-Type: application/json" -X POST -d {\"searchTerm\":\"title\"} http://127.0.0.1:5000/questions
  - Response :
    {
          "code": 200,
          "currentCategory": 4,
          "message": "OK",
          "questions": 
              [
                {
                  "answer": "Maya Angelou",
                  "category": 4,
                  "difficulty": 2,
                  "id": 5,
                  "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                },
                {
                  "answer": "Edward Scissorhands",
                  "category": 5,
                  "difficulty": 3,
                  "id": 6,
                  "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                }
              ],
            "success": true,
            "totalQuestions": 2
    }   

                        ``` Eight EndPoint ```
    - POST '/quizzes'
    - This EndPoint get questions to play the quiz. It should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
    - Data = json
        example :
        {
            'quiz_category':{'id':'5','type':'History'},
            'previous_questions':[2,6,1]
        }
    - Example request with curl :
        curl -H "Content-Type: application/json" -X POST -d {\"quiz_category\":{\"id\":5,\"type\":\"History\"},\"previous_questions\":[5]} http://127.0.0.1:5000/quizzes
    
    - Response :
        {
          "code": 200,
          "message": "OK",
          "previousQuestions": [
            5
          ],
          "question": {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
          },
          "success": true
        }
        
                    ``` Extra EndPoint ```
                    
    - POST '/newcategories'
    - This EndPoint add a new category
    - Data = {
                'category':'.......'
            }
    - Example request with curl :
        curl -H "Content-Type: application/json" -X POST -d {\"category\":\"Films\"} http://127.0.0.1:5000/newcategories
    
    - response : json
    {
        'success':True,
        'message':'OK',
        'code':200,
        'category':{category},
        'categories':[{category1},....]
        
    }
    {
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    },
        {
      "id": 7,
      "type": "Films"
    }
  ],
  "category": {
    "id": 7,
    "type": "Films"
  },
  "code": 200,
  "message": "OK",
  "success": true
}
    


## Testing
To run the tests, run
```
1 - Dropdb trivia_test
2 - Createdb trivia_test and psql trivia_test < trivia.psql
    or
        open psql and after that:
        Dropdb trivia_test,write this request CREATEdb trivia_test WITH TEMPLATE=trivia;
3 - python test_flaskr.py
```