from flask import Flask, request
from NF_IDS import GetPredict

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def Predict():
    content = request.get_json(force=True)
    predict = GetPredict(content)
    return str([float("{0:.4f}".format(pred)) for pred in predict])