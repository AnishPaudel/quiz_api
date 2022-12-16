# Quiz Api
## Create ,Submit and evaluate your quiz


Quiz Api is made with the help of Django and Django restframework.

> The test mock JSON are placed under folder
> test_jsons/



## Features

- create users and staff (who can create questions)
- create quiz and submit answers
- See user stats 

### Api docs
To see the swagger auto generated api documentation runserver. It is the home page.
```sh
python manage.py runserver
```
### Authentication
This app uses token based authentications and divides staffs and user , such that only staff can create,edit questions
for most of the api except create-user requires header Authorization: Token <ur-token>

for token generation use  
```sh
prams: username,password
http://127.0.0.1:8000/api/user/token/
```
> Also change user is_staff from admin at
> http://127.0.0.1:8000/admin

### Quiz
The quiz contains question list which further contain answers. Question can be of two types mulitple or single choice

for creation the payload looks like this:
```sh
{
  "name": "string",
  "discription": "string",
  "questions": [
    {
      "question": "string",
      "is_multi": true,
      "options": [
        {
          "answer": "string",
          "is_answer": true
        }
      ],
      "mark": 0
    }
  ]
}
```
### Answer Submission
The Answer submitted to quiz is validated so that the ids for quiz,options and answer exists in the respective fields.

The request for answer submission looks something like 
```sh
{
  "quiz": 3, # quiz it belongs to
  "answers": [
    {
      "question":2 , #quesiton id
      "options": [
        {
          "std_answer": 2 #student selected id
        }
      ]
    }
  ]
}
```
and the response is evaluated marks of the quiz
```sh
{
  "marks_obtained": 2,
  "correct_answers": 1,
  "incorrect_answers": 0
}
```
User selected data is also returned if neccessary

### User stat
After each answer submission user stats is calculated.
The response looks like 
```sh
[
  {
    "over_all_score": 0,
    "total_score": 0,
    "correct": 0,
    "incorrect": 0
  }
]
```

