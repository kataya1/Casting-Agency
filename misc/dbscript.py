from random import randrange, choice

def populate_movies(x,y):
    for i in range(x,y):
        json = f'{{"title": "movie{i}",   "release_date": "{randrange(1900,2020)}-{randrange(1,12)}-{randrange(1,28)}"}}'
        print(f"curl --location --request POST 'localhost:8080/movies' --header 'Content-Type: application/json' --data-raw '{json}'")

def populate_actors(x,y):
        for i in range(x,y):
            json = f'{{"name": "Actor{i}",   "DOB": "{randrange(1900,2020)}-{randrange(1,12)}-{randrange(1,28)}", "gender": "{choice(["male", "female", "other"])}"}}'
            print(f"curl --location --request POST 'localhost:8080/actors' --header 'Content-Type: application/json' --data-raw '{json}'")
populate_actors(1,100)