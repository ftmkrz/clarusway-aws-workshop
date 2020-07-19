from flask import Flask, render_template, request

app = Flask(__name__)

def milsec_to_hour(milsec):
    sec = milsec // 1000
    sec, min = sec % 60, sec // 60
    min, hour= min % 60, min // 60
    result = f"{bool(hour) * str(hour)}{bool(hour) * ' hour/s '}\
{bool(min) * str(min)}{bool(min) * ' minute/s '}\
{bool(sec) * str(sec)}{bool(sec) * ' second/s'}"

    return f'just {milsec} milisecond/s' if milsec < 1000 else result

@app.route('/', methods=['GET'])
def main_get():
    return render_template('index.html', developer_name='Fatma', not_valid=False)

@app.route('/', methods=['POST'])
def main_post():
    milsec = request.form['number']
    if milsec.isdecimal() and milsec != '0':
       return render_template('result.html', developer_name='Fatma', milliseconds=milsec, result=milsec_to_hour(int(milsec)))
    return render_template('index.html', developer_name='Fatma', not_valid=True)

if __name__ == "__main__":
    app.run('localhost', port=5000, debug=True)
    #app.run(debug=True)
    #app.run('0.0.0.0.', port=80, debug=True)