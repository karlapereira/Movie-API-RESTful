# Movie-API-RESTful
> API REST of movies using Flask

## Modules

- [Python](https://www.python.org/downloads/) - Programming Language,
- Flask - The framework used,
- Marshmellow - ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes,
- SQLite - Relational database management system (RDBMS),
- Blueprint - A template for generating a view of api for docummentation and tests,
- Pip - Dependency Management.

## Virtual environments (Linux)
- install [Python](https://www.python.org/downloads/)
```
$ sudo apt-get install python-virtualenv
$ python3 -m venv venv
$ . venv/bin/activate
```
Install all project dependencies using:
```
$ pip install -r requirements.txt
```
## Virtual environments (Windows)
- install [Python](https://www.python.org/downloads/)
```
$ pip install virtualenv
$ python -m venv venv
$ . venv\Scripts\Activate.ps1
```
Install all project dependencies using:
```
$ pip install -r requirements.txt
```
## Runing

```
$ python run.py
```
# Runing with Docker Container
## commands docker
```
docker build --tag docker-api-movie .   
docker run -p 5000:5000 -d docker-api-movie   
```

# Router API

## - Server 
port=5000 \
host=0.0.0.0 (localhost) 

## - Docs
url = {HOST}:{PORT}/api/docs

## - Movies
url = {HOST}:{PORT}/api/movies

[Method POST] - Load a file.csv into database

Require: form-data with key "database_csv"

[Method GET] - With query_param "producers_range_winner" = True

Description: Return min and max range intervals of movie producers
```
{
    "min": [
        {
            "previousWin": 1984,
            "interval": 6,
            "producer": "Bo Derek",
            "followingWin": 1990
        }
    ],
    "max": [
        {
            "previousWin": 1984,
            "interval": 6,
            "producer": "Bo Derek",
            "followingWin": 1990
        }
    ]
}
```

[Method GET] - Return all movies in database
```
{
    "movies": [
        {
            "year": 1980,
            "title": "Can't Stop the Music",
            "studios": "Associated Film Distribution",
            "producers": "Allan Carr",
            "winner": "yes"
        },
        {
            "year": 1980,
            "title": "Cruising",
            "studios": "Lorimar Productions, United Artists",
            "producers": "Jerry Weintraub",
            "winner": null
        },
        {
            "year": 1980,
            "title": "The Formula",
            "studios": "MGM, United Artists",
            "producers": "Steve Shagan",
            "winner": null
        }
}
```
