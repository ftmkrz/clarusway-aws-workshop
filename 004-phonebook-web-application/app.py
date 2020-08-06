from flask import Flask, render_template, url_for, request
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'call-mysql-db-server.cbanmzptkrzf.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Admin123'
app.config['MYSQL_DATABASE_DB'] = 'phone_book'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

def init_phonebook_db():
    drop_table = 'DROP TABLE IF EXISTS phonebook;'
    phonebook_table = '''
    CREATE TABLE phonebook(
        id INTEGER NOT NULL AUTO_INCREMENT,
        name varchar(50) NOT NULL,
        number varchar(13),
        PRIMARY KEY(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    '''
    data = '''
    INSERT INTO phonebook(name, number)
    VALUES
    ('John Doe', '(333)666-4422'),
    ('Jack Black', '(222)777-9955');
    '''
cursor.execute(drop_table)
cursor.execute(phonebook_table)
cursor.execute(data)

def find(keyword):
    query = f"""
    SELECT * FROM phonebook WHERE name like '%{keyword}%';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    phonebook = [(row[1], row[2]) for row in result]
    if not any(phonebook):
        phonebook = [('Not found.', 'Not Found.')]
    return phonebook

def add(name, number):
    query = f"""
    SELECT * FROM phonebook WHERE name like '{name}';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    response = 'Error occurred..'
    if name == " " or number == " ":
        response = 'Name or number can not be emtpy!!'
    elif not any(result):
        insert = f"""
        INSERT INTO phonebook(name, number)
        VALUES ('{name}', '{number}');
        """
        cursor.execute(insert)
        response = f'Name {name} added successfully'
    else:
        response = f'Name {name} already exits.'
    return response

def delete(name):
    query = f"""
    SELECT * FROM phonebook WHERE name like '{name}';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        delete=f"""
        DELETE FROM phonebook WHERE name like '{name}';
        """
        cursor.execute(delete)
        response = f'Name {name} deleted succesfully'
        return response
    else:
        response = f'Name {name} does not exist'
    return response

@app.route('/', methods = ['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('index.html', developer_name ='Fatma', show_result=False)
    if request.method == 'POST':
        keyword = request.form['username']
        persons = find(keyword)
        return  render_template('index.html', developer_name='Fatma', show_result=True, persons=persons, keyword=keyword )
    else:
        return  render_template('index.html', developer_name='Fatma', show_result=False)
@app.route('/', methods = ['GET','POST'])
def add():
    if request.method == 'POST':
        keyword = request.form['username'].title()
        number = request.form['number']
        if keyword.replace(" ", "").isalpha() and number.isdigit():
            result = add(name, number)
            return render_template('add-update.html', developer_name='Fatma', action_name='add', result=result, show_result=True)
        elif keyword == " " and keyword.isdigit():
            return render_template('add-update.html', developer_name='Fatma', not_valid=True, action_name='add', message="Error")
        elif number == " " and number.isalpha():
            return render_template('add-update.html', developer_name='Fatma', not_valid=True, action_name='add', message="Error")
    else:
        return render_template('add-update.html', developer_name='Fatma', action_name='add', show_result=False)
@app.route('/', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        keyword = request.form['username'].title()
        result = delete(name)
        if result == None:
             return render_template('delete.html', developer_name='Fatma', not_valid=True, message=f'There is no any contact with name {name}')
        else:
            return render_template('delete.html', developer_name='Fatma', show_result=True, result=result)
    else:
        return render_template('delete.html', developer_name='Fatma', show_result=False)  

if __name__ == '__main__':
    init_phonebook_db()
    app.run('0.0.0.0', port = 80, debug = True)
    #app.run(debug=True)
    #app.run('localhost', port=5000, debug=True)


    






