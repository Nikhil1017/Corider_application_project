from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
api = Api(app)

app.config["MONGO_URI"] = "mongodb+srv://NikhilKrishna:UaUcC7NE1SeP2qJB@cluster0.arkj1sx.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)

class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=str, required=True)
        self.reqparse.add_argument('name', type=str, required=True)
        self.reqparse.add_argument('email', type=str, required=True)
        self.reqparse.add_argument('password', type=str, required=True)
        super(User, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        mongo.db.users.insert_one(args)
        return {'message': 'user resource created successfully!'}, 201

    def get(self):
        users = mongo.db.users.find()
        userlist = []
        for user in users:
            user['_id'] = str(user['_id'])
            userlist.append(user)
        return {'users': userlist}, 200

    def put(self, userid):
        args = self.reqparse.parse_args()
        mongo.db.users.update_one({'_id': ObjectId(userid)}, {'$set': args})
        return {'message': 'user details updated'}, 200

    def delete(self, userid):
        mongo.db.users.delete_one({'_id': ObjectId(userid)})
        return {'message': 'user has been deleted successfully'}, 200
    
api.add_resource(User, '/users', '/users/<userid>')  

if __name__ == '__main__':
    app.run(debug=True)