#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

# Import models (assuming models.py has db, Article, and User defined)
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize database migration support
migrate = Migrate(app, db)

# Bind the database to the app
db.init_app(app)

@app.route('/clear')
def clear_session():
    # Reset the session page_views counter to 0
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    # Retrieve all articles from the database
    articles = Article.query.all()
    # Serialize the articles data
    articles_data = [article.to_dict() for article in articles]
    # Return the articles data as JSON
    return jsonify(articles_data), 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views to 0 if it doesn't exist
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views by 1 for each request to this endpoint
    session['page_views'] += 1

    # Check if the user has viewed more than 3 articles
    if session['page_views'] > 3:
        # If the limit is reached, return an error message and a 401 status code
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Retrieve the article by ID from the database
    article = Article.query.get(id)
    
    # If the article is not found, return a 404 error
    if not article:
        return jsonify({'message': 'Article not found'}), 404
    
    # Return the article data as JSON
    return jsonify(article.to_dict()), 200

if __name__ == '__main__':
    app.run(port=5555)
