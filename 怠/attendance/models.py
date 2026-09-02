# Flask-Loginがユーザーを管理する際に利用するクラスを作成する
# Userクラスに入れた情報はAPIの中でcurrent_userとして取得ができるようになるので、後で利用したい情報があればこのクラスに入れておく

# attendance
# __init__

#------------------------------------------------
# 基本的なモジュールの読み込み
#------------------------------------------------

from __init__ import app, db, login_manager

#------------------------------------------------
# ハッシュ化されたパスワードを管理するために、werkzeug(flaskのDependency)を利用する
#------------------------------------------------

#from werkzeug.security import generate_password_hash, check_password_hash

#------------------------------------------------
# UserMixinクラスをimport UserMixinでログインに必要な機能を継承する。
#------------------------------------------------

from flask import render_template, redirect
from flask_login import UserMixin, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

class User(UserMixin):
   def __init__(self,id):
       self.id = id

#------------------------------------------------
# UserMixinクラスを継承したUserクラスを定義
# モデル
# 2つ継承「db.Model」はSQLAlchemy、「UserMixin」はflask_login
#------------------------------------------------

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    number = db.Column(db.String(8), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    # [追加] データベース管理画面(/admin)にアクセスできるかどうかを表すフラグ。
    # 一般の従業員アカウントではFalseのままにし、管理者専用アカウントだけ
    # Trueにすることで、出退勤ログインと管理者アクセスを区別する。
    is_admin = db.Column(db.Boolean, nullable=False, default=False, server_default="0")


#------------------------------------------------
# パスワードをハッシュ化
#------------------------------------------------
    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self.password

#------------------------------------------------
# 入力されたパスワードが登録されているパスワードハッシュと一致するかを確認
#------------------------------------------------
#    def check_password(self, password):
#        return check_password_hash(self.password, password)
#
#    def __repr__(self):
#        return "User('{self.password}')"
#
#    def check_password(self, password):
#        password_hash = generate_password_hash(password)
#        print('password_hash = ' + 'self.password')


#------------------------------------------------
# ログイン入力項目・ボタンとの紐づけ
#------------------------------------------------

# class LoginForm(FlaskForm):
#     __tablename__ = "user"
#     username = StringField('username', validators=[DataRequired()])
#     password = PasswordField('password', validators=[DataRequired()])
#     number = StringField('number', validators=[DataRequired()])
#     submit = SubmitField('ログイン')


#------------------------------------------------
# 出退勤時間のクラスを定義
#------------------------------------------------

class Time(db.Model):

    __tablename__ = "time"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    number = db.Column(db.String(8))
    place1 = db.Column(db.String(10))
    start1 = db.Column(db.String(10))
    end1 = db.Column(db.String(10))
    leader1 = db.Column(db.String(10))
    subleader1 = db.Column(db.String(10))
    teach1 = db.Column(db.String(10))
    wait1 = db.Column(db.String(10))
    designated1 = db.Column(db.String(10))
    distant1 = db.Column(db.String(10))
    highway1 = db.Column(db.String(10))
    express1 = db.Column(db.String(10))
    other1 = db.Column(db.String(10))
    special1 = db.Column(db.String(10))
    place2 = db.Column(db.String(10))
    start2 = db.Column(db.String(10))
    end2 = db.Column(db.String(10))
    leader2 = db.Column(db.String(10))
    subleader2 = db.Column(db.String(10))
    teach2 = db.Column(db.String(10))
    wait2 = db.Column(db.String(10))
    designated2 = db.Column(db.String(10))
    distant2 = db.Column(db.String(10))
    highway2 = db.Column(db.String(10))
    express2 = db.Column(db.String(10))
    other2 = db.Column(db.String(10))
    special2 = db.Column(db.String(10))


class Place(db.Model):
    # [修正/追加]
    # ・元々このモデルは定義されているだけで、どこからも使われていなかった。
    #   これを使って「会館名」を一般ユーザーごとに変えられるようにした。
    # ・user_id を追加し、どのユーザーに表示する会館かを紐づけられるようにした。
    #   （user_idがNULLの行は、全ユーザー共通の会館として扱う）
    # ・company/area/place の文字数上限が10文字と短く、実際の会館名
    #   （例:「愛知葬祭 春日井会場」で10文字ちょうど）だと収まらないケースが
    #   あったため、余裕を持たせて100文字に広げた。

    __tablename__ = "Place"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    company = db.Column(db.String(100))
    area = db.Column(db.String(100))
    place = db.Column(db.String(100), nullable=False)
    other = db.Column(db.String(100))

    user = db.relationship("User", backref=db.backref("places", lazy="dynamic"))
