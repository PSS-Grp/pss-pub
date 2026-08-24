from flask import Flask, render_template

import admin

print(__name__)
app = Flask(__name__)

#tamplatesからhtmlを読み込む
#@app.route("/", methods==['GET','POST'] )
@app.route("/" )
def login_page():
    return render_template('index.html')

@app.route("/time_stamp")
def input_page():
    return render_template('time_stamp.html')

@app.route("/admin")
def admin_page():
    return render_template('admin.html')


if __name__ == "__main__":
    app.run(debug=True)
