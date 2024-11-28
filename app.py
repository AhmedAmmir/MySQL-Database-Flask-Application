from io import TextIOWrapper
from flask import Flask, render_template, redirect, url_for, flash, request
from connector import MySQLSession

import json

class MySQLWebApplication(Flask):
    
    def __init__(self):

        self.mysqlSession: MySQLSession = None

        super().__init__(import_name=__name__, template_folder='./HTML Files/')
        self.secret_key = b'-QfR{^]A$81%"|X,O0r~'
        self.config['MYSQL_DATABASE_URI'] = None

        self._route_setup(self)
    
    @staticmethod
    def _route_setup(self):
        
        @self.route('/')
        @self.route('/')
        def homepage():
            return render_template("homepage.html")
    
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

            configFile = request.files['config_file']

            if configFile is not None:
                connectionConfig = json.load(configFile)

            self.mysqlSession = MySQLSession(**connectionConfig)

            try:
                if self.mysqlSession.session_is_connected():
                    flash("Connection Succesful!", 'success')
                    return redirect(url_for("main_menu"))
            except Exception as err:
                flash(f"Error: {err}", 'danger')
            
            return render_template("config_connect.html")
        
        @self.route('/main_menu')
        def main_menu():
            return render_template("main_menu.html")
        
        @self.route('/data_entry_menu')
        def data_entry_menu():
            return "Data Entry Menu"
        
        @self.route('/report_generation_menu')
        def report_generation_menu():
            return "Report Generation Menu"
        
    def session_init(self, hostname: str, username: str, password: str, database: str):
        self.mysqlSession = MySQLSession(host=hostname, user=username, password=password, database=database)

if __name__ == '__main__':
    app = MySQLWebApplication()
    app.run(debug=True)