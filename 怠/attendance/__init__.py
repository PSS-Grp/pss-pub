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
# 実行環境に依存しないパス・シークレットキーを扱うためのモジュール
# [Colab対応] os / secrets を追加。カレントディレクトリに依存せず、
# このファイルがある場所を基準にパスを解決する。
#------------------------------------------------

import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#------------------------------------------------
# Flask モジュールを(__name__)でモジュール指定してアプリの生成
#------------------------------------------------

app = Flask(__name__)

#------------------------------------------------
# [修正] 末尾スラッシュの有無で自動的に別URLへリダイレクトされる挙動
# （例: /admin -> /admin/）を無効化。
# Colabのポート転送プロキシ経由だと、このリダイレクト先URLが
# 正しい外部アドレスではなく "localhost" になってしまい、埋め込み
# iframeが手元のPCのlocalhost（＝存在しない場所）を開こうとして
# 画面が真っ白になる不具合があったため。
#------------------------------------------------
app.url_map.strict_slashes = False

#------------------------------------------------
# LoginManagerの起動 #extensionを起動させる際の標準的な記述
#
# [修正] 以前は 'pss_security_key' というパスワードが平文でハードコードされ、
# 公開リポジトリに残っていた。環境変数 ATTENDANCE_SECRET_KEY があればそれを使い、
# なければ実行のたびに安全なランダム値を自動生成する。
# （ランダム生成の場合、サーバーを再起動するとログインセッションは切れる。
#   本番で使う場合は環境変数で固定値を設定すること。）
#------------------------------------------------

_secret_key = os.environ.get("ATTENDANCE_SECRET_KEY") or secrets.token_hex(32)
app.secret_key = _secret_key

login_manager = LoginManager()
login_manager.init_app(app)

#------------------------------------------------
# [修正] login_view が未設定だと、未ログイン状態で @login_required の
# ページに来た際にFlask-Loginが abort(401) を返し、ブラウザには
# 素の「Unauthorized」画面が表示されてしまう。ログインページへ
# リダイレクトされるよう明示的に設定する。
#------------------------------------------------
login_manager.login_view = "login"

#------------------------------------------------
# DBの指定 sqlite
# [修正] 相対パス "sqlite:///db/attendance.db" はカレントディレクトリに依存し、
# どこから起動しても壊れないよう、このファイルの場所からの絶対パスに変更した。
#------------------------------------------------

_db_dir = os.path.join(BASE_DIR, "db")
os.makedirs(_db_dir, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(_db_dir, "attendance.db")

#------------------------------------------------
# セッションタイムアウト時間
#------------------------------------------------
app.permanent_session_lifetime = timedelta(minutes=30)

#------------------------------------------------
# DBの指定（MySQL）
# [修正] 実際の接続パスワードが平文でコミットされていたため削除。
# MySQLを使う場合は環境変数から読み込むこと（例）。
# ------------------------------------------------
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(
#     user=os.environ["DB_USER"],
#     password=os.environ["DB_PASSWORD"],
#     host=os.environ.get("DB_HOST", "localhost"),
#     db_name=os.environ.get("DB_NAME", "attend_db"),
# )

#------------------------------------------------
# ローカルな現在の日付と時刻を取得
#------------------------------------------------
import datetime
on_time = datetime.datetime.today()
today = on_time.date()

#------------------------------------------------
# sessionを使う際にSECRET_KEYを設定
# [修正] 上の app.secret_key と重複していたうえ 'secret_key' という
# 固定文字列がハードコードされていたため、同じ値を再利用するよう統一。
#------------------------------------------------

app.config['SECRET_KEY'] = _secret_key


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
