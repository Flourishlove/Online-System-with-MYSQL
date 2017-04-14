# all the imports
import sys, os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask.ext.mysql import MySQL
from hashlib import md5


from settings import APP_STATIC

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.debug = True

mysql = MySQL()

application = Flask(__name__)


application.config['MYSQL_DATABASE_USER'] = 'lyr1994'
application.config['MYSQL_DATABASE_PASSWORD'] = 'database4400'
application.config['MYSQL_DATABASE_DB'] = 'city82'
application.config['MYSQL_DATABASE_HOST'] = 'database4400.clmserjcl9pt.us-east-1.rds.amazonaws.com'

mysql.init_app(application)

conn = mysql.connect()
cur = conn.cursor()

class ServerError(Exception):pass

@application.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']

        cur.execute("SELECT COUNT(1) FROM users WHERE name = {};"
                    .format(username_form))
        if not cur.fetchone()[0]:
            raise ServerError('Invalid username')

        password_form = request.form['password']
        cur.execute("SELECT pass FROM users WHERE name = {};"
                    .format(username_form))

        for row in cur.fetchall():
            if md5(password_form).hexdigest() == row[0]:
                session['username'] = request.form['username']
                return redirect(url_for('choosefunction'))
            else :
                flash("Wrong Password!")
        url = request.form['target_url']
        return redirect(url_for('choosefunction', url=url))
    else:
        entries = []
        return render_template('login.html', entries=entries)


@application.route('/choosefunction', methods=['GET'])
def choose_function():
    return render_template('choosefunction.html')

@application.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@application.route('/newdatapoint', methods=['GET'])
def new_datapoint():
    return render_template('newdatapoint.html')

@application.route('/newlocation', methods=['GET'])
def new_location():
    return render_template('newlocation.html')

@application.route('/pendingdatapoint', methods=['GET'])
def pending_datapoint():
    return render_template('pendingdatapoint.html')

@application.route('/pendingaccount', methods=['GET'])
def pending_account():
    return render_template('pendingaccount.html')

@application.route('/viewpoi', methods=['GET'])
def view_poi():
    return render_template('viewpoi.html')

@application.route('/poidetail', methods=['GET'])
def poi_detail():
    return render_template('poidetail.html')

@application.route('/poireport', methods=['GET'])
def poi_report():
    return render_template('poireport.html')

@application.route('/', methods=['GET'])
def mainpage():
    return render_template('index.html')


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()