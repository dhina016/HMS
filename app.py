import os, time
from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, session, logging, jsonify
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from form import LoginForm, CreatePatient, UpdatePatient, DeletePatient


app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'hms'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    print(sha256_crypt.encrypt('Exec@1'))
    cur.execute("SELECT * from users WHERE username = 'executive' AND isDel = '0' ")
    detail = cur.fetchone()
    return jsonify(detail)

#login
@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        user_pass = request.form['password']
        print(username,user_pass)
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s AND isDel = '0' ",[username])
        print(result)
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            userlevel = data['level']
            if userlevel == 'ade':
                permission = 'Excecutive'
            elif userlevel == 'pharmacist':
                permission = 'Pharamacist'
            elif userlevel == 'dse':
                permission = 'Diagnosist'

            if sha256_crypt.verify(user_pass, password):
                session['logged_in']    = True
                session['userlevel']    = userlevel
                session['username']     = username
                session['permission']   = permission
                print(session)
                flash('Logged In Successfully!!!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid Login', 'danger')
                return redirect(url_for('login'))
        else:
            flash('User Not Found', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in',False)
    session.pop('permission',False)
    session.pop('username',False)
    session.pop('userlevel',False)
    return jsonify('success')


#dashboard
@app.route('/dashboard')
def dashboard():
    title = ['Dashboard1', 'This is dashboard', '']
    return render_template('createpatient.html',title=title)


#Customer section
@app.route('/createpatient',methods=["GET","POST"])
def createpatient():
    if session.get('logged_in'):
        if session.get('userlevel') == 'ade':
            title = ['Create PAtient', 'This is create Patient', '']  
            form = CreatePatient()
            cur = mysql.connection.cursor()
            if request.method == 'POST' and form.validate():
                ssnid = request.form['ssnid']
                generate = str(int(time.time()))
                patientid = int(generate[0:1]+generate[2:])
                patientname = request.form['patientname']
                address = request.form['address']
                state = request.form['state']
                city = request.form['city']
                age = request.form['age']
                doj = datetime.today().strftime('%Y-%m-%d')
                rtype = request.form['type']
                checkpatient = cur.execute("select SSNID from patient where SSNID = %s ",[ssnid])
                if checkpatient  == False:
                    if(cur.execute('''Insert into patient (ssnid, patientid, patientname, address, state, city, age, doj, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', ( ssnid, patientid, patientname, address, state, city, age, doj, rtype))):
                        mysql.connection.commit()
                        cur.close()
                        flash('Created Successfully!!', 'success')
                        return redirect(url_for('createpatient'))
                    else:
                        flash('Something went wrong', 'danger')
                        return redirect(url_for('createpatient'))
                else:
                    flash('SSN ID already exist', 'danger')
                    return redirect(url_for('createpatient'))
            return render_template('createpatient.html',title=title,form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))



#Customer section
@app.route('/updatepatient',methods=["GET","POST"])
def updatepatient():
    if session.get('logged_in'):
        if session.get('userlevel') == 'ade':
            title = ['Update Patient', 'This is create Patient', '']  
            form = UpdatePatient()
            cur = mysql.connection.cursor()
            if request.method == 'POST' and form.validate():
                patientid = request.form['patientid']
                patientname = request.form['patientname']
                address = request.form['address']
                age = request.form['age']
                status = request.form['pstatus']
                check = cur.execute("UPDATE patient SET patientname = %s, address = %s, age = %s, status = %s where patientid = %s", ( patientname, address, age, status, patientid))
                if(check):
                    mysql.connection.commit()
                    cur.close()
                    flash('Updated Successfully!!', 'success')
                    return redirect(url_for('updatepatient'))
                else:
                    flash('Something went wrong', 'danger')
                    return redirect(url_for('updatepatient'))
            return render_template('updatepatient.html',title=title,form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


#Customer section
@app.route('/deletepatient',methods=["GET","POST"])
def deletepatient():
    if session.get('logged_in'):
        if session.get('userlevel') == 'ade':
            title = ['Delete Patient', 'This is Delete Patient', '']  
            form = DeletePatient()
            cur = mysql.connection.cursor()
            if request.method == 'POST' and form.validate():
                patientid = request.form['patientid']
                check = cur.execute("UPDATE patient SET isDel = %s where patientid = %s", ( '1', patientid))
                if(check):
                    mysql.connection.commit()
                    cur.close()
                    flash('Deleted Successfully!!', 'success')
                    return redirect(url_for('deletepatient'))
                else:
                    flash('Something went wrong', 'danger')
                    return redirect(url_for('deletepatient'))

            return render_template('deletepatient.html',title=title,form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


#Customer section
@app.route('/viewpatient',methods=["GET","POST"])
def viewpatient():
    if session.get('logged_in'):
        if session.get('userlevel') == 'ade':
            title = ['View Patient', 'This is View Patient', ''] 
            cur = mysql.connection.cursor()
            cur.execute("select * from patient where isDel = '0' ")
            detail = cur.fetchall()
            return render_template('viewpatient.html',title=title, detail=detail)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


#Customer section
@app.route('/singlepatient',methods=["GET","POST"])
def singlepatient():
    if session.get('logged_in'):
        if session.get('userlevel') == 'ade':
            title = ['View Patient', 'This is create Patient', '']
            form = DeletePatient()
            return render_template('singlepatient.html',title=title, form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))




@app.route('/getpatientdetail',methods=["GET"])
def getpatientdetail():
    if session.get('logged_in'):
        if  (session.get('userlevel') == 'ade'):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from patient where patientid = %s AND isDel = '0'", [ request.args.get('pid') ])
            detail = cur.fetchone()
            return jsonify(detail)
        else:
            return jsonify(None)
    else:
        return jsonify(None)


if __name__ == "__main__":
    app.secret_key = 'hms-secretkey'
    app.run(debug = True)