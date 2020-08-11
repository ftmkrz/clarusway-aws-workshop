from flask import Flask, render_template, url_for, request
from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = os.getenv("DB_HOST", 'last-test.cmo1zcgk7qya.us-east-1.rds.amazonaws.com')
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Admin12345'
app.config['MYSQL_DATABASE_DB'] = 'phonebook'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

def find_number(keyword):
    query = f"""
    SELECT * FROM persons WHERE name like '%{keyword}%';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    persons= [{"name":row[1], "number":row[2]} for row in result]
   
    if not any(persons):
        persons = [{"name":'Not found.', "number":'Not Found.'}]
    return persons

def add_number(name, number):
    query = f"""
    SELECT * FROM persons WHERE name like '{name}';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    response = 'Error occurred..'
    if name == " " or number == " ":
        response = 'person or number can not be emtpy!!'
    elif not any(result):
        insert = f"""
        INSERT INTO persons(name,number) 
        VALUES ('{name}', '{number}');
        """
        cursor.execute(insert)
        connection.commit()
        response = f'{name} successfully added to phonebook'
    else:
        response = f'{name} already exits.'
    return response
def update(name, number):
    query = f"""
    SELECT * FROM persons WHERE name like '{name}';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        query=f""" 
        UPDATE persons SET number='{number}' where name like '{name}';
        """
        cursor.execute(query)
        connection.commit()
        return f"Phone number for {name} successfully updated with {number}"
    else:
        return f"There isn't any contact with name {name}"

def delete(name):
    query=f"""
    SELECT * FROM persons WHERE name='{name}';
    """
    cursor.execute(query)
    result=cursor.fetchall()
    if result:
        delete=f"""
        DELETE FROM persons
        WHERE name like '{name}';
        """
        cursor.execute(delete)
        connection.commit()
        response=f"{name} successfully deleted from phonebook"
        return response
    else:
        response=f"{name} doesn't exist in the phonebook"
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        name=request.form['username'].strip()
        persons=find_number(name)
        return render_template("index.html", developer_name="Fatma", persons=persons, show_result=True, keyword=name )
    else:
        return render_template("index.html", developer_name="Fatma", show_result=False)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method=='POST':
        name=request.form['username'].title().strip()
        number=request.form['phonenumber']
        if (name.replace(" ", "")).isalpha() and number.isdigit():
            result=add_number(name, number)
            return render_template("add-update.html", developer_name='Fatma', action_name="add phonebook", result=result, show_result=True)
        elif name is None or name.strip()=="":
            return render_template("add-update.html", developer_name="Fatma", action_name="add phonebook", not_valid=True, message="Name can not be empty")    
        elif name.isdigit():
            return render_template("add-update.html", developer_name="Fatma", action_name="add phonebook", not_valid=True, message="Name of person should be text")    
        elif not (name.replace(" ", "")).isalpha():
            return render_template("add-update.html", developer_name="Fatma", action_name="add phonebook", not_valid=True, message="Name of person should be text")    
        elif number==" ":
            return render_template("add-update.html", developer_name="Fatma", action_name="add phonebook", not_valid=True, message="Number can not be empty")    
        elif not number.isdigit():
            return render_template("add-update.html", developer_name="Fatma", action_name="add phonebook", not_valid=True, message="Phone number should be in numeric format")       
    else:
        return render_template("add-update.html", developer_name="Fatma", action_name="add phonebook", show_result=False)  
@app.route('/update', methods=['GET','POST'])  
def update_number():
    if request.method=='POST':
        name=request.form['username'].title()
        number=request.form['phonenumber']
        if (name.replace(" ", "")).isalpha() and number.isdigit():
            result=update(name, number)
            return render_template("add-update.html", developer_name='Fatma', action_name="update phonebook", result=result, show_result=True)
        elif name==" ":
            return render_template("add-update.html", developer_name="Fatma", action_name="update phonebook", not_valid=True, message="Name can not be empty")    
        elif number==" ":
            return render_template("add-update.html", developer_name="Fatma", action_name="update phonebook", not_valid=True, message="Number can not be empty")    
        elif not number.isdigit():
            return render_template("add-update.html", developer_name="Fatma", action_name="update phonebook", not_valid=True, message="Phone number should be in numeric format")       
    else:
        return render_template("add-update.html", developer_name="Fatma", action_name="update phonebook", show_result=False)  
        
@app.route('/delete', methods=['GET','POST']) 
def delete_contact():
    if request.method=='POST':
        name=request.form['username'].title().strip()
        if name=="" or name is None:
            return render_template("delete.html", developer_name="Fatma", not_valid=True, message="Name can not be empty")    
        result=delete(name)
        return render_template("delete.html", developer_name="Fatma", show_result=True, result=result)
    else:
        return render_template("delete.html", developer_name="Fatma", show_result=False)  

if __name__=='__main__':
    # init_pb_db()
    app.run(host='0.0.0.0', port=80)
    # app.run(debug=True)
