
from flask import Flask,request,render_template
import  Model

app = Flask(__name__)
model = Model.Model()

@app.get("/")
def base():
    model.init()
    return render_template("index.html")

@app.route("/ask",methods=['POST'])
def chat():
    question = request.form.get('question')
    response = model.query_response(question)
    return render_template('index.html',result = response)



if __name__ == "__main__":
    app.run(debug=True)