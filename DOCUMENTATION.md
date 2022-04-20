# Full Stack Trivia

The Project is realised as an execise in the Udacity course "Full stack web devloper"

## Getting Started

Project is divided into two part `frontend` and `backend`.

### Backend

The `./backend` directory contains a  Flask and SQLAlchemy server. 

### Frontend

The `./frontend` directory contains a  React frontend  app.

### Database

- PostgresSQL

## Installation

it is recomanded to start with start with the backend.

**Backend**
Creating db and populating data.

we supose tha postgresql is installed and running.

```bash
# Creating db
createdb trivia

cd backend/

# Populating database with tables and related data
psql trivia < trivia.psql
```

```bash
# Creating virtual environment
virtualenv venv

# Activating virtual environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Start your project in development mode

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

# if you are using windows and power shell

$env:FLASK_APP="flaskr" 
$env:FLASK_ENV="development"
python -m flask run

```

## API Documentation

### Endpoints

**/categories** [GET]

GET '/categories'

Fetches a dictionary of categories in which the keys are the ids and the value is the name of the category
Request Arguments: None

```bash

{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

**/questions?page=1** [GET]

return 10  questions per page

**'/questions', methods=['POST']**
 create question or search for questions

**/questions/\<int:question_id\>** method  [DELETE]

delete a quuestion by id.

# Acknowledgments:

All my thanks for UDACITY Staf, and the teachers of the full stack devloper course.


