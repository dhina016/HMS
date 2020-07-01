import os, time
from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, session, logging, jsonify
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from form import LoginForm, CreatePatient, UpdatePatient, DeletePatient, Medicine, DeleteMedicine, Diagnosis, DeleteDiagnosis


app = Flask(__name__)
app.secret_key = 'hms-secretkey'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'hms'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def home():
    return redirect(url_for('login'))

#login
@app.route('/login',methods=["GET","POST"])
def login():
    if session.get('logged_in'):
        return redirect(url_for('logout'))
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
    return redirect(url_for('login'))


#dashboard
@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        title = ['Dashboard', 'This is Dashboard', ''] 
        cur = mysql.connection.cursor()
        cur.execute("select count(*) as total from patient where isDel = '0' ")
        patient = cur.fetchone()
        cur.execute("select count(*) as total from medicine where isDel = '0' ")
        medicine = cur.fetchone()
        cur.execute("select count(*) as total from diagnosis where isDel = '0' ")
        diagnosis = cur.fetchone()
        return render_template('dashboard.html',title=title, patient=patient, medicine=medicine, diagnosis=diagnosis)
    else:
        flash('Session Timeout', 'danger')
        return redirect(url_for('login'))


#Customer section
@app.route('/createpatient',methods=["GET","POST"])
def createpatient():
    if session.get('logged_in'):
        if session.get('userlevel') == 'ade':
            title = ['Create Patient', 'This is create Patient', '']  
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
            title = ['Update Patient', 'This is update Patient', '']  
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
        if session.get('userlevel') == 'ade' or session.get('userlevel') == 'dse':
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
        if session.get('userlevel') == 'ade' or session.get('userlevel') == 'dse':
            title = ['View Patient', 'This is View Patient', '']
            form = DeletePatient()
            return render_template('singlepatient.html',title=title, form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))



#Customer section
@app.route('/generatebill/<id>',methods=["GET","POST"])
def generatebill(id):
    if session.get('logged_in'):
        if session.get('userlevel') == 'ade':
            title = ['Generate Bill', 'This is Generate Bill', '']
            cur = mysql.connection.cursor()
            if request.method == 'POST':
                id = request.form['patientid']
                status = 'discharged'
                check = cur.execute("UPDATE patient SET status = %s where patientid = %s", (status, id))
                if(check):
                    cur.execute("select * from bill where checkbill = 'not' AND patientid = %s",[id])
                    bill = cur.fetchall()
                    if(bill):
                        status = 'billed'
                        date = datetime.today().strftime('%Y-%m-%d')
                        check = cur.execute("UPDATE bill SET checkbill = %s, billdate = %s where patientid = %s", (status, date, id))
                        print(check)
                        if(check):
                            mysql.connection.commit()
                            flash('Patient Discharged', 'success')
                            return redirect(url_for('viewpatient'))
                        else:
                            flash('Something went wrong', 'danger')
                            return redirect(url_for('viewpatient'))
                    else:
                        mysql.connection.commit()
                        flash('Patient Discharged', 'success')
                        return redirect(url_for('viewpatient'))
                else:
                    flash('Something went wrong', 'danger')
                    return redirect(url_for('viewpatient'))
            extra = {}
            title = ['View Patient', 'This is create Patient', '']
            date = datetime.today().strftime('%Y-%m-%d')
            cur.execute("select *, DATEDIFF (%s, doj) as totaldate  from patient where isDel = '0' AND patientid = %s AND status='active'",[date,id])
            patient = cur.fetchone()
            cur.execute("select * from bill where checkbill = 'not' AND patientid = %s",[id])
            bill = cur.fetchall()
            if(patient):
                if(patient['totaldate'] <= 0):
                    patient['totaldate'] = 1
                if(patient['type'] == 'semi'):
                    extra['rtype'] = 'Semi sharing'
                    extra['price'] = 4000.0
                elif(patient['type'] == 'general'):
                    extra['rtype'] = 'General ward'
                    extra['price'] = 2000.0
                elif(patient['type'] == 'single'):
                    extra['rtype'] = 'Single Room'
                    extra['price'] = 8000.0
                extra['date'] = date
                total = 0
                for i in bill:
                    total += (int(i['quantity'])*float(i['rate']))
                extra['total'] = total+ (float(extra['price'])*float(patient['totaldate']))
            return render_template('generatebill.html',title=title, patient=patient, bill=bill, extra=extra)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))




@app.route('/getpatientdetail',methods=["GET"])
def getpatientdetail():
    if session.get('logged_in'):
        if(session.get('userlevel') == 'ade' or session.get('userlevel') == 'dse'):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from patient where patientid = %s AND isDel = '0' ", [ request.args.get('pid') ])
            detail = cur.fetchone()
            return jsonify(detail)
        else:
            return jsonify(None)
    else:
        return jsonify(None)

#medicine

#Customer section
@app.route('/createmedicine',methods=["GET","POST"])
def createmedicine():
    if session.get('logged_in'):
        if session.get('userlevel') == 'pharmacist':
            title = ['Create Medicine', 'This is Create Medicine', '']  
            form = Medicine()
            cur = mysql.connection.cursor()
            if request.method == 'POST' and form.validate():
                medicinename = request.form['medicinename']
                quantity = request.form['quantity']
                rate = request.form['rate']
                checkpatient = cur.execute("select medicinename from medicine where medicinename = %s ",[medicinename])
                if checkpatient  == False:
                    if(cur.execute('''Insert into medicine (medicinename, quantity, rate) VALUES (%s, %s, %s)''', ( medicinename, quantity, rate ))):
                        mysql.connection.commit()
                        cur.close()
                        flash('Created Successfully!!', 'success')
                        return redirect(url_for('createmedicine'))
                    else:
                        flash('Something went wrong', 'danger')
                        return redirect(url_for('createmedicine'))
                else:
                    flash('Medicine already exist', 'danger')
                    return redirect(url_for('createmedicine'))
            return render_template('createmedicine.html',title=title,form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))



#Customer section
@app.route('/updatemedicine',methods=["GET","POST"])
def updatemedicine():
    if session.get('logged_in'):
        if session.get('userlevel') == 'pharmacist':
            title = ['Update Medicine', 'This is Update Medicine', '']  
            form = Medicine()
            cur = mysql.connection.cursor()
            if request.method == 'POST' and form.validate():
                medicinename = request.form['medicinename']
                quantity = request.form['quantity']
                rate = request.form['rate']
                check = cur.execute("UPDATE medicine SET quantity = %s, rate = %s where medicinename = %s", ( quantity, rate, medicinename))
                if(check):
                    mysql.connection.commit()
                    cur.close()
                    flash('Updated Successfully!!', 'success')
                    return redirect(url_for('updatemedicine'))
                else:
                    flash('Something went wrong', 'danger')
                    return redirect(url_for('updatemedicine'))
            return render_template('updatemedicine.html',title=title,form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


#Customer section
@app.route('/deletemedicine',methods=["GET","POST"])
def deletemedicine():
    if session.get('logged_in'):
        if session.get('userlevel') == 'pharmacist':
            title = ['Delete Medicine', 'This is Delete Medicine', '']  
            form = DeleteMedicine()
            cur = mysql.connection.cursor()
            if request.method == 'POST' and form.validate():
                medicinename = request.form['medicinename']
                check = cur.execute("UPDATE medicine SET isDel = %s where medicinename = %s", ( '1', medicinename))
                if(check):
                    mysql.connection.commit()
                    cur.close()
                    flash('Deleted Successfully!!', 'success')
                    return redirect(url_for('deletemedicine'))
                else:
                    flash('Something went wrong', 'danger')
                    return redirect(url_for('deletemedicine'))

            return render_template('deletemedicine.html',title=title,form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


#Customer section
@app.route('/viewmedicine',methods=["GET","POST"])
def viewmedicine():
    if session.get('logged_in'):
        if session.get('userlevel') == 'pharmacist':
            title = ['View Medicine', 'This is View Medicine', ''] 
            cur = mysql.connection.cursor()
            cur.execute("select * from medicine where isDel = '0' ")
            detail = cur.fetchall()
            return render_template('viewmedicine.html',title=title, detail=detail)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


@app.route('/patientmedicineadd', methods=['GET','POST'])
def patientmedicineadd():
    if session.get('logged_in'):
        if session.get('userlevel') == 'pharmacist':
            title = ['Add Medcine To Patient', 'This is Add Medcine To Patient', ''] 
            cur = mysql.connection.cursor()
            cur.execute("select * from medicine where isDel = '0' AND quantity > 0")
            medicine = cur.fetchall()
            cur.execute("select * from patient where isDel = '0' ")
            patient = cur.fetchall()
            if request.method == 'POST':
                patientid = request.form['patientname']
                type = 'medicine'
                dup = []
                for i in range((len(request.form)-1)//2):
                    dup.append(request.form['group-a[{}][medicinename]'.format(i)])
                if(len(dup) != len(set(dup))):
                    flash('Duplicate medicine Found', 'danger')
                    return redirect(url_for('patientmedicineadd'))
                for i in range((len(request.form)-1)//2):
                    name = request.form['group-a[{}][medicinename]'.format(i)]
                    quantity = int(request.form['group-a[{}][quantity]'.format(i)])
                    if(cur.execute("select rate,quantity from medicine where quantity >= %s AND medicinename = %s AND isDel ='0'",[quantity, name])):
                        rate = cur.fetchone()
                        total = float(rate['rate']) * quantity
                        val = (patientid, type, name, quantity, total)
                        if(cur.execute('''Insert into bill (patientid, type, name, quantity, rate) VALUES (%s, %s, %s, %s, %s)''', ( val ))):
                            if(cur.execute("UPDATE medicine SET quantity = %s where medicinename = %s", ( int(rate['quantity'])-quantity, name  ))):
                                mysql.connection.commit()
                                flash('Added '+name, 'success')
                            else:
                                flash('Something Went Wrong', 'danger')
                                return redirect(url_for('patientmedicineadd'))
                        else:
                            flash('Something Went Wrong', 'danger')
                            return redirect(url_for('patientmedicineadd'))
                    else:
                        flash('Low Stock:'+name, 'danger')
                
                return redirect(url_for('patientmedicineadd'))
            return render_template('patientmedicine.html',title=title, medicine=medicine, patient=patient)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


@app.route('/getmedicinedetail',methods=["GET"])
def getmedicinedetail():
    if session.get('logged_in'):
        if  (session.get('userlevel') == 'pharmacist'):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from medicine where medicinename = %s AND isDel = '0'", [ request.args.get('mname') ])
            detail = cur.fetchone()
            return jsonify(detail)
        else:
            return jsonify(None)
    else:
        return jsonify(None)



#Diagnosis
@app.route('/creatediagnosis',methods=["GET","POST"])
def creatediagnosis():
    if session.get('logged_in'):
        if session.get('userlevel') == 'dse':
            title = ['Create diagnosis', 'This is Create diagnosis', '']  
            form = Diagnosis()
            cur = mysql.connection.cursor()
            if request.method == 'POST' and form.validate():
                diagnosisname = request.form['diagnosisname']
                rate = request.form['rate']
                checkpatient = cur.execute("select diagnosisname from diagnosis where diagnosisname = %s ",[diagnosisname])
                if checkpatient  == False:
                    if(cur.execute('''Insert into diagnosis (diagnosisname, rate) VALUES (%s, %s)''', ( diagnosisname, rate ))):
                        mysql.connection.commit()
                        cur.close()
                        flash('Created Successfully!!', 'success')
                        return redirect(url_for('creatediagnosis'))
                    else:
                        flash('Something went wrong', 'danger')
                        return redirect(url_for('creatediagnosis'))
                else:
                    flash('Medicine already exist', 'danger')
                    return redirect(url_for('creatediagnosis'))
            return render_template('creatediagnosis.html',title=title,form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


#Customer section
@app.route('/updatediagnosis',methods=["GET","POST"])
def updatediagnosis():
    if session.get('logged_in'):
        if session.get('userlevel') == 'dse':
            title = ['Update Diagnosis', 'This is Update Diagnosis', '']  
            form = Diagnosis()
            cur = mysql.connection.cursor()
            if request.method == 'POST' and form.validate():
                diagnosisname = request.form['diagnosisname']
                rate = request.form['rate']
                check = cur.execute("UPDATE diagnosis SET rate = %s where diagnosisname = %s", ( rate, diagnosisname))
                if(check):
                    mysql.connection.commit()
                    cur.close()
                    flash('Updated Successfully!!', 'success')
                    return redirect(url_for('updatediagnosis'))
                else:
                    flash('Something went wrong', 'danger')
                    return redirect(url_for('updatediagnosis'))
            return render_template('updatediagnosis.html',title=title,form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


#Customer section
@app.route('/deletediagnosis',methods=["GET","POST"])
def deletediagnosis():
    if session.get('logged_in'):
        if session.get('userlevel') == 'dse':
            title = ['Delete Diagnosis', 'This is Delete Diagnosis', '']  
            form = DeleteDiagnosis()
            cur = mysql.connection.cursor()
            if request.method == 'POST' and form.validate():
                diagnosisname = request.form['diagnosisname']
                check = cur.execute("UPDATE diagnosis SET isDel = %s where diagnosisname = %s", ( '1', diagnosisname))
                if(check):
                    mysql.connection.commit()
                    cur.close()
                    flash('Deleted Successfully!!', 'success')
                    return redirect(url_for('deletediagnosis'))
                else:
                    flash('Something went wrong', 'danger')
                    return redirect(url_for('deletediagnosis'))

            return render_template('deletediagnosis.html',title=title,form=form)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


#Customer section
@app.route('/viewdiagnosis',methods=["GET","POST"])
def viewdiagnosis():
    if session.get('logged_in'):
        if session.get('userlevel') == 'dse':
            title = ['View Diagnosis', 'This is View Diagnosis', ''] 
            cur = mysql.connection.cursor()
            cur.execute("select * from diagnosis where isDel = '0' ")
            detail = cur.fetchall()
            return render_template('viewdiagnosis.html',title=title, detail=detail)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


@app.route('/patientdiagnosisadd', methods=['GET','POST'])
def patientdiagnosisadd():
    if session.get('logged_in'):
        if session.get('userlevel') == 'dse':
            title = ['Add Diagnosis To Patient', 'This is Add Diagnosis To Patient', ''] 
            cur = mysql.connection.cursor()
            cur.execute("select * from diagnosis where isDel = '0'")
            diagnosis = cur.fetchall()
            cur.execute("select * from patient where isDel = '0' ")
            patient = cur.fetchall()
            if request.method == 'POST':
                print(request.form)
                patientid = request.form['patientname']
                type = 'diagnosis'
                dup = []
                for i in range(len(request.form)-1):
                    dup.append(request.form['group-a[{}][diagnosisname]'.format(i)])
                if(len(dup) != len(set(dup))):
                    flash('Duplicate diagnosis Found', 'danger')
                    return redirect(url_for('patientdiagnosisadd'))
                for i in range(len(request.form)-1):
                    name = request.form['group-a[{}][diagnosisname]'.format(i)]
                    quantity = 1
                    if(cur.execute("select rate from diagnosis where diagnosisname = %s AND isDel ='0'",[name])):
                        rate = cur.fetchone()
                        val = (patientid, type, name, quantity, float(rate['rate']))
                        if(cur.execute('''Insert into bill (patientid, type, name, quantity, rate) VALUES (%s, %s, %s, %s, %s)''', ( val ))):
                            mysql.connection.commit()
                            flash('Added '+name, 'success')
                        else:
                            flash('Something Went Wrong', 'danger')
                            return redirect(url_for('patientdiagnosisadd'))
                    else:
                        flash('Not Found:'+name, 'danger')
                
                return redirect(url_for('patientdiagnosisadd'))
            return render_template('patientdiagnosis.html',title=title, diagnosis=diagnosis, patient=patient)
        else:
            flash('Session Timeout', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Access Denied', 'danger')
        return redirect(url_for('logout'))


@app.route('/getdiagnosisdetail',methods=["GET"])
def getdiagnosisdetail():
    if session.get('logged_in'):
        if  (session.get('userlevel') == 'dse'):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from diagnosis where diagnosisname = %s AND isDel = '0'", [ request.args.get('mname') ])
            detail = cur.fetchone()
            return jsonify(detail)
        else:
            return jsonify(None)
    else:
        return jsonify(None)


@app.route('/getbilldetail',methods=["GET"])
def getbilldetail():
    if session.get('logged_in'):
        if (session.get('userlevel') == 'dse' or session.get('userlevel') == 'ade'):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from bill where patientid = %s AND type='medicine' ", [ request.args.get('mname') ])
            detail = cur.fetchall()
            return jsonify(detail)
        else:
            return jsonify(None)
    else:
        return jsonify(None)


if __name__ == "__main__":
    app.secret_key = 'hms-secretkey'
    app.run(debug = True)