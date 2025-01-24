#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User


class ClearSession(Resource):
    def delete(self):
        session.clear()
        return {}, 204


class Signup(Resource):
    def post(self):
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')

        if not username or not password:
            return {'message': '400: Username and password are required'}, 400

        
        if User.query.filter_by(username=username).first():
            return {'message': '400: Username already exists'}, 400

        user = User(username=username)
        user.password_hash = password  

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return user.to_dict(), 201


class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if not user_id:
            return {}, 204

        user = User.query.get(user_id)
        if user:
            return user.to_dict(), 200
        else:
            return {'message': '404: User not found'}, 404


class Login(Resource):
    def post(self):
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')
        
        if not username or not password:
            return {'message': '400: Username and password are required'}, 400

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):  
            session['user_id'] = user.id
            return user.to_dict(), 200

        return {'message': '401: Invalid username or password'}, 401


class Logout(Resource):
    def delete(self):
        session.clear()
        return {'message': 'Logged out successfully'}, 204



api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
