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

@application.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('login_page'))

@application.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        user_type = None
        error = None
        email = request.form['useremail']
        password = request.form['userpass']
        cur.execute("SELECT COUNT(1) FROM USER WHERE Email = %s;", [email])
        if cur.fetchone()[0]:
            cur.execute("SELECT Username, Password, UserType, Approved FROM USER WHERE Email = %s;", [email])
            for row in cur.fetchall():
                if password == row[1] and row[3] == 1:
                    session['logged_in'] = True
                    session['username'] = row[0]
                    session['usertype'] = row[2]
                    #user_type = row[2]
                else:
                    error = "Invalid Credential"
        else:
            error = "User not exist"
        if error:
            return redirect(url_for('login_page', error=error))
        else:
            return redirect(url_for('choose_function'))
    else:
        error = request.args.get('error')
        return render_template('login.html', error=error)

@application.route('/choosefunction', methods=['GET', 'POST'])
def choose_function():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    curType = session.get('usertype')
    print curType
    if request.method == 'POST':
        if request.form['action'] == 'Pending Data Point':
            return redirect(url_for('pending_datapoint'))
        elif request.form['action'] == 'Pending City Official Accounts':
            return redirect(url_for('pending_account'))
        elif request.form['action'] == 'Filter/Search POI':
            return redirect(url_for('view_poi'))
        else:
            return redirect(url_for('poi_report'))
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
    sqlHead = 'select * from citystate'
    cur.execute(sqlHead)
    rows = [[str(item) for item in results] for results in cur.fetchall()]

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
            return render_template('signup.html', error=error, rows=rows)

        return redirect(url_for('login_page'))
    else:
        return render_template('signup.html', rows=rows)

@application.route('/newdatapoint', methods=['GET','POST'])
def new_datapoint():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

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
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    error = None
    message = None
    sqlHead = 'select * from citystate'
    cur.execute(sqlHead)
    rows = [[str(item) for item in results] for results in cur.fetchall()]
    list1 = []
    list2 = []
    for name in rows:
        list1.append(name[0])
        list2.append(name[1])
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
            return render_template('newlocation.html', message=message, error=error, rows=rows)
        except Exception, e:
            print str(e)
            error = 'Input Error!!'
            message = None
            return render_template('newlocation.html', error=error, rows=rows)
    else:
        error = None
        return render_template('newlocation.html', rows=rows)

@application.route('/pendingdatapoint', methods=['GET', 'POST'])
def pending_datapoint():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

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
                conn.commit()
        else:
            for value in checklist:
                print value
                index = int(value)
                cur.execute("UPDATE DATAPOINT SET Accepted = 1 WHERE PLocation_Name = %s AND DateRecorded = %s;", [entries[index][0], entries[index][3]])
                conn.commit()
        return redirect(url_for('pending_datapoint'))
    else:
        return render_template('pendingdatapoint.html', entries=entries)

@application.route('/pendingaccount', methods=['GET', 'POST'])
def pending_account():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

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
                conn.commit()
        else:
            for value in checklist:
                print value
                index = int(value)
                cur.execute("UPDATE USER SET Approved = 1 WHERE Email = %s;", [entries[index][1]])
                conn.commit()
        return redirect(url_for('pending_account'))
    else:
        return render_template('pendingaccount.html', entries=entries)

@application.route('/viewpoi', methods=['GET','POST'])
def view_poi():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

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
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        location = request.form['plocation_name']
        if request.form['action'] == 'filter':
            datatype = request.form['data_type']
            StartValue = request.form['StartValue']
            EndValue = request.form['EndValue']
            StartDate = request.form['StartDate']
            EndDate = request.form['EndDate']

            if StartValue != "" and EndValue != "" and StartDate != "" and EndDate != "":
                cur.execute("SELECT DType, Data_Value, DateRecorded FROM DATAPOINT WHERE (DateRecorded >= %s AND DateRecorded < %s) AND (Data_Value >= %s AND Data_Value < %s) AND DType = %s AND PLocation_Name = %s;", (StartDate, EndDate, StartValue, EndValue, datatype, location))
            elif StartDate != "" and EndDate != "":
                cur.execute("SELECT DType, Data_Value, DateRecorded FROM DATAPOINT WHERE (DateRecorded >= %s AND DateRecorded < %s) AND DType = %s AND PLocation_Name = %s;", (StartDate, EndDate,  datatype, location))
            elif StartValue != "" and EndValue != "":
                cur.execute("SELECT DType, Data_Value, DateRecorded FROM DATAPOINT WHERE (Data_Value >= %s AND Data_Value < %s) AND DType = %s AND PLocation_Name = %s;", (StartValue, EndValue, datatype, location))
            else:
                cur.execute("SELECT DType, Data_Value, DateRecorded FROM DATAPOINT WHERE DType = %s AND PLocation_Name = %s;", (datatype, location))

            entries = cur.fetchall()

            cur.execute("SELECT Flag FROM POI WHERE Location_Name = %s;", (location))
            flag = cur.fetchall()
            if flag[0][0] == 0:
                boo = "Not Flagged"
            else:
                boo = "Flagged"
            return render_template('poidetail.html', entries=entries, plocation_name=location, flag=boo)

        else:
            cur.execute("UPDATE POI SET Flag = 1, Date_Flagged = CURDATE() WHERE Location_Name = %s;", (location))
            conn.commit()
            cur.execute("SELECT DType, Data_Value, DateRecorded FROM DATAPOINT WHERE PLocation_Name = %s;", (location))
            entries = cur.fetchall()

            cur.execute("SELECT Flag FROM POI WHERE Location_Name = %s;", (location))
            flag = cur.fetchall()
            if flag[0][0] == 0:
                boo = "Not Flagged"
            else:
                boo = "Flagged"
            return render_template('poidetail.html',plocation_name=location, flag=boo)

    else:
        location = request.args.get('plocation_name')
        cur.execute("SELECT DType, Data_Value, DateRecorded FROM DATAPOINT WHERE PLocation_Name = %s;", (location))
        entries = cur.fetchall()
        #entries = request.args.get('entries')
        cur.execute("SELECT Flag FROM POI WHERE Location_Name = %s;", (location))
        flag = cur.fetchall()
        if flag[0][0] == 0:
            boo = "Not Flagged"
        else:
            boo = "Flagged"
        return render_template('poidetail.html', entries=entries, plocation_name=location, flag=boo)

@application.route('/poireport', methods=['GET'])
def poi_report():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    mold = "mold"
    airquality = "airquality"

    sql2 = '(select t2.PLocation_Name, t3.PCity, t3.PState, t1.mmin, t1.mavg, t1.mmax, t2.aqmin, t2.aqavg, t2.aqmax, Cm + Caq, Flag from ((select PLocation_Name, MIN(Data_Value) as mmin, AVG(Data_Value) as mavg, MAX(Data_Value) as mmax, COUNT(*) as Cm from DATAPOINT as A where Dtype = \'' + mold + '\' group by PLocation_Name) t1 right join (select PLocation_Name, MIN(Data_Value) as aqmin, AVG(Data_Value) as aqavg, MAX(Data_Value) as aqmax, COUNT(*) as Caq from DATAPOINT as A where Dtype = \'' + airquality + '\' group by PLocation_Name) t2 on t1.PLocation_Name = t2.PLocation_Name) join (select Location_Name, PCity, PState, Flag from POI) t3 on t2.PLocation_Name = t3.Location_Name)'

    sql3 = '(select t4.PLocation_Name, t6.PCity, t6.PState, t4.mmin, t4.mavg, t4.mmax, t5.aqmin, t5.aqavg, t5.aqmax, Cm + Caq, Flag from ((select PLocation_Name, MIN(Data_Value) as mmin, AVG(Data_Value) as mavg, MAX(Data_Value) as mmax, COUNT(*) as Cm from DATAPOINT as A where Dtype = \'' + mold + '\' group by PLocation_Name) t4 left join (select PLocation_Name, MIN(Data_Value) as aqmin, AVG(Data_Value) as aqavg, MAX(Data_Value) as aqmax, COUNT(*) as Caq from DATAPOINT as A where Dtype = \'' + airquality + '\' group by PLocation_Name) t5 on t4.PLocation_Name = t5.PLocation_Name) join (select Location_Name, PCity, PState, Flag from POI) t6 on t4.PLocation_Name = t6.Location_Name)'

    sql1 = sql3 + ' union ' + sql2
    cur.execute(sql1)
    drows = [[str(item) for item in results] for results in cur.fetchall()]

    sql4 = 'select PLocation_Name, COUNT(*) from DATAPOINT group by PLocation_Name'
    cur.execute(sql4)
    crows = [[str(item) for item in results] for results in cur.fetchall()]

    for item in drows:
        for c in crows:
            if item[0] == c[0]:
                item[9] = c[1]
        if item[10] == '0':
            item[10] = False
        elif item[10] == '1':
            item[10] = True

    return render_template('poireport.html', drows=drows)


application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()