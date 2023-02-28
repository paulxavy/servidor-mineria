
# % pylab inline
import os
import pandas as pd
import librosa
import glob 
import random
import numpy as np
from datetime import datetime
import os
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import StandardScaler


#listar los archivos
filelist = os.listdir('C:\\Users\\Martínez\\Desktop\\espanol\\pruebas') 
#leerlos en pandas
df_pruebas = pd.DataFrame(filelist)
# Renombrar el nombre de la columna a file
df_pruebas = df_pruebas.rename(columns={0:'file'})
df_pruebas.head()
#print(df_pruebas)
df = pd.concat([df_pruebas], ignore_index=True)

def extract_features(files):
    
    # Establecer el nombre para que sea la ruta de donde está el archivo en mi ordenador
    fn = os.path.abspath('C:\\Users\\Martínez\\Desktop\\espanol\\pruebas'+'/'+str(files.file))
    file_name = os.path.join(os.path.abspath('drive/Mydrive/voice')+'/'+str(files.file))
    # Carga el archivo de audio como una serie temporal de coma flotante y asigna la frecuencia de muestreo por defecto.
    # La frecuencia de muestreo se establece en 22050 por defecto
    X, sample_rate = librosa.load(fn, res_type='kaiser_fast') 

    # Generar coeficientes cepstrales de frecuencia Mel (MFCC) a partir de una serie temporal 
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_fft=2048, n_mfcc=40).T,axis=0)

    # Genera una transformada de Fourier en tiempo corto (STFT) para utilizarla en el chroma_stft
    
    stft = np.abs(librosa.stft(X))

    # Calcula un cromagrama a partir de una forma de onda o espectrograma de potencia.
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)

    # Calcula un espectrograma a escala mel.
    mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)

    # Calcula el contraste espectral
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)

    # Calcula las características del centroide tonal (tonnetz)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X),
    sr=sample_rate).T,axis=0)
        
    


    return mfccs, chroma, mel, contrast, tonnetz

# Código para iniciar el temporizador para ver cuánto tiempo se tarda en extraer las características
startTime = datetime.now()

# Aplicar la función a los datos del entrenamiento accediendo a cada fila del dataframe.
features_label = df.apply(extract_features, axis=1)

# Código para ver cuánto tardó
print(datetime.now() - startTime)

# Creamos una lista vacía donde concatenaremos todas las características en una característica larga
# para cada archivo para alimentar nuestra red neuronal

features = []
for i in range(0, len(features_label)):
    features.append(np.concatenate((features_label[i][0], features_label[i][1], 
                features_label[i][2], features_label[i][3],
                features_label[i][4]), axis=0))
    

len(features)

speakers = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10']

labels = speakers

X = np.array(features)
X.shape
y = np.array(labels)
# Codificación en caliente de y
lb = LabelEncoder()
y = to_categorical(lb.fit_transform(y))

modelo = load_model('C:\\Users\\Martínez\\Desktop\\m-servidor\\model17.h5')

ss = StandardScaler()
X = ss.fit_transform(X)

# Obtenemos nuestras predicciones de los datos de prueba
preds = modelo.predict(X)
classes1=np.argmax(preds,axis=1)

# Transformamos de nuevo nuestras predicciones a los identificadores de los oradores
preds = lb.inverse_transform(classes1)

# Creamos una nueva columna llamada preds y la hacemos igual a nuestras predicciones
df['preds'] = preds

print(df)