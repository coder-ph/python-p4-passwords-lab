#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    
    def get(self):
        user_id = session.get('user_id')
        
        if not user_id:
            return {'message': "401: Not authorized, log in"}, 401
        
        user = User.query.get(user_id)
        if not user:
            return {'message': '404: user not found'}, 404
        return user.to_dict(), 204

class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'message': '400: Invalid json payload'}
        username = data.get('username')
        if not username:
            return {'message': '400: username required'},400
        user = User.query.filter(User.username== username).first()
        if not user:
            return {'message': '404: Invalid username'}, 404
        session['user_id']=user.id
        return user.to_dict(), 200

class Logout(Resource):
    def delete(self):
        session.clear()
        return {'message': 'Logged out successfully'}, 204
    

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, '/check_session', endpoint = 'check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
