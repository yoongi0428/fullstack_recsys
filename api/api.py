from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin

from recommend.recommender import RecommenderWrapper

wrapper = RecommenderWrapper()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/api/recommend", methods=['POST'])
# @cross_origin()
def recommend():
    data = request.get_json()

    if ('context' not in data or
        len(data['context']) == 0 or 
        'model' not in data):
        abort(400)
    else:
        user_context = data['context']
        model = data['model']

        wrapper.set_model(model)
        result = wrapper.recommend(user_context)

        return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=False)