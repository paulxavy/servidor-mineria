from flask import Flask,jsonify
from flask import request,render_template
from flask_cors import CORS
import os
import uuid

from modelo import completo
from modelo import dataframe
app = Flask(__name__)
CORS(app)





@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  # Obtiene el archivo de la solicitud
    #file = request.files['file']

    # Genera un nombre único para el archivo
    #filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]

    # Guarda el archivo en el directorio de subidas
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    json_data = request.json
    print(json_data)
    filelist = os.listdir('C:\\Users\\Martínez\\Desktop\\m-servidor\\audios') 
    df = dataframe(filelist)
    a_value = json_data["name"] #la palabra correcta desde de correr el algoritmo
    b_value =  completo(a_value, df)

    print(b_value)
    
    # Retorna una respuesta exitosa
    
    return jsonify(value=b_value)


#app.config['UPLOAD_FOLDER'] = 'C:\\Users\\Martínez\\Desktop\\m-servidor\\audios'

if __name__ == "__main__":
  app.run(port=5000, debug=True)