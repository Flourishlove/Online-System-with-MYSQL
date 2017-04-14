# all the imports
import sys, os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mysql import MySQL


from settings import APP_STATIC

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.debug = True

mysql = MySQL()
application.config['MYSQL_DATABASE_USER'] = 'root'
application.config['MYSQL_DATABASE_PASSWORD'] = 'FriApr14'
application.config['MYSQL_DATABASE_DB'] = 'city82'
application.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(application)


sql = "show tables"
conn = mysql.connect()
cursor = conn.cursor()
cursor.execute(sql)
for row in cursor:
    print (row)


@application.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['useremail']
        password = request.form['userpass']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT UserType FROM USER WHERE ")
        return redirect(url_for('choose_function', type=type))
    else:
        entries = []
        return render_template('login.html', entries=entries)


@application.route('/choosefunction', methods=['GET'])
def choose_function():
    entries = []
    return render_template('choosefunction.html', entries=entries)

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