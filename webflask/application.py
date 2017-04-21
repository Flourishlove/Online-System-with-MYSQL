# all the imports
import sys, os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mysql import MySQL
import ast

from settings import APP_STATIC

# EB looks for an 'application' callable by default.

reload(sys)

sys.setdefaultencoding('utf-8')
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
        username = request.form['username']
        email = request.form['email']
        password = request.form['userpass']
        usertype = request.form['usertype']

        if usertype == 'city_official':
            title = request.form['usertitle']
            approved = False
            ucity = request.form['usercity']
            ustate = request.form['userstate']
        else:
            title = None
            approved = True
            ucity = None
            ustate = None

        sql = "INSERT INTO USER (email,username,password,usertype,title,approved,ucity,ustate) VALUES (%s,%s,%s,%s,%s,%r,%s,%s)"
        try:
            cur.execute(sql, (email, username, password, usertype, title, approved, ucity, ustate))
            conn.commit()
        except Exception, e:
            print str(e)
            error = e
            return render_template('signup.html', error=error, citylist=list1, statelist=list2)

        return redirect(url_for('login_page'))
    else:
        return render_template('signup.html', citylist=list1, statelist=list2)

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

@application.route('/pendingdatapoint', methods=['GET', 'POST'])
def pending_datapoint():
    cur.execute("SELECT PLocation_Name, DType, Data_Value, DateRecorded FROM DATAPOINT WHERE NOT Accepted;")
    entries = cur.fetchall()
    if request.method == 'POST':
        checklist = request.form.getlist('check')
        checklist = [str(x) for x in checklist]
        if request.form['action'] == 'Reject':
            for value in checklist:
                print value
                index = int(value)
                cur.execute("DELETE FROM DATAPOINT WHERE PLocation_Name = %s AND DateRecorded = %s;", [entries[index][0], entries[index][3]])
        else:
            for value in checklist:
                print value
                index = int(value)
                cur.execute("UPDATE DATAPOINT SET Accepted = 1 WHERE PLocation_Name = %s AND DateRecorded = %s;", [entries[index][0], entries[index][3]])
        return redirect(url_for('pending_datapoint'))
    else:
        return render_template('pendingdatapoint.html', entries=entries)

@application.route('/pendingaccount', methods=['GET', 'POST'])
def pending_account():
    cur.execute("SELECT Username, Email, UCity, UState, Title FROM USER WHERE NOT Approved;")
    entries = cur.fetchall()
    if request.method == 'POST':
        checklist = request.form.getlist('check')
        checklist = [str(x) for x in checklist]
        if request.form['action'] == 'Reject':
            for value in checklist:
                print value
                index = int(value)
                cur.execute("DELETE FROM USER WHERE Email = %s;", [entries[index][1]])
        else:
            for value in checklist:
                print value
                index = int(value)
                cur.execute("UPDATE USER SET Approved = 1 WHERE Email = %s;", [entries[index][1]])
        return redirect(url_for('pending_account'))
    else:
        return render_template('pendingaccount.html', entries=entries)

@application.route('/viewpoi', methods=['GET','POST'])
def view_poi():
    sqlHead = 'select Location_Name from poi'
    cur.execute(sqlHead)
    rows = [[str(item) for item in results] for results in cur.fetchall()]
    list_location = []
    for name in rows:
        list_location.append(name[0])
    sqlHead = 'select state from citystate'
    cur.execute(sqlHead)
    rows = [[str(item) for item in results] for results in cur.fetchall()]
    list_state = []
    for name in rows:
        list_state.append(name[0])
    sqlHead = 'select city from citystate'
    cur.execute(sqlHead)
    rows = [[str(item) for item in results] for results in cur.fetchall()]
    list_city = []
    for name in rows:
        list_city.append(name[0])
    if request.method == 'POST':
        locationNmae = request.form['locationname']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        flag = request.form.getlist('flag')
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        sql = 'select Location_Name,PCity,PState,Zip_Code,Flag,Date_Flagged from poi '
        needAnd = False
        needWhere = True
        if locationNmae != 'null':
            sql +='where Location_Name=\''+locationNmae+'\' '
            needAnd = True
            needWhere = False
        if city != 'null':
            if needWhere:
                sql += 'where '
                needWhere = False
            else:
                sql += 'and '
            sql += 'pcity=\''+city+'\' '
        if state != 'null':
            if needWhere:
                sql += 'where '
                needWhere = False
            else:
                sql += 'and '
            sql += 'pstate=\''+state+'\' '
        if len(zipcode) > 0:
            print(zipcode)
            if needWhere:
                sql += 'where '
                needWhere = False
            else:
                sql += 'and '
            sql += 'Zip_Code='+zipcode+' '

        if len(startdate) > 0 and len(enddate) > 0:
            print('startdate='+startdate)
            print('enddate='+enddate)
            if needWhere:
                sql += 'where '
                needWhere = False
            else:
                sql += 'and '
            sql += 'Date_Flagged between \''+startdate+'\' and \''+enddate+'\' '
        if len(flag) > 0:
            print(flag)
            if needWhere:
                sql += 'where '
                needWhere = False
            else:
                sql += 'and '
            sql += 'Flag=True'
        print(sql)

        matrix = []
        try:
            cur.execute(sql)
            conn.commit()
            matrix =cur.fetchall()
            print(matrix)

        except Exception,e:
            print(e)

        return render_template('viewpoi.html', matrix=matrix, namelist=list_location, citylist=list_city, statelist=list_state)
    else:
        return render_template('viewpoi.html', namelist=list_location, citylist=list_city, statelist=list_state)

@application.route('/poidetail', methods=['GET', 'POST'])
def poi_detail():
    if request.method == 'POST':
        StartDate = request.form['StartDate']
        EndValue = request.form['EndValue']
        StartDate = request.form['StartDate']
        EndDate = request.form['EndDate']
        print StartDate
        cur.execute("SELECT Username, Email, UCity, UState, Title FROM POI WHERE NOT Approved;")
        return redirect(url_for('poi_detail'))
    else:
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