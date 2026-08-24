#------------------------------------------------
# データベース管理画面を利用するためのモジュールのインポート
#------------------------------------------------
from __init__ import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User, Time 
# from models import User, Time ,LoginForm


#import models

#------------------------------------------------
#DBのクリエイト宣言
#------------------------------------------------
db.create_all()

#admin = Admin(app)

admin = Admin(
    app,
    name='データベース管理画面',
    template_mode='bootstrap4',
)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Time, db.session))

