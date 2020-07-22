from flask import Flask, render_template, request

app = Flask(__name__)

def milsec(mil):
    sec = (mil // 1000)
    min = (mil // (1000 * 60)) % 60
    hr = (mil // (1000 * 60 * 60))
    
    return f'{sec} seconds {min} minutes {hr} hours'

@app.route('/', methods=['GET'])
def main_get():
    return render_template('index.html', developer_name='Fatma', not_valid=False)

@app.route('/', methods=['POST'])
def main_post():
    mil = request.form['number']
    if mil.isdecimal() and mil != '0':
       return render_template('result.html', developer_name='Fatma', milliseconds=mil, result=milsec(int(mil)))
    return render_template('index.html', developer_name='Fatma', not_valid=True)

if __name__ == "__main__":
    app.run('localhost', port=5000, debug=True)
    #app.run(debug=True)
    #app.run('0.0.0.0.', port=80, debug=True)