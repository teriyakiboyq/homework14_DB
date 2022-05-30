import sqlite3
from flask import Flask, jsonify
from func import db_connect

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True


@app.route('/movie/<title>')
def search_by(title):
    query = f"""
            SELECT title, country, release_year, listed_in AS genre, description
            FROM netflix
            WHERE title = '{title}'
            ORDER BY release_year DESC 
            LIMIT 1 
    """
    response = db_connect(query)[0]
    response_json = {
        'title': response[0],
        'country': response[1],
        'release_year': response[2],
        'genre': response[3],
        'description': response[4]
    }
    return jsonify(response_json)


@app.route('/movie/<int:start>/to/<int:end>')
def search_by_period(start, end):
    query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {start} AND {end}
            ORDER BY release_year 
            LIMIT 100
    """
    response = db_connect(query)
    response_json = []
    for film in response:
        response_json.append({
            'title': film[0],
            'release_year': film[1]

        })
    return jsonify(response_json)


@app.route('/rating/<group>')
def search_by_group(group):
    order = {
        'children': ['G'],
        'family': ['G', 'PG', 'PG-13'],
        'adult': ['R', 'NC-17']
    }
    if group in order:
        group_object = '\", \"'.join(order[group])
        group_object = f'\"{group_object}\"'
    else:
        return jsonify([])

    query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN ({group_object})
    """
    response = db_connect(query)
    response_json = []
    for rating in response:
        response_json.append({
            'title': rating[0],
            'rating': rating[1],
            'description': rating[2]

        })
    return jsonify(response_json)


@app.route('/genre/<genre>')
def search_by_genre(genre):
    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC 
            LIMIT 10
    """
    response = db_connect(query)
    response_json = []
    for film in response:
        response_json.append({
            'title': film[0],
            'description': film[1]
        })
    return jsonify(response_json)


def actors_game(first_act, second_act):
    query = f"""
            SELECT "cast"
            FROM netflix
            WHERE "cast" LIKE '%{first_act}%'
            AND "cast" LIKE '%{second_act}%'
    """
    response = db_connect(query)
    actors = []
    for cast in response:
        actors.extend(cast[0].split(', '))
    result = []
    for a in actors:
        if a not in [first_act, second_act]:
            if actors.count(a) > 2:
                result.append(a)
    result = set(result)
    return result


def tv_name(type_tv, year, genre):
    query = f"""
            SELECT title, description
            FROM netflix
            WHERE "type" = '{type_tv}'
            AND release_year = '{year}'
            AND listed_in LIKE '%{genre}%'
    """
    response = db_connect(query)
    movie = []
    for film in response:
        movie.append({
            'title': film[0],
            'description': film[1]
        })
    return movie


print(tv_name('Movie', '2010', 'Dramas'))

app.run(debug=True)
