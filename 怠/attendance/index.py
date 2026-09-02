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

from tsuya import tsuya_modify, tsuya_stamp
from honso import honso_modify, honso_stamp



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
# トップページ
# [修正] "/" にルートが無く、Colabの埋め込み表示やブラウザで
# ルートURLを開くと404 (Not Found) になっていたため、/login へ
# リダイレクトするルートを追加した。
#------------------------------------------------
@app.route('/')
def root():
    return redirect('/login')


#------------------------------------------------
# ログインページ
#------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
       if request.form['login'] == 'ログイン':
          session.permanent = True  
          number = request.form.get('number')                       # 入力値の取得
          password = request.form.get('password')                   # 入力値の取得
          user_check = User.query.filter_by(number=number).first()  # Userクラスからnumberをチェック
          if not user_check:
             return render_template('login.html', error_message='従業員番号が違います。', title="ログイン失敗")
          if check_password_hash(user_check.password, password):    # パスワードをハッシュ化してチェック
             login_user(user_check)
             session['user_number'] = user_check.number
             session['user_name'] = user_check.username

             # [追加] 管理者アカウント（is_admin=True）でログインした場合は
             # 出退勤画面(/judge)ではなく、データベース管理画面へ直接遷移させる。
             # 遷移先は /admin/ （中身が空の「Home」画面。ナビからも非表示にした）
             # ではなく、実際にデータが見える /admin/user/ にしている。
             if getattr(user_check, "is_admin", False):
                return redirect('/admin/user/')

             return redirect('/judge')

          else:
             return render_template('login.html', error_message='パスワードが違います。', title="ログイン失敗")

    return render_template('login.html', error_message='ログインして出退勤の入力をお願いします。', title="ログイン前")

#------------------------------------------------
# レコード判定ページ
#------------------------------------------------
@app.route('/judge')
@login_required                                  #ログイン必須にしたい関数の前に記述する

def judge():

    number = session['user_number']              #sessionからユーザー情報を取得
    user_name = session['user_name']             #sessionからユーザー情報を取得
    today_record = Time.query.filter(Time.number==number, Time.date==today).first() #パート番号と本日日付でレコードを検索

    if not today_record: #レコードが無い場合

       return render_template('select.html', user_name=user_name, number=number, today=today, title="本日の勤務選択")

    else:                #レコードがある場合

       record_id = today_record.id
       session["record_id"] = record_id

       if not today_record.place1:
          place1 = "未入力"
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

       if not today_record.special1:
          special1 = "off"
       else:
          special1 = "checked"

       if not today_record.highway1:
          highway1 = "off"
       else:
          highway1 = "checked"

       if not today_record.express1:
          express1 = "-,---"
       else:
          express1 = today_record.express1

       if not today_record.other1:
          other1 = ""
       else:
          other1 = today_record.other1

       if not today_record.place2:
          place2 = "未入力"
       else:
          place2 = today_record.place2

       if not today_record.start2:
          start2 = "--:--"
       else:
          start2 = today_record.start2

       if not today_record.end2:
          end2 = "--:--"
       else:
          end2 = today_record.end2

       if not today_record.leader2:
          leader2 = "off"
       else:
          leader2 = "checked"

       if not today_record.subleader2:
          subleader2 = "off"
       else:
          subleader2 = "checked"

       if not today_record.teach2:
          teach2 = "off"
       else:
          teach2 = "checked"

       if not today_record.wait2:
          wait2 = "off"
       else:
          wait2 = "checked"

       if not today_record.special2:
          special2 = "off"
       else:
          special2 = "checked"

       if not today_record.designated2:
          designated2 = "off"
       else:
          designated2 = "checked"

       if not today_record.distant2:
          distant2 = "off"
       else:
          distant2 = "checked"

       if not today_record.highway2:
          highway2 = "off"
       else:
          highway2 = "checked"

       if not today_record.express2:
          express2 = "-,---"
       else:
          express2 = today_record.express2

       if not today_record.other2:
          other2 = ""
       else:
          other2 = today_record.other2

       session["place1"] = place1          #sessionに情報をセット
       session["start1"] = start1
       session["end1"] = end1
       session["leader1"] = leader1
       session["subleader1"] = subleader1
       session["teach1"] = teach1
       session["wait1"] = wait1
       session["designated1"] = designated1
       session["distant1"] = distant1
       session["special1"] = special1
       session["highway1"] = highway1
       session["express1"] = express1
       session["other1"] = other1

       session["place2"] = place2
       session["start2"] = start2
       session["end2"] = end2
       session["leader2"] = leader2
       session["subleader2"] = subleader2
       session["teach2"] = teach2
       session["wait2"] = wait2
       session["designated2"] = designated2
       session["distant2"] = distant2
       session["highway2"] = highway2
       session["special2"] = special2
       session["express2"] = express2
       session["other2"] = other2

       return render_template('exit_view.html', 
                               title="勤怠情報", 
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
                               other1=other1, 
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
                               other2=other2 )  # パラメータをexit_view.htmlに送る


#------------------------------------------------
# 選択ページ
#------------------------------------------------
@app.route('/select', methods=['GET', 'POST'])
@login_required                                  #ログイン必須にしたい関数の前に記述する

def select():

    if request.method == 'POST':                 # 本葬、通夜を選択
       if request.form['honso-tsuya'] == '本 葬':
          return redirect('/honso_stamp')

       if request.form['honso-tsuya'] == '通 夜':
          return redirect('/tsuya_stamp')


#------------------------------------------------
# 入力済みの表示ページ
#------------------------------------------------
@app.route('/exit_view', methods=["GET","POST"])
@login_required                                  #ログイン必須にしたい関数の前に記述する

def exit_view():

    number = session['user_number']              #sessionからユーザー情報を取得
    user_name = session['user_name']             #sessionからユーザー情報を取得
    today_record = Time.query.filter(Time.number==number, Time.date==today).first() #パート番号と本日日付でレコードを検索
    honso_start1 = Time.query.filter(Time.start1==today_record.start1).first()
    tsuya_start2 = Time.query.filter(Time.start2==today_record.start2).first()
    honso_end1 = Time.query.filter(Time.end1==today_record.end1).first()            #本葬退勤時間を検索
    tsuya_end2 = Time.query.filter(Time.end2==today_record.end2).first()

    record_id = session['record_id']
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

    if request.method =='POST':                  # リクエストがPOSTの場合

       if end1 == "--:--" and start2 == "--:--":

          return render_template('honso_modify.html', 
                                  title="本葬退勤入力", 
                                  record_id=record_id, 
                                  today=today, 
                                  place1=place1, 
                                  start1=start1, 
                                  end1=end1, 
                                  other1=other1, 
                                  leader1=leader1, 
                                  subleader1=subleader1, 
                                  teach1=teach1, 
                                  wait1=wait1, 
                                  designated1=designated1, 
                                  distant1=distant1, 
                                  special1=special1, 
                                  highway1=highway1, 
                                  express1=express1 )  # パラメータをhonso_modify.htmlに送る

       else:

          if start2 == "--:--" and end2 == "--:--":

             return render_template('tsuya_stamp.html', 
                                     title="通夜勤怠入力", 
                                     record_id=record_id, 
                                     today=today, 
                                     place2=place2, 
                                     start2=start2, 
                                     end2=end2, 
                                     other2=other2, 
                                     leader2=leader2, 
                                     subleader2=subleader2, 
                                     teach2=teach2, 
                                     wait2=wait2, 
                                     designated2=designated2, 
                                     distant2=distant2, 
                                     special2=special2, 
                                     highway2=highway2, 
                                     express2=express2 )  # パラメータをtsuya_stamp.htmlに送る

          else:

             return render_template('tsuya_modify.html', 
                                     title="通夜勤怠更新", 
                                     record_id=record_id, 
                                     today=today, 
                                     place2=place2, 
                                     start2=start2, 
                                     end2=end2, 
                                     other2=other2, 
                                     leader2=leader2, 
                                     subleader2=subleader2, 
                                     teach2=teach2, 
                                     wait2=wait2, 
                                     designated2=designated2, 
                                     distant2=distant2, 
                                     special2=special2, 
                                     highway2=highway2, 
                                     express2=express2 )  # パラメータをtsuya_modify.htmlに送る



#------------------------------------------------
# DB管理の表示ページ
#------------------------------------------------
# @app.route('/admin', methods=['GET', 'POST'])
# @login_required                                  #ログイン必須にしたい関数の前に記述する
# def admin():
#     return redirect('/admin')

#employee # 従業員


#------------------------------------------------
# ログアウト
#------------------------------------------------
@app.route("/init_view", methods=["GET","POST"]) #ログアウトする
@login_required                                  #ログイン必須にしたい関数の前に記述する

def init_view():

    if request.method =='POST':                  # リクエストがPOSTの場合

       return render_template('login.html')

       logout_user() # ログアウト
       driver.close()


#------------------------------------------------
# ログアウト
#------------------------------------------------
@app.route("/honso_init", methods=["GET","POST"]) #ログアウトする
@login_required                                   #ログイン必須にしたい関数の前に記述する

def honso_init():

    if request.method =='POST':                   #リクエストがPOSTの場合

       return render_template('login.html')

       logout_user() # ログアウト
       driver.close()


#------------------------------------------------
# ログアウト
#------------------------------------------------
@app.route("/tsuya_init", methods=["GET","POST"]) #ログアウトする
@login_required                                   #ログイン必須にしたい関数の前に記述する

def tsuya_init():

    if request.method =='POST':                   #リクエストがPOSTの場合

       return render_template('login.html')

       logout_user() # ログアウト
       driver.close()


if __name__ == '__main__':
    app.run(debug=True)
