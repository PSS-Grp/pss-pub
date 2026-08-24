from werkzeug.security import generate_password_hash

# 平文のパスワード
pw = 'hujiko0-'
# generate_password_hash() デフォルト
pw_hash = generate_password_hash(pw)

print('pw =' + pw)
print('pw_hash = ' + pw_hash)
