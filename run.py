from core.app import core_app
from flask import Flask
import os
import pymysql

if os.getenv("PORT"):
    port = int(os.getenv("PORT"))


app = Flask(__name__)

app.register_blueprint(core_app)

# Run the server via Python
if __name__ == '__main__':
    onGaia = False

    # instance-folders configuration
    CONN = pymysql.connect(host='localhost',
                           user='root',
                           passwd='',
                           db='aimversions',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

    app.config.from_object('config.Development')
    app.config.update(dict(DATABASE=CONN))

    # Run server
    app.run()

else:
    CONN = pymysql.connect(host='us-cdbr-iron-east-04.cleardb.net',
                           user='b587f56c2dc0e4',
                           passwd='323eb5ed',
                           db='ad_83b0e5b3ce40758',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

    app.config.from_object('config.Production')
    app.config.update(dict(DATABASE=CONN))

    onGaia = True


# For gunicorn
# app = bottle.default_app()
# in manifest must go command= gunicorn run:app
