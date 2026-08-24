#from app import app
#from admin import admin.add_view

# attendance
# __init__

#### アプリの起動と各モジュールの集約 ####

from __init__ import app ,db ,login_manager ,today

from flask import Flask, request, render_template, redirect, flash, session 
from flask_login import login_required, login_user, current_user

from models import User, Time
# from models import LoginForm, User ,
from werkzeug.security import generate_password_hash, check_password_hash

#------------------------------------------------
# DB 管理ページ  # データベース管理画面のモジュール(admin.py)の読み込み
#------------------------------------------------
from admin import admin


#------------------------------------------------
# デコレータを付与したload_user関数を定義
# 現在のログインユーザーの情報を保持し、必要なときに参照できるようになる。
#------------------------------------------------
@login_manager.user_loader
def load_user(id):                               # usersテーブルから指定のidを持つレコードを取り出す
    return User.query.get(int(id))               # flask-loginがこの関数に引数として渡すidの値は文字列であるため、数値に変換する


#------------------------------------------------
# 本葬選択後の表示ページ
#------------------------------------------------
@app.route('/honso_stamp', methods=["GET","POST"])
@login_required                                  #ログイン必須にしたい関数の前に記述する

def honso_stamp():

    number = session['user_number']              #sessionからユーザー情報を取得

    start1 = "--:--"
    end1 = "--:--"
    leader1='off'
    subleader1=None 
    teach1=None 
    wait1=None 
    designated1=None 
    distant1=None 
    special1=None 
    highway1=None 
    express1=None 
    other1=None 

    if request.method =='POST':                  # POSTがリクエストされた場合
       place1 = request.form.get('place1')       # place1をから入力値を取得
       start1 = request.form.get('start1')
       end1 = request.form.get('end1')
       leader1 = request.form.get('leader1')
       subleader1 = request.form.get('subleader1')
       teach1 = request.form.get('teach1')
       wait1 = request.form.get('wait1')
       designated1 = request.form.get('designated1')
       distant1 = request.form.get('distant1')
       special1 = request.form.get('special1')
       highway1 = request.form.get('highway1')
       express1 = request.form.get('express1')
       other1 = request.form.get('other1')

       time = Time()                             # Timeテーブルに追加することを指定
       time.date=today
       time.number=session['user_number']
       time.place1=place1
       time.start1=start1
       time.end1=end1
       time.leader1=leader1
       time.subleader1=subleader1
       time.teach1=teach1
       time.wait1=wait1
       time.designated1=designated1
       time.distant1=distant1
       time.special1=special1
       time.highway1=highway1
       time.express1=express1
       time.other1=other1
       db.session.add(time)                      # 入力値をTimeテーブルに追加
       db.session.commit()


       if not end1:
          end1 = "--:--"
       else:
          end1 = end1

       if not other1:
          other1 = ""
       else:
          other1 = other1



       return render_template('honso_init.html', 
                               title="本葬勤怠確認", 
                               today=today, 
                               place1=place1, 
                               start1=start1, 
                               end1=end1, 
                               leader1=leader1, 
                               subleader1=subleader1, 
                               teach1=teach1, 
                               wait1=wait1, 
                               designated1=designated1, 
                               distant1=distant1, 
                               special1=special1, 
                               highway1=highway1, 
                               express1=express1, 
                               other1=other1 )  # パラメータをinit_view.htmlに送る

    return render_template('honso_stamp.html', 
                            title="本葬出勤入力", 
                            today=today, 
                            start1=start1, 
                            end1=end1, 
                            leader1=leader1, 
                            subleader1=subleader1, 
                            teach1=teach1, 
                            wait1=wait1, 
                            designated1=designated1, 
                            distant1=distant1, 
                            special1=special1, 
                            highway1=highway1, 
                            express1=express1, 
                            other1=other1)  # パラメータをexit_view.htmlに送る

#------------------------------------------------
# 編集ページ
#------------------------------------------------
@app.route('/honso_modify', methods=["GET","POST"])
@login_required                                  #ログイン必須にしたい関数の前に記述する

def honso_modify():

    record_id = session['record_id']
    number = session['user_number']              #sessionからユーザー情報をとってくる
    place1 = session["place1"]
    start1 = session["start1"]
    end1 = session["end1"]
    leader1 = session["leader1"]
    subleader1 = session["subleader1"]
    teach1 = session["teach1"]
    wait1 = session["wait1"]
    designated1 = session["designated1"]
    distant1 = session["distant1"]
    special1 = session["special1"]
    highway1 = session["highway1"]
    express1 = session["express1"]
    other1 = session["other1"]

    print("セッションゲット",express1)

    if request.method == 'POST':                  # リクエストがPOSTの場合

       if end1 == "--:--":
          end1 = request.form.get('end1')
       else:
          end1 = end1

       leader1 = request.form.get('leader1')
       subleader1 = request.form.get('subleader1')
       teach1 = request.form.get('teach1')
       wait1 = request.form.get('wait1')
       designated1 = request.form.get('designated1')
       distant1 = request.form.get('distant1')
       special1 = request.form.get('special1')
       highway1 = request.form.get('highway1')
#       express1 = request.form.get('express1')

       if express1 == "-,---":
          express1 = request.form.get('express1')
       else:
          express1 = express1

       other1 = request.form.get('other1')

       print("入力ゲット",express1)

       modify_record = Time.query.filter(Time.id == record_id).one() # レコードを上書き
       modify_record.date=today
       modify_record.number=session['user_number']
       modify_record.place1=place1
       modify_record.start1=start1
       modify_record.end1=end1
       modify_record.leader1=leader1
       modify_record.subleader1=subleader1
       modify_record.teach1=teach1
       modify_record.wait1=wait1
       modify_record.designated1=designated1
       modify_record.distant1=distant1
       modify_record.special1=special1
       modify_record.highway1=highway1
       modify_record.express1=express1
       modify_record.other1=other1
#       db.session.add(time)                     # 入力値をTimeテーブルに追加
       db.session.commit()

       print("DB更新",express1)

    return render_template('honso_init.html', 
                            title="本葬勤怠確認", 
                            record_id=record_id, 
                            today=today, 
                            place1=place1, 
                            start1=start1, 
                            end1=end1, 
                            leader1=leader1, 
                            subleader1=subleader1, 
                            teach1=teach1, 
                            wait1=wait1, 
                            designated1=designated1, 
                            distant1=distant1, 
                            special1=special1, 
                            highway1=highway1, 
                            express1=express1, 
                            other1=other1 )  # パラメータをhonso_init.htmlに送る

