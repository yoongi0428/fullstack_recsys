import json
from datetime import datetime
from flask.json import jsonify
from flask import request
import requests

from flask import render_template

from app import app, db, manager, migrate
from app.model import User, Movie, Interaction

API_ADDRESS = 'http://0.0.0.0:8000%s'
@app.route('/recommend', methods=['POST'])
def recommend():
	data = request.get_json()
	# res = json.loads(requests.post(API_ADDRESS % '/api/recommend', json={"context": [1, 2, 3, 4], "model": "EASE"}).content)
	res = json.loads(requests.post(API_ADDRESS % '/api/recommend', json=data).content)
	recommend_db_items = [Movie.query.filter_by(id=ids).first() for ids in res['result']]
	recommend_items = [
		{"id": item.id, "title": item.title, "genre": item.genre}
		for item in recommend_db_items
	]
	return {'result': recommend_items}

@app.route('/init', methods=['GET'])
def init():
	all_db_items = Movie.query.all()
	all_items = sorted([
		{"id": item.id, "title": item.title, "genre": item.genre, "date": datetime.strftime(item.date, '%Y-%b-%d')}
		for item in all_db_items
	], key=lambda x: x["id"])
	return {'result': all_items}


@manager.command
def run():
	app.run()

if __name__ == '__main__':
    manager.run()