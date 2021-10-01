from flask import Flask,render_template,request,session
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib


app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/Uploadfile', methods=['POST', 'GET'])
def upload1():
    if request.method == "POST":
        dataset = request.files['file']
        filename = dataset.filename
        file = "dataset\\" + filename
        session['dataset'] = file
        return render_template('upload.html', msg="success")
    return render_template('upload.html')

@app.route('/view')
def viewdata():
    datafile = session["dataset"]
    df = pd.read_csv(datafile)

    return render_template('viewdata.html',data=df.to_html())


@app.route('/splitdataset',methods=['POST','GET'])
def splitdataset():
    global x_train,x_test,y_train,y_test
    if request.method == 'POST':
        testsize = request.form['test_size']
        testsize = float(testsize)
        datafile = session.get('dataset')
        df = pd.read_csv(datafile)
        x = df.iloc[:,1:]
        y = df.iloc[:,0]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=testsize)

        lentr = len(x_train)
        lentes = len(x_test)
        return render_template('splitdata.html', msg1="done",tr1 =lentr,te1 = lentes)
    return render_template('splitdata.html')



@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/prediction1',methods = ['POST','GET'])
def prediction1():
    a = []
    if request.method == "POST":
        date = (request.form['date'])
        prevclose = (request.form['prevclose'])
        open = (request.form['open'])
        high = (request.form['high'])
        low = (request.form['low'])
        last = (request.form['last'])
        close = (request.form['close'])

        a.extend([date,prevclose,open,high,low,last,close])
        model = joblib.load("bumodel.pkl")
        y_pred = model.predict([a])
        return render_template('prediction.html',msg = "done",op=y_pred)
    return render_template("prediction.html")




if __name__ == '__main__':
    app.run(debug=True)
