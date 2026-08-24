# データベース管理画面を利用するためのモジュールのインポート
#------------------------------------------------
from init import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(10))
    number = db.Column(db.String(10), unique=True)

#DBのクリエイト宣言
db.create_all()

#DBが空の状態(最初の1回)はtestuserを作成する
user = User.query.filter_by(username='testuser').first()
if user is None:
    testuser = User(username='testuser', password='323103Ps!', number='320103')
    db.session.add(testuser)
    db.session.commit()

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
