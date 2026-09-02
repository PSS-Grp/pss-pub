#------------------------------------------------
# Colab / ローカル環境でこのアプリを試すためのセットアップスクリプト。
#
# 元リポジトリにコミットされていた db/attendance.db には、実際の従業員
# データ（従業員番号やパスワードハッシュ）が含まれている可能性があったため、
# このプロジェクトには含めていない。代わりに、このスクリプトを実行すると
# 空のDBを作成し、動作確認用のアカウントとサンプルの会館データを作成する。
#
#   1. 一般の従業員アカウント（出退勤の打刻用。is_admin=False）を3件
#      → それぞれ別々の会館名（Place）が割り当てられており、
#        本葬・通夜の出勤画面の「会館」プルダウンに、ログインした
#        ユーザーごとに異なる会館名が表示されることを確認できる。
#   2. 管理者アカウント（/admin のデータベース管理画面用。is_admin=True）を1件
#
# どちらも同じ /login 画面からログインするが、管理画面へは is_admin=True の
# アカウントでログインした場合のみアクセスできる（admin.py 参照）。
# 「その他」を選ぶと従来通り手動入力ができる（プルダウンの一覧には含めない）。
#
# 実際の従業員データ・会館データを使う場合は、管理者アカウントでログイン後、
# /admin 画面からUser・Placeを登録してください。
#------------------------------------------------

import os
import sys

APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from __init__ import app, db  # noqa: E402
from models import User, Place  # noqa: E402
from werkzeug.security import generate_password_hash  # noqa: E402

ADMIN_NUMBER = os.environ.get("ADMIN_USER_NUMBER", "9001")
ADMIN_NAME = os.environ.get("ADMIN_USER_NAME", "管理者")
ADMIN_PASSWORD = os.environ.get("ADMIN_USER_PASSWORD", "admin1234")

# 従業員番号・氏名・パスワード・その従業員が選べる会館名のリスト（適当なサンプル）。
# 「その他」はテンプレート側で自動的に末尾に追加されるため、ここには含めない。
DEMO_EMPLOYEES = [
    {
        "number": "0001",
        "name": "デモ太郎",
        "password": "demo1234",
        "places": ["愛知葬祭 春日井会場", "平安会館 一宮斎場"],
    },
    {
        "number": "0002",
        "name": "デモ次郎",
        "password": "demo2345",
        "places": ["名古屋メモリアルホール", "豊田会館"],
    },
    {
        "number": "0003",
        "name": "デモ花子",
        "password": "demo3456",
        "places": ["岡崎セレモニーホール", "安城会館", "刈谷会館"],
    },
]


def _create_user_if_missing(number, name, password, is_admin, places=None):
    existing = User.query.filter_by(number=number).first()
    if existing:
        print(f"  従業員番号 {number} は既に存在します（作成をスキップ）。")
        return existing

    user = User(
        username=name,
        number=number,
        password=generate_password_hash(password),
        is_admin=is_admin,
    )
    db.session.add(user)
    db.session.commit()

    kind = "管理者アカウント" if is_admin else "従業員アカウント"
    print(f"  {kind}を作成しました。 従業員番号: {number} / パスワード: {password}")

    for place_name in places or []:
        db.session.add(Place(user_id=user.id, place=place_name))
    if places:
        db.session.commit()
        print(f"    会館名を登録しました: {', '.join(places)}")

    return user


def main():
    with app.app_context():
        db.create_all()

        print("デモ用アカウントを準備します。")
        for emp in DEMO_EMPLOYEES:
            _create_user_if_missing(
                emp["number"], emp["name"], emp["password"], is_admin=False, places=emp["places"]
            )
        _create_user_if_missing(ADMIN_NUMBER, ADMIN_NAME, ADMIN_PASSWORD, is_admin=True)


if __name__ == "__main__":
    main()
