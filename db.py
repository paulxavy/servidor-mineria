from urllib import request, response
from flask import Flask, request , jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

#app.secret_key = 'myawesomesecretkey'

if __name__ == "__main__":
    app.run(debug=True, port=3000)

app.config['MONGO_URI'] = 'mongodb+srv://paulxavy:ZrQvS!s_qzNqmt4@cluster0.usce4v6.mongodb.net/Corrector?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/words', methods=['POST'])
def create_word():
    # Receiving Data
    palabra_correcta = request.json['palabra_correcta']
    palabra_incorrecta = request.json['palabra_incorrecta']
    
    if  palabra_incorrecta and palabra_correcta:
        id = mongo.db.words.insert_one(
            {'palabra_incorrecta' : palabra_incorrecta, 'palabra_correcta' : palabra_correcta }
        )
        response = {
            'id': str(id),
            'palabra_incorrecta' : palabra_incorrecta,
            'palabra_correcta' : palabra_correcta            
        }
        return response
    else:
        {'message' : 'received'}
    return {'message' : 'received'}

@app.route('/words', methods=['GET'])
def get_words():
    #words = mongo.db.words.find()
    #response = json_util.dumps(words)
    return {'message':'recived'}#Response(response, mimetype="application/json")

@app.route('/words/<id>', methods=['GET'])
def get_word(id):
    print(id)
    word = mongo.db.words.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(word)
    return Response(response, mimetype="application/json")


@app.route('/words/<id>', methods=['DELETE'])
def delete_words(id):
    mongo.db.words.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Word' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route('/words/<_id>', methods=['PUT'])
def update_word(_id):
    palabra_correcta = request.json['palabra_correcta']
    palabra_incorrecta = request.json['palabra_incorrecta']
    if palabra_incorrecta and palabra_correcta and _id:
        mongo.db.words.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'palabra_incorrecta': palabra_incorrecta, 'palabra_correcta': palabra_correcta}})
        response = jsonify({'message': 'Word' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


