from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def page():
    return render_template('attendanceform.html')


@app.route("/viewAttendance", methods=['GET', 'POST'])
def page2():
    return render_template('displayEmployeeAttendance.html')


@app.route("/viewAllAttendance", methods=['GET', 'POST'])
def page3():
    return render_template('allAttendance.html')


@app.route("/AddAttendance", methods=['POST'])
def AddAttendance():

    attendance_id = request.form['attendance_id']
    emp_name = request.form['emp_name']
    date = request.form['date']
    time_in = request.form['time_in']
    time_out = request.form['time_out']
    benefit = request.form['benefit']

    insert_sql = "INSERT INTO timeandattendance VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:

        cursor.execute(insert_sql, (attendance_id, emp_name, date, time_in, time_out, benefit))
        db_conn.commit()

    finally:
        cursor.close()

        print("all modification done...")
        return render_template('attendanceform.html')


@app.route("/DisplayAll", methods=['POST'])
def DisplayAll():
    cursor = db_conn.cursor()
    cursor.execute("SELECT attendance_id, emp_name, date, time_in, time_out, benefit from timeandattendance")
    a = cursor.fetchall()
    return render_template('allAttendance.html', data=a)


@app.route("/DisplayAttendance", methods=['POST'])
def DisplayAttendance():

    attendanceid = request.form['attendanceid']
    select_sql = "SELECT attendance_id, emp_name, date, time_in, time_out, benefit from timeandattendance WHERE attendance_id = %s"
    cursor = db_conn.cursor()

    cursor.execute(select_sql, (attendanceid))
    db_conn.commit()

    for a in cursor:
        attendance_id = a[0]
        emp_name = a[1]
        date = a[2]
        time_in = a[3]
        time_out = a[4]
        benefit = a[5]

    cursor.close()
    return render_template('displayEmployeeAttendance.html', attendance_id=attendance_id, emp_name=emp_name,
                           date=date, time_in=time_in, time_out=time_out, benefit=benefit)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
