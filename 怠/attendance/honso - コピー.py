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

    today_record = Time.query.filter(Time.number==number, Time.date==today).first()

#    print("honso_stampデバッグ１ = ",number,today,today_record)
#    db_time = Time.query.all()
#    today_record.place1, today_record.place2, today_record.start1, today_record.end1, today_record.start2, today_record.end2, today_record.option1, today_record.option2) # デバッグ


    if not today_record:                         #本日の入力が無い場合、Noneなどの値を変数に代入
       comment = "入力データなし"
       record_id = None
       place1 = "選択してください"
       start1 = "--:--"
       end1 = "--:--"
       leader1='off'
       subleader1=None 
       teach1=None 
       wait1=None 
       designated1=None 
       distant1=None 
       highway1=None 
       express1=None 
       other1=None 


#       today_record = "-"
#       place2 = "選択してください"
#       start2 = "--:--"
#       end2 = "--:--"

#       leader2=None
#       subleader2=None 
#       teach2=None 
#       wait2=None 
#       designated2=None 
#       distant2=None 
#       highway2=None 
#       express2=None 
#       other2=None 

#       place = request.form.get('place1')        # place1をから入力値を取得


    else:
       comment = "入力データあり"                #本日の入力がある場合、値のある変数はDBレコードより代入、なければNone
       record_id = today_record.id
       session["record_id"] = record_id

       if not today_record.place1:
          place1 = "-"
       else:
          place1 = today_record.place1

       if not today_record.start1:
          start1 = "--:--"
       else:
          start1 = today_record.start1

       if not today_record.end1:
          end1 = "--:--"
       else:
          end1 = today_record.end1

       if not today_record.leader1:
          leader1 = "off"
       else:
          leader1 = "checked"

       if not today_record.subleader1:
          subleader1 = "off"
       else:
          subleader1 = "checked"

       if not today_record.teach1:
          teach1 = "off"
       else:
          teach1 = "checked"

       if not today_record.wait1:
          wait1 = "off"
       else:
          wait1 = "checked"

       if not today_record.designated1:
          designated1 = "off"
       else:
          designated1 = "checked"

       if not today_record.distant1:
          distant1 = "off"
       else:
          distant1 = "checked"

       if not today_record.highway1:
          highway1 = "off"
       else:
          highway1 = "checked"

       if not today_record.express1:
          express1 = "----"
       else:
          express1 = today_record.express1

       if not today_record.other1:
          other1 = "off"
       else:
          other1 = today_record.other1


#       if not today_record.place2:
#          place2 = "-"
#       else:
#          place2 = today_record.place2

#       if not today_record.start2:
#          start2 = "--:--"
#       else:
#          start2 = today_record.start2
#
#       if not today_record.end2:
#          end2 = "--:--"
#       else:
#          end2 = today_record.end2
#
#       if not today_record.leader2:
#          leader2 = "off"
#       else:
#          leader2 = "checked"
#
#       if not today_record.subleader2:
#          subleader2 = "off"
#       else:
#          subleader2 = "checked"
#
#       if not today_record.teach2:
#          teach2 = "off"
#       else:
#          teach2 = "checked"
#
#       if not today_record.wait2:
#          wait2 = "off"
#       else:
#          wait2 = "checked"
#
#       if not today_record.designated2:
#          designated2 = "off"
#       else:
#          designated2 = "checked"
#
#       if not today_record.distant2:
#          distant2 = "off"
#       else:
#          distant2 = "checked"
#
#       if not today_record.highway2:
#          highway2 = "off"
#       else:
#          highway2 = "checked"
#
#       if not today_record.express2:
#          express2 = "----"
#       else:
#          express2 = today_record.express2
#
#       if not today_record.other2:
#          other2 = "off"
#       else:
#          other2 = today_record.other2


       session["place1"] = place1                #sessionに情報をセット
       session["start1"] = start1
       session["end1"] = end1
       session["start2"] = start2
       session["end2"] = end2
       session["leader1"] = leader1
       session["subleader1"] = subleader1
       session["teach1"] = teach1
       session["wait1"] = wait1
       session["designated1"] = designated1
       session["distant1"] = distant1
       session["highway1"] = highway1
       session["express1"] = express1
       session["other1"] = other1

#       session["place2"] = place2
#       session["leader2"] = leader2
#       session["subleader2"] = subleader2
#       session["teach2"] = teach2
#       session["wait2"] = wait2
#       session["designated2"] = designated2
#       session["distant2"] = distant2
#       session["highway2"] = highway2
#       session["express2"] = express2
#       session["other2"] = other2

       return render_template('exit_view.html',  #表示で画面に入力値を表示
                                   title=comment, 
                                   record_id=record_id, 
                                   today=today, 
                                   place1=place1, 
                                   start1=start1, 
                                   end1=end1, 
                                   start2=start2, 
                                   end2=end2, 
                                   leader1=leader1, 
                                   subleader1=subleader1, 
                                   teach1=teach1, 
                                   wait1=wait1, 
                                   designated1=designated1, 
                                   distant1=distant1, 
                                   highway1=highway1, 
                                   express1=express1, 
                                   other1=other1 )  # パラメータをexit_view.htmlに送る

#                                   place2=place2, 
#                                   leader2=leader2, 
#                                   subleader2=subleader2, 
#                                   teach2=teach2, 
#                                   wait2=wait2, 
#                                   designated2=designated2, 
#                                   distant2=distant2, 
#                                   highway2=highway2, 
#                                   express2=express2, 
#                                   other2=other2, 

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
       time.highway1=highway1
       time.express1=express1
       time.other1=other1
       db.session.add(time)                      # 入力値をTimeテーブルに追加
       db.session.commit()

#       place2 = request.form.get('place2')
#       start2 = request.form.get('start2')
#       end2 = request.form.get('end2')
#      time.place2=place2
#      time.start2=start2
#      time.end2=end2



    else:

       return render_template('honso_stamp.html', 
                                   title="入力前", 
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
                                   highway1=highway1, 
                                   express1=express1, 
                                   other1=other1)  # パラメータをexit_view.htmlに送る

#                                   place2=place2, 
#                                   start2=start2, 
#                                   end2=end2, 

       session["place1"] = place1          #sessionに情報をセット
       session["start1"] = start1
       session["end1"] = end1
       session["leader1"] = leader1
       session["subleader1"] = subleader1
       session["teach1"] = teach1
       session["wait1"] = wait1
       session["designated1"] = designated1
       session["distant1"] = distant1
       session["highway1"] = highway1
       session["express1"] = express1
       session["other1"] = other1

#       session["start2"] = start2
#       session["end2"] = end2
#       session["place2"] = place2
#       session["other2"] = other2

       time = Time()
       time.date=today
       time.number=session['user_number']
       time.place1=place1
       time.start1=start1
       time.end1=end1
       time.place2=place2
       time.start2=start2
       time.end2=end2
       time.leader=leader
       time.subleader=subleader
       time.teach=teach
       time.wait=wait
       time.designated=designated
       time.distant=distant
       time.highway=highway
       time.express=express
       time.honso=honso
       time.tsuya=tsuya
       db.session.add(record_id)                     # 入力値をTimeテーブルに追加
       db.session.commit()


    return render_template('init_view.html', 
                                   title="入力後", 
                                   record_id=record_id, 
                                   today=today, 
                                   place1=place1, 
                                   place2=place2, 
                                   start1=start1, 
                                   end1=end1, 
                                   start2=start2, 
                                   end2=end2, 
                                   leader1=leader1, 
                                   subleader1=subleader1, 
                                   teach1=teach1, 
                                   wait1=wait1, 
                                   designated1=designated1, 
                                   distant1=distant1, 
                                   highway1=highway1, 
                                   express1=express1, 
                                   other1=other1 )  # パラメータをinit_view.htmlに送る


#------------------------------------------------
# 編集ページ
#------------------------------------------------
@app.route('/honso_modify', methods=["GET","POST"])
@login_required                                  #ログイン必須にしたい関数の前に記述する

def honso_modify():

    record_id = session['record_id']

    number = session['user_number']              #sessionからユーザー情報をとってくる
    record_id = session['record_id']
    place1 = session["place1"]
    place2 = session["place2"]
    start1 = session["start1"]
    end1 = session["end1"]
    start2 = session["start2"]
    end2 = session["end2"]
    leader = session["leader"]
    subleader = session["subleader"]
    teach = session["teach"]
    wait = session["wait"]
    designated = session["designated"]
    distant = session["distant"]
    highway = session["highway"]
    express = session["express"]
    honso = session["honso"]
    tsuya = session["tsuya"]

    if request.method == 'POST':                  # リクエストがPOSTの場合

#       if place1 == "None":
#          place1 = request.form.get('place1')
#       else:
#          place1 = place1

       if not place1:
          place1 = place1
       else:
          place1 = request.form.get('place1')

       if start1 == "--:--":
          start1 = request.form.get('start1')
       else:
          start1 = start1

       if end1 == "--:--":
          end1 = request.form.get('end1')
       else:
          end1 = end1

       if place2 == "--:--":
          place2 = request.form.get('place2')
       else:
          place2 = place2

       place2 = request.form.get('place2')
       start2 = request.form.get('start2')
       end2 = request.form.get('end2')
       leader = request.form.get('leader')
       subleader = request.form.get('subleader')
       teach = request.form.get('teach')
       wait = request.form.get('wait')
       designated = request.form.get('designated')
       distant = request.form.get('distant')
       highway = request.form.get('highway')
       express = request.form.get('express')
       honso = request.form.get('honso')
       tsuya = request.form.get('tsuya')

       modify_record = Time.query.filter(Time.id == record_id).one()
#       modify_record = Time()
       modify_record.date=today
       modify_record.number=session['user_number']
       modify_record.place1=place1
       modify_record.start1=start1
       modify_record.end1=end1
       modify_record.place2=place2
       modify_record.start2=start2
       modify_record.end2=end2
       modify_record.leader=leader
       modify_record.subleader=subleader
       modify_record.teach=teach
       modify_record.wait=wait
       modify_record.designated=designated
       modify_record.distant=distant
       modify_record.highway=highway
       modify_record.express=express
       modify_record.honso=honso
       modify_record.tsuya=tsuya
#       db.session.add(time)                     # 入力値をTimeテーブルに追加
       db.session.commit()

       print("編集",start1,end1,place1,modify_record)

    else:

       print("？？？")

    return render_template('honso_init.html', 
                                   title="入力後", 
                                   record_id=record_id, 
                                   today=today, 
                                   place1=place1, 
                                   place2=place2, 
                                   start1=start1, 
                                   end1=end1, 
                                   start2=start2, 
                                   end2=end2, 
                                   leader=leader, 
                                   subleader=subleader, 
                                   teach=teach, 
                                   wait=wait, 
                                   designated=designated, 
                                   distant=distant, 
                                   highway=highway, 
                                   express=express, 
                                   honso=honso, 
                                   tsuya=tsuya )  # パラメータをexit_view.htmlに送る

