from io import TextIOWrapper
from flask import Flask, render_template, redirect, url_for, flash, request
from connector import MySQLSession

import json

class MySQLWebApplication(Flask):
    
    def __init__(self):

        self.mysqlSession: MySQLSession = None
        
        self.recordFilePaths: dict = {
            "Faculty": "./CSV Files/Faculties.csv",
            "Department": "./CSV Files/Departments.csv",
            "Title": "./CSV Files/Titles.csv",
            "Teaching Staff": "./CSV Files/Teaching Staff.csv",
            "Student": "./CSV Files/Students.csv",
            "Course": "./CSV Files/Courses.csv",
            "Student Course": "./CSV Files/Student Courses.csv",
        }

        super().__init__(import_name=__name__, template_folder='./HTML Files/', static_folder='./CSS Files/')
        self.secret_key = b'-QfR{^]A$81%"|X,O0r~'
        self.config['MYSQL_DATABASE_URI'] = None

        self._route_setup(self)
    
    @staticmethod
    def _route_setup(self):
        
        @self.route('/', methods=['GET', 'POST'])
        def homepage():
            
            if request.method != 'POST':
                return render_template("homepage.html")
            
            connectionMethod = request.form['connectionMethod']

            match connectionMethod:
                
                case "manualConnect":
                    return redirect(url_for("manual_connect"))
                
                case "configFileConnect":
                    return redirect(url_for("config_connect"))
    
        @self.route('/manual_connect', methods=['GET', 'POST'])
        def manual_connect():
            
            if request.method != 'POST':
                return render_template("manual_connect.html")

            hostname = request.form['hostname']
            username = request.form['username']
            password = request.form['password']
            database = request.form['database']
            
            try:
                mysqlSession = MySQLSession(hostname, username, password, database)

                if mysqlSession.session_is_connected():
                    flash("Connection Succesful!", 'success')
                    return redirect(url_for("main_menu"))
            except Exception as err:
                flash(f"Error: {err}", 'danger')

            return render_template("manual_connect.html")
        
        @self.route('/config_connect', methods=['GET', 'POST'])
        def config_connect():
            
            configFile: TextIOWrapper
            connectionConfig: dict
            
            if request.method != 'POST':
                return render_template("config_connect.html")

            configFile = request.files['configFile']

            if configFile is not None:
                connectionConfig = json.load(configFile)

            try:
                mysqlSession = MySQLSession(**connectionConfig)

                if mysqlSession.session_is_connected():
                    flash("Connection Succesful!", 'success')
                    return redirect(url_for("main_menu"))
            except Exception as err:
                flash(f"Error: {err}", 'danger')
            
            return render_template("config_connect.html")
        
        @self.route('/main_menu', methods=['GET', 'POST'])
        def main_menu():
            
            if request.method != 'POST':
                return render_template("main_menu.html")
            
            mainMenuOption = request.form['mainMenuOption']

            match mainMenuOption:
                
                case "dataEntry":
                    return redirect(url_for("data_entry_menu"))
                
                case "reportGeneration":
                    return redirect(url_for("report_generation_menu"))

        @self.route('/data_entry_menu', methods=['GET', 'POST'])
        def data_entry_menu():
            return f"Data Entry Menu"

        @self.route('/table_insert/<tableName>', methods=['GET', 'POST'])
        def table_insert(tableName: str):
            return f"Table Name: {tableName}"
        
        @self.route('/table_update/<tableName>', methods=['GET', 'POST'])
        def table_update(tableName: str):
            return f"Table Name: {tableName}"

        @self.route('/table_delete/<tableName>', methods=['GET', 'POST'])
        def table_delete(tableName: str):
            return f"Table Name: {tableName}"
        
        @self.route('/report_generation_menu')
        def report_generation_menu():
            return "Report Generation Menu"
        
if __name__ == '__main__':
    app = MySQLWebApplication()
    app.run(debug=True)