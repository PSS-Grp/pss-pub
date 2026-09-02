#from app import app
#from admin import admin.add_view

# attendance
# __init__

#### アプリの起動と各モジュールの集約 ####

from __init__ import app ,db ,login_manager ,today

from flask import Flask, request, render_template, redirect, flash, session 
from flask_login import login_required, login_user, current_user

from models import User, Time, Place
# from models import LoginForm, User ,
from werkzeug.security import generate_password_hash, check_password_hash


#------------------------------------------------
# [追加] ログイン中のユーザーに紐づく会館名の一覧を取得するヘルパー。
# honso.py 側と同じロジック（重複しているが、既存ファイル構成を
# 大きく変えないよう、あえてそれぞれのファイルに置いている）。
#------------------------------------------------
def get_places_for_current_user():
    return [
        p.place
        for p in Place.query.filter(
            (Place.user_id == current_user.id) | (Place.user_id.is_(None))
        )
        .order_by(Place.id)
        .all()
    ]

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
# 通夜選択後の表示ページ
#------------------------------------------------
@app.route('/tsuya_stamp', methods=["GET","POST"])
@login_required                                  #ログイン必須にしたい関数の前に記述する

def tsuya_stamp():

    number = session['user_number']              #sessionからユーザー情報を取得

    start2 = "--:--"
    end2 = "--:--"
    leader2='off'
    subleader2=None 
    teach2=None 
    wait2=None 
    designated2=None 
    distant2=None 
    special2=None 
    highway2=None 
    express2=None 
    other2=None 
    record_id=None 

    if request.method =='POST':                  # POSTがリクエストされた場合
       place2 = request.form.get('place2')       # place2をから入力値を取得
       start2 = request.form.get('start2')
       end2 = request.form.get('end2')
       leader2 = request.form.get('leader2')
       subleader2 = request.form.get('subleader2')
       teach2 = request.form.get('teach2')
       wait2 = request.form.get('wait2')
       designated2 = request.form.get('designated2')
       distant2 = request.form.get('distant2')
       special2 = request.form.get('special2')
       highway2 = request.form.get('highway2')
       express2 = request.form.get('express2')
       other2 = request.form.get('other2')

       record_id = session['record_id']              #sessionからユーザー情報を取得
       new_record = Time.query.filter(Time.id == record_id).first() # レコードを上書き
       print("デバッグ１ = ",number,record_id,new_record)

       if not new_record:

          print("デバッグ２ = ",number,record_id,new_record)

          time = Time()                             # Timeテーブルに追加することを指定
#          time = Time.query.filter(Time.id == record_id).first() # レコードを上書き
          time.date=today
          time.number=session['user_number']
          time.place2=place2
          time.start2=start2
          time.end2=end2
          time.leader2=leader2
          time.subleader2=subleader2
          time.teach2=teach2
          time.wait2=wait2
          time.designated2=designated2
          time.distant2=distant2
          time.special2=special2
          time.highway2=highway2
          time.express2=express2
          time.other2=other2
          db.session.add(time)                      # 入力値をTimeテーブルに追加
          db.session.commit()

          if not end2:
             end2 = "--:--"
          else:
             end2 = end2

          if not other2:
             other2 = ""
          else:
             other2 = other2

          return render_template('tsuya_init.html', 
                                  title="通夜勤怠確認", 
                                  today=today, 
                                  place2=place2, 
                                  start2=start2, 
                                  end2=end2, 
                                  leader2=leader2, 
                                  subleader2=subleader2, 
                                  teach2=teach2, 
                                  wait2=wait2, 
                                  designated2=designated2, 
                                  distant2=distant2, 
                                  special2=special2, 
                                  highway2=highway2, 
                                  express2=express2, 
                                  other2=other2 )  # パラメータをinit_view.htmlに送る

       else:

          print("デバッグ３ = ",number,record_id,new_record)

          record_id = session['record_id']              #sessionからユーザー情報を取得

          modify_record = Time.query.filter(Time.id == record_id).one() # レコードを上書き
          # [修正] 元コードは modify_record.date=record_id という誤代入の直後に
          # modify_record.date=today で上書きしており無意味だったため削除。
          modify_record.date=today
          modify_record.number=session['user_number']
          modify_record.place2=place2
          modify_record.start2=start2
          modify_record.end2=end2
          modify_record.leader2=leader2
          modify_record.subleader2=subleader2
          modify_record.teach2=teach2
          modify_record.wait2=wait2
          modify_record.designated2=designated2
          modify_record.distant2=distant2
          modify_record.special2=special2
          modify_record.highway2=highway2
          modify_record.express2=express2
          modify_record.other2=other2
          db.session.commit()                     # 入力値で更新

          if not end2:
             end2 = "--:--"
          else:
             end2 = end2

          if not other2:
             other2 = ""
          else:
             other2 = other2


          return render_template('tsuya_init.html', 
                                  title="通夜勤怠確認", 
                                  today=today, 
                                  place2=place2, 
                                  start2=start2, 
                                  end2=end2, 
                                  leader2=leader2, 
                                  subleader2=subleader2, 
                                  teach2=teach2, 
                                  wait2=wait2, 
                                  designated2=designated2, 
                                  distant2=distant2, 
                                  special2=special2, 
                                  highway2=highway2, 
                                  express2=express2, 
                                  other2=other2 )  # パラメータをinit_view.htmlに送る

    return render_template('tsuya_stamp.html',
                            title="通夜出勤入力",
                            today=today,
                            places=get_places_for_current_user(),
                            start2=start2,
                            end2=end2, 
                            leader2=leader2, 
                            subleader2=subleader2, 
                            teach2=teach2, 
                            wait2=wait2, 
                            designated2=designated2, 
                            distant2=distant2, 
                            special2=special2, 
                            highway2=highway2, 
                            express2=express2, 
                            other2=other2)  # パラメータをexit_view.htmlに送る


#------------------------------------------------
# 編集ページ
#------------------------------------------------
@app.route('/tsuya_modify', methods=["GET","POST"])
@login_required                                  #ログイン必須にしたい関数の前に記述する

def tsuya_modify():

    record_id = session['record_id']
    number = session['user_number']              #sessionからユーザー情報をとってくる
    place2 = session["place2"]
    start2 = session["start2"]
    end2 = session["end2"]
    leader2 = session["leader2"]
    subleader2 = session["subleader2"]
    teach2 = session["teach2"]
    wait2 = session["wait2"]
    designated2 = session["designated2"]
    distant2 = session["distant2"]
    special2 = session["special2"]
    highway2 = session["highway2"]
    express2 = session["express2"]
    other2 = session["other2"]

    if request.method == 'POST':                  # リクエストがPOSTの場合

       if end2 == "--:--":
          end2 = request.form.get('end2')
       else:
          end2 = end2

       leader2 = request.form.get('leader2')
       subleader2 = request.form.get('subleader2')
       teach2 = request.form.get('teach2')
       wait2 = request.form.get('wait2')
       designated2 = request.form.get('designated2')
       distant2 = request.form.get('distant2')
       special2 = request.form.get('special2')
       highway2 = request.form.get('highway2')
#       express2 = request.form.get('express2')

       if express2 == "-,---":
          express2 = request.form.get('express2')
       else:
          express2 = express2

       other2 = request.form.get('other2')

       if not other2:
          other2 = ""
       else:
          other2 = other2

       modify_record = Time.query.filter(Time.id == record_id).one() # レコードを上書き
       modify_record.date=today
       modify_record.number=session['user_number']
       modify_record.place2=place2
       modify_record.start2=start2
       modify_record.end2=end2
       modify_record.leader2=leader2
       modify_record.subleader2=subleader2
       modify_record.teach2=teach2
       modify_record.wait2=wait2
       modify_record.designated2=designated2
       modify_record.distant2=distant2
       modify_record.special2=special2
       modify_record.highway2=highway2
       modify_record.express2=express2
       modify_record.other2=other2
#       db.session.add(time)                     # 入力値をTimeテーブルに新規追加
       db.session.commit()                     # 入力値で更新


    return render_template('tsuya_init.html', 
                            title="通夜勤怠確認", 
                            record_id=record_id, 
                            today=today, 
                            place2=place2, 
                            start2=start2, 
                            end2=end2, 
                            leader2=leader2, 
                            subleader2=subleader2, 
                            teach2=teach2, 
                            wait2=wait2, 
                            designated2=designated2, 
                            distant2=distant2, 
                            special2=special2, 
                            highway2=highway2, 
                            express2=express2, 
                            other2=other2 )  # パラメータをtsuya_init.htmlに送る

