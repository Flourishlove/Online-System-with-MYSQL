# all the imports
import sys, os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mysql import MySQL


from settings import APP_STATIC

# EB looks for an 'application' callable by default.

reload(sys)

sys.setdefaultencoding('utf-8')
application = Flask(__name__)
application.debug = True

mysql = MySQL()
application.config['MYSQL_DATABASE_USER'] = 'root'
application.config['MYSQL_DATABASE_PASSWORD'] = '9404122004'
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
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['userpass']
        usertype = request.form['usertype']
        sql = "INSERT INTO USER (email,username,password,usertype) VALUES (%s, %s,%s,%s)"
        try:
            cur.execute(sql, (email, username, password, usertype))
            conn.commit()
        except Exception, e:
            print str(e)
            error = 'Email Exists!!'
            return render_template('signup.html', error=error)


        return redirect(url_for('login_page'))
    else:
        return render_template('signup.html')

@application.route('/newdatapoint', methods=['GET','POST'])
def new_datapoint():
    error = None
    sql = 'select location_name from POI'
    cur.execute(sql)
    rows = [[str(item) for item in results] for results in cur.fetchall()]
    list = []
    for name in rows:
        list.append(name[0])
    if request.method == 'POST':
        poiLocationName = request.form['locationname']
        datatype = request.form['datatype']
        datavalue = request.form['value']
        timedate = request.form['timeanddate']
        sql = "INSERT INTO DATAPOINT (PLocation_Name, DateRecorded, Data_Value, DType, Accepted) VALUES (%s, %s,%s,%s,%s)"
        try:
            cur.execute(sql, (poiLocationName, timedate, datavalue, datatype, False))
            conn.commit()
            return render_template('newdatapoint.html', locationlist=list)
        except Exception, e:
            print str(e)
            error = 'POI ERROR!!'
            return render_template('newdatapoint.html', locationlist=list, error=error)
    else:
        return render_template('newdatapoint.html', locationlist=list)

@application.route('/newlocation', methods=['GET', 'POST'])
def new_location():
    error = None
    message = None
    sqlHead = 'select city from citystate'
    cur.execute(sqlHead)
    rows = [[str(item) for item in results] for results in cur.fetchall()]
    list1 = []
    for name in rows:
        list1.append(name[0])
    sqlHead = 'select state from citystate'
    cur.execute(sqlHead)
    rows = [[str(item) for item in results] for results in cur.fetchall()]
    list2 = []
    for name in rows:
        list2.append(name[0])
    if request.method == 'POST':
        locationname = request.form['locationname']
        pcity = request.form['pcity']
        pstate = request.form['pstate']
        zipcode = request.form['zipcode']
        sql = 'INSERT INTO POI (Location_Name, Zip_Code, PCity, PState) VALUES (%s, %s, %s, %s)'
        try:
            cur.execute(sql, (locationname, zipcode, pcity, pstate))
            conn.commit()
            error = None
            message = 'Add New Location Successfully!'
            return render_template('newlocation.html', message=message, error=error, citylist=list1, statelist=list2)
        except Exception, e:
            print str(e)
            error = 'Input Error!!'
            message = None
            return render_template('newlocation.html', error=error, citylist=list1, statelist=list2)
    else:
        error = None
        return render_template('newlocation.html', citylist=list1, statelist=list2)

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