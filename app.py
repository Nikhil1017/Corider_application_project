from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify, request, json
from bson import ObjectId, json_util


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://NikhilKrishna:UaUcC7NE1SeP2qJB@cluster0.arkj1sx.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def user_resource():
    id = request.json['id']
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    mongo.db.users.insert_one({'id': id,'name': name, 'email': email, 'password': password})
    return jsonify({'message': 'user resource created successfully!'})

@app.route('/users')
def all_users():
    users = mongo.db.users.find()
    userlist = []
    for user in users:
        user['_id'] = str(user['_id'])
        userlist.append(user)
    return {'users': userlist}

@app.route('/users/<userid>', methods=['GET'])
def userinfo(userid):
    user = mongo.db.users.find_one({'_id':ObjectId(userid)})
    return jsonify(json.loads(json_util.dumps(user)))


@app.route('/users/<userid>', methods=['PUT'])
def update(userid):
    id = request.json['id']
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    mongo.db.users.update_one({'_id': ObjectId(userid)}, {'$set':{'id': id,'name': name, 'email': email, 'password': password}})
    return jsonify({'message': 'user details updated'})

@app.route('/users/<userid>', methods=['DELETE'])
def delete (userid):
   mongo.db.users.delete_one({'_id': ObjectId(userid)})
   return jsonify({'message': 'user has been deleted successfully'})
       

if __name__ == '__main__':
    app.run(debug=True)
