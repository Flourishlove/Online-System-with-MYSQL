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
conn = mysql.connect()
cur = conn.cursor()


@application.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        user_type = None
        error = None
        email = request.form['useremail']
        password = request.form['userpass']
        cur.execute("SELECT COUNT(1) FROM USER WHERE Email = %s;", [email])
        if cur.fetchone()[0]:
            cur.execute("SELECT Username, Password, UserType FROM USER WHERE Email = %s;", [email])
            for row in cur.fetchall():
                if password == row[1]:
                    session['logged_in'] = True
                    session['username'] = row[0]
                    user_type = row[2]
                else:
                    error = "Invalid Credential"
        else:
            error = "User not exist"
        if error:
            return redirect(url_for('login_page', error=error))
        else:
            return redirect(url_for('choose_function', type=user_type))
    else:
        error = request.args.get('error')
        return render_template('login.html', error=error)

@application.route('/choosefunction', methods=['GET', 'POST'])
def choose_function():
    curType = request.args.get('type')
    if request.method == 'POST':
        if request.form['action'] == 'Pending Data Point':
            return redirect(url_for('pending_datapoint'))
        elif request.form['action'] == 'Pending City Official Accounts':
            return redirect(url_for('pending_account'))
        elif request.form['action'] == 'Filter/Search POI':
            return redirect(url_for('view_poi'))
        else:
            return redirect(url_for('poi_detail'))
    else:
        if curType == 'admin':
            entries = ['Pending Data Point', 'Pending City Official Accounts']
        else:
            entries = ['Filter/Search POI', 'POI Report']
        return render_template('choosefunction.html', entries=entries)

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['userpass']
        usertype = request.form['usertype']
        sql = "INSERT INTO USER (email,username,password,usertype) VALUES (%s, %s,%s,%s)"
        cur.execute(sql, (email, username, password,usertype))
        conn.commit()
        return redirect(url_for('login_page'))
    else:
        return render_template('signup.html')

@application.route('/newdatapoint', methods=['GET'])
def new_datapoint():
    return render_template('newdatapoint.html')

@application.route('/newlocation', methods=['GET', 'POST'])
def new_location():
    if request.method == 'POST':
        return redirect(url_for('new_location'))
    else:
        return render_template('newlocation.html')

@application.route('/pendingdatapoint', methods=['GET'])
def pending_datapoint():
    cur.execute("SELECT PLocation_Name, DType, Data_Value, DateRecorded FROM DATAPOINT WHERE NOT Accepted;")
    entries = cur.fetchall()
    return render_template('pendingdatapoint.html', entries=entries)

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

application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()