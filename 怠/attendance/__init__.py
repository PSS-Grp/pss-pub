#------------------------------------------------
# flask パッケージ から Flask モジュールのインポート
#------------------------------------------------

#from flask import Flask, render_template, request, redirect
from flask import Flask
from datetime import timedelta 

#------------------------------------------------
# データベースを利用するための flask_sqlalchemy モジュールから SQLAlchemy クラスのインポート
#------------------------------------------------

from flask_sqlalchemy import SQLAlchemy

#------------------------------------------------
# データベース管理画面を利用するためのモジュールのインポート
#------------------------------------------------

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

#------------------------------------------------
# ログイン機能を利用するためのモジュールのインポート
#------------------------------------------------

from flask_login import LoginManager, login_required

#------------------------------------------------
# Flask モジュールを(__name__)でモジュール指定してアプリの生成
#------------------------------------------------

app = Flask(__name__)

#------------------------------------------------
# LoginManagerの起動 #extensionを起動させる際の標準的な記述
#------------------------------------------------

app.secret_key = 'pss_security_key'

login_manager = LoginManager()
login_manager.init_app(app)

#------------------------------------------------
# DBの指定 sqlite
#------------------------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/attendance.db"

#------------------------------------------------
# セッションタイムアウト時間
#------------------------------------------------
app.permanent_session_lifetime = timedelta(minutes=30) 

#------------------------------------------------
# DBの指定（MySQL）
# ------------------------------------------------
#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
#      'user': "pss",
#      'password': "hujiko0-",
#      'host': "localhost",
#      'db_name': "attend_db"
#  })

#------------------------------------------------
# ローカルな現在の日付と時刻を取得
#------------------------------------------------
import datetime
on_time = datetime.datetime.today()  
today = on_time.date()

#------------------------------------------------
#sessionを使う際にSECRET_KEYを設定
#------------------------------------------------

app.config['SECRET_KEY'] = 'secret_key'


#------------------------------------------------
# おまじない
#------------------------------------------------

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#------------------------------------------------
# dbの初期化
#------------------------------------------------

db = SQLAlchemy(app)

#------------------------------------------------
# Flask-LoginがユーザーIDからユーザー情報を復元する方法や、ログインする処理などをFlaskと連携するために利用するオブジェクトを作成する
#------------------------------------------------
