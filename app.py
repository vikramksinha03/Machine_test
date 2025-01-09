from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:letsdoit143*@localhost:5433/movie_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def get_db_connection():
    connection = psycopg2.connect(
        host='localhost',
        port=5433, 
        database='movie_database',
        user='postgres',
        password='letsdoit143*'
    )
    return connection

# Define Models
class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    nconst = db.Column(db.String(20), nullable=False)
    primaryName = db.Column(db.String(100), nullable=False)
    birthYear = db.Column(db.Integer)
    deathYear = db.Column(db.Integer)
    primaryProfession = db.Column(db.String(200))
    knownForTitles = db.Column(db.String(200))

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    tconst = db.Column(db.String(20), nullable=False)
    titleType = db.Column(db.String(50), nullable=False)
    primaryTitle = db.Column(db.String(200), nullable=False)
    isAdult = db.Column(db.Boolean, nullable=False)
    startYear = db.Column(db.Integer)
    endYear = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.String(100))

# API Endpoint: Search for Movies
@app.route('/api/movies/search', methods=['GET'])
def search_movies():
    filters = []
    params = []

    year = request.args.get('year')
    genre = request.args.get('genre')
    person_name = request.args.get('person_name')
    movie_type = request.args.get('type')

    query = """
    SELECT "primaryTitle" AS title, "startYear" AS year_released, "titleType" AS type, genres
    FROM "Movie"
    WHERE 1=1
    """

    if year:
        query += " AND \"startYear\" = %s"
        params.append(year)
    if genre:
        query += " AND genres ILIKE %s"
        params.append(f'%{genre}%')
    if movie_type:
        query += " AND \"titleType\" = %s"
        params.append(movie_type)

    # Joining Person table if person_name is provided
    if person_name:
        query = f"""
        SELECT m."primaryTitle" AS title, m."startYear" AS year_released, m."titleType" AS type, m.genres
        FROM "Movie" m
        JOIN "Person" p ON m."tconst" = ANY(string_to_array(p."knownForTitles", ','))
        WHERE p."primaryName" ILIKE %s
        """ + query[len("SELECT m.\"primaryTitle\" AS title, m.\"startYear\" AS year_released, m.\"titleType\" AS type, m.genres FROM \"Movie\" m"):]
        params.insert(0, f'%{person_name}%')

    try:
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return jsonify([{
            'Title': row[0],
            'Year Released': row[1],
            'Type': row[2],
            'Genre': row[3]
        } for row in results]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Endpoint: Search for People
@app.route('/api/persons/search', methods=['GET'])
def search_persons():
    filters = []
    params = []

    movie_title = request.args.get('movie_title')
    name = request.args.get('name')
    profession = request.args.get('profession')

    query = """
    SELECT "primaryName" AS name, "birthYear" AS birth_year, "primaryProfession" AS profession, "knownForTitles"
    FROM "Person"
    WHERE 1=1
    """

    if movie_title:
        query += " AND \"knownForTitles\" ILIKE %s"
        params.append(f'%{movie_title}%')
    if name:
        query += " AND \"primaryName\" ILIKE %s"
        params.append(f'%{name}%')
    if profession:
        query += " AND \"primaryProfession\" ILIKE %s"
        params.append(f'%{profession}%')

    try:
        db_connection = get_db_connection()
        cursor = db_connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return jsonify([{
            'Name': row[0],
            'Birth Year': row[1],
            'Profession': row[2],
            'Known for Titles': row[3]
        } for row in results]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
