# __init__.py モジュール から app と db 機能のインポート
------------------------------------------------
from . import app
from . import db

db.init_app(app)

#(テーブルの定義) Userクラス
------------------------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True)
    e_mail = db.Column(db.String(50),unique=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class attted(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    day = db.Column(db.String(100), unique=True)
    time = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    place = db.Column(db.String(1000))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True)
    e_mail = db.Column(db.String(50),unique=True)

#DBのクリエイト宣言
------------------------------------------------
db.create_all()


#DBが空の状態(最初の1回)はtestuserを作成する
------------------------------------------------
user = User.query.filter_by(username='testuser').first()
if user is None:
    testuser = User(username='testuser', e_mail='test@test')
    db.session.add(testuser)
    db.session.commit()


#管理画面機能を扱うために初期化
------------------------------------------------
admin = Admin(app)
admin.add_view(ModelView(User, db.session))


@app.route('/')
def index():
    user = User.query.filter_by(username='testuser').first()
    user_name = user.username
    return 'Welcome ' + user_name

if __name__ == '__main__':
    app.run(debug=True)