from elasticsearch_dsl import Document, Text, Keyword, connections
from app.config.config import Config
from flask import Flask, request, jsonify, redirect, render_template, session, make_response
from .database_engine import db
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from functools import wraps
from datetime import datetime, timedelta
import jwt
import redis
import os
import secrets
import json
INDEX_NAME = os.getenv("INDEX_NAME")

class CreateUser(db.Model):
    __tablename__ =  "create_user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    gmail = db.Column(db.String(150), unique=True, nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)
    login = db.relationship('Login', backref='user', uselist=False)

class Login(db.Model):
    __tablename__ = "login"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('create_user.id'))

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('create_user.id'))
    image = db.Column(db.String(250))
    bio = db.Column(db.Text)
    favorite_genres = db.Column(db.String(250))

class Reset(db.Model):
    __tablename__ = "Reset"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('create_user.id'))
    reset_token = db.Column(db.String(100))
    expires_at = db.Column(db.DateTime)

class VideoDocument(Document):
    title = Text()
    url = Text()
    transcript = Text(analyzer="english")
    multi_title = Keyword(multi=True)

    class Index:
        name = INDEX_NAME

class Video_Document(Document):
    title = Text()
    url = Text()
    transcript = Text(analyzer="english")
    multi_title = Keyword(multi=True)

    class Index:
        name =  INDEX_NAME



