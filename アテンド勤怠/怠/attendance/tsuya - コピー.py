#from app import app
#from admin import admin.add_view

# attendance
# __init__

#### アプリの起動と各モジュールの集約 ####

from __init__ import app ,db ,login_manager

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
# ローカルな現在の日付と時刻を取得
#------------------------------------------------
import datetime
on_time = datetime.datetime.today()  
today = on_time.date()

#------------------------------------------------
# ログイン後の表示ページ
#------------------------------------------------
@app.route('/tsuya_stamp', methods=["GET","POST"])
@login_required                                  #ログイン必須にしたい関数の前に記述する

def tsuya_stamp():

    number = session['user_number']              #sessionからユーザー情報を取得

    today_record = Time.query.filter(Time.number==number, Time.date==today).first()

#    db_time = Time.query.all()
    print("tsuya_stampデバッグ１ = ",number,today,today_record)
# today_record.place1, today_record.place2, today_record.start1, today_record.end1, today_record.start2, today_record.end2, today_record.option1, today_record.option2) # デバッグ


    if not today_record:   
       comment = "入力データなし"
       record_id = None
#       today_record = "-"
       place1 = "選択してください"
       place2 = "選択してください"
       start1 = "--:--"
       end1 = "--:--"
       start2 = "--:--"
       end2 = "--:--"
       leader=None
       subleader=None 
       teach=None 
       wait=None 
       designated=None 
       distant=None 
       highway=None 
       express=None 
       honso=None 
       tsuya=None 

#       place = request.form.get('place1')      # place1をから入力値を取得


#       if request.method =='GET':                  # リクエストがGETの場合
#
#          if not place1 == "選択してください"
#             enable = "enable"
#          else:
#             enable = "disable"

    else:
       comment = "入力あり"
       record_id = today_record.id
       session["record_id"] = record_id

       if not today_record.place1:
          place1 = "-"
       else:
          place1 = today_record.place1

       if not today_record.place2:
          place2 = "-"
       else:
          place2 = today_record.place2

       if not today_record.start1:
          start1 = "--:--"
       else:
          start1 = today_record.start1

       if not today_record.end1:
          end1 = "--:--"
       else:
          end1 = today_record.end1

       if not today_record.start2:
          start2 = "--:--"
       else:
          start2 = today_record.start2

       if not today_record.end2:
          end2 = "--:--"
       else:
          end2 = today_record.end2

       if not today_record.leader:
          leader = "off"
       else:
          leader = "checked"

       if not today_record.subleader:
          subleader = "off"
       else:
          subleader = "checked"
#          subleader = today_record.subleader

       if not today_record.teach:
          teach = "off"
       else:
          teach = "checked"

       if not today_record.wait:
          wait = "off"
       else:
          wait = "checked"

       if not today_record.designated:
          designated = "off"
       else:
          designated = "checked"

       if not today_record.distant:
          distant = "off"
       else:
          distant = "checked"

       if not today_record.highway:
          highway = "off"
       else:
          highway = "checked"

       if not today_record.express:
          express = "----"
       else:
          express = today_record.express

       if not today_record.honso:
          honso = "off"
       else:
          honso = today_record.honso

       if not today_record.tsuya:
          tsuya = "off"
       else:
          tsuya = today_record.tsuya
 
       session["place1"] = place1          #sessionに情報をセット
       session["place2"] = place2
       session["start1"] = start1
       session["end1"] = end1
       session["start2"] = start2
       session["end2"] = end2
       session["leader"] = leader
       session["subleader"] = subleader
       session["teach"] = teach
       session["wait"] = wait
       session["designated"] = designated
       session["distant"] = distant
       session["highway"] = highway
       session["express"] = express
       session["honso"] = honso
       session["tsuya"] = tsuya

       return render_template('exit_view.html', 
                                   title=comment, 
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

    if request.method =='POST':                  # リクエストがPOSTの場合
#      if request.form['tsuya_stamp'] == '登録':
       place1 = request.form.get('place1')      # place1をから入力値を取得
       start1 = request.form.get('start1')
       end1 = request.form.get('end1')
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
       db.session.add(time)                     # 入力値をTimeテーブルに追加
       db.session.commit()

    else:

       return render_template('tsuya_stamp.html', 
                                   title="入力前", 
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

       session["place1"] = place1          #sessionに情報をセット
       session["place2"] = place2
       session["start1"] = start1
       session["end1"] = end1
       session["start2"] = start2
       session["end2"] = end2
       session["leader"] = leader
       session["subleader"] = subleader
       session["teach"] = teach
       session["wait"] = wait
       session["designated"] = designated
       session["distant"] = distant
       session["highway"] = highway
       session["express"] = express
       session["honso"] = honso
       session["tsuya"] = tsuya

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


    return render_template('tsuya_init.html', 
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
                                   tsuya=tsuya )  # パラメータをinit_view.htmlに送る


#------------------------------------------------
# 編集ページ
#------------------------------------------------
@app.route('/tsuya_modify', methods=["GET","POST"])
@login_required                                  #ログイン必須にしたい関数の前に記述する

def tsuya_modify():

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

    return render_template('tsuya_view.html', 
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

