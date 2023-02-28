from flask import Flask,jsonify
from flask import request,render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)





@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  json_data = request.json
  print(json_data)
  a_value = json_data["data"] #la palabra correcta desde de correr el algoritmo
  b_value =  corrector(a_value)
  print(b_value)
  return jsonify(value=b_value)

if __name__ == "__main__":
  app.run(port=5000, debug=True)