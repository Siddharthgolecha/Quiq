from cgitb import html
from distutils.log import debug
from flask import Flask, render_template, request


app= Flask(__name__)

@app.route('/home')
def interface():
    return render_template('interface.html')

@app.route('/pass', methods=["post"])
def getvalue():
    key1=request.form['key1']
    key2=request.form['key2']
    file=open('keys.txt', 'w')
    file.write(key1 + '\n')
    file.write(key2 + '\n')
    file.close()
    return render_template('pass.html', k1=key1, k2=key2)

if __name__ == '__main__':
    app.run(debug=True)

