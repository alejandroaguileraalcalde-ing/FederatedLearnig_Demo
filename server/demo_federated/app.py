import zipfile
from _weakref import ref
import logging
import os

import flask

from google.cloud import storage



from flask import request
from flask import send_from_directory
import pandas as pd
from datetime import datetime as dt
import tensorflow as tf
import numpy as np
import io as io
from zipfile import ZipFile



from tensorflow.python.training import saver

'''import boto3'''
import pickle as pickle


app = flask.Flask(__name__)

#variables
numero = 8000
modelctr = 8000
modelctrstr = str(modelctr)
NOMBRE_CHECKPOINTS = "checkpoints_name_"+ str(modelctr)
NOMBRE_ZIP = "Zip_Name_" + str(modelctr)
nombre_fichero_descarga = ""


@app.route('/', methods=['GET'])

def home():
    return "Hello, this is the home page"


@app.route('/prueba', methods=['GET'])

def prueba():
    modelo()
    print("modelo")
    return "Hello, this is the prueba tab"

@app.route('/modelo', methods=['GET'])

def modelo():
    modelctr =contador + 1
    modeloSencillo()
    print("modelo sencillo")
    return "Hello, this is modelo sencillo"


@app.route('/crear_weight', methods=['GET'])

def crear_weight():

    averageWeights()
    print("se han usado los pesos y se ha crado un modleoa actualizado")
    return "se han usado los pesos y se ha crado un modleoa actualizado"



@app.route("/upload2", methods = ['GET'])
def u():
    configurabucket()
    return "es una prueba u"
@app.route("/upload_download", methods = ['GET'])     #funciona, descargar un fichero de la bucket de google y lo manda a la app.
def u3():
    if flask.request.method == "GET":
     storage_client = storage.Client.from_service_account_json("tftalejandroaguilera-8712e9c215d2.json")
     BUCKET_NAME = 'bucket-alejandro-aguilera'  # Nombre del bucket que he creado en el google-cloud
     bucket = storage_client.get_bucket(BUCKET_NAME)

     blob = bucket.blob('checkpoint_name.ckpt.meta')

     blob.download_to_filename("ejemplo")

     app.config["FICHERO_CHECK"] = ""

     return send_from_directory(app.config["FICHERO_CHECK"], filename="ejemplo", as_attachment=True)  #PROBAR

 #   configurabucket2()

@app.route("/contador", methods = ['GET'])  #perfecto
def u4():
     global numero
     numero = numero + 1
     global modelctr
     modelctr = modelctr +1
     global NOMBRE_CHECKPOINTS
     NOMBRE_CHECKPOINTS = "checkpoints_name_"+ str(modelctr)
     global NOMBRE_ZIP
     NOMBRE_ZIP = "Zip_Name_" + str(modelctr)
     ChangeIsModelUpdated()

     return "numero= " + str(numero) + " , nombre= " + NOMBRE_CHECKPOINTS + "isModelUpdated= " +str(isModelUpdated) + "Zip_name= " + str(NOMBRE_ZIP)


@app.route("/contador2", methods = ['GET'])  #perfecto
def uCCONT2():
     Contador()
     ChangeIsModelUpdated()

     return "numero= " + str(numero) + " , nombre= " + NOMBRE_CHECKPOINTS + "isModelUpdated= " +str(isModelUpdated) + "Zip_name= " + str(NOMBRE_ZIP)


def Contador():
    global numero
    numero = numero + 1
    global modelctr
    modelctr = modelctr + 1
    global NOMBRE_CHECKPOINTS
    NOMBRE_CHECKPOINTS = "checkpoints_name_" + str(modelctr)
    global NOMBRE_ZIP
    NOMBRE_ZIP = "Zip_Name_" + str(modelctr)
    return

def ChangeIsModelUpdated():
    global isModelUpdated
    if (isModelUpdated):
     isModelUpdated = False
     return
    else:
     isModelUpdated = True
     return

def configurabucket():
#poner el path al fichero key json
 storage_client = storage.Client.from_service_account_json("FICHERO_JSON")
 #BUCKET_NAME = 'bucket-alejandro-aguilera' # Nombre del bucket que he creado en el google-cloud
 #bucket = storage_client.get_bucket(BUCKET_NAME)
 bucket_nombre = 'prueba'
 bucket = storage_client.create_bucket(bucket_nombre)
 print("bucket lista pra usarse")

def configurabucket2():
#poner el path al fichero key json
 storage_client = storage.Client.from_service_account_json("FICHERO_JSON")
 BUCKET_NAME = 'bucket-alejandro-aguilera' # Nombre del bucket que he creado en el google-cloud
 bucket = storage_client.get_bucket(BUCKET_NAME)

 print("bucket lista pra usarse")

def subirficheroALmacenado():
#para subir
 blob = bucket.blob("nombrefichero.txt")
 blob.upload_from_filename("nombrefichero.txt")
 print("file uploaded")
 return
def descargarfichero():
#para descargar
 blob = bucket.blob("nombrefichero.txt")
 blob.download_from_filename("nombrefichero.txt")
 print("file downloaded")

def createbucket():
#si quiero crear una bucket
 bucket_Creada = storage_client.create_bucket("nombre bucket")

modelUpdated = True


@app.route("/isModelUpdated", methods = ['GET'])
def isModelUpdated():
 if flask.request.method == "GET":
  print("mirando si esta updated")
  
  if modelUpdated:
      return "YES"
  else:
      return "NO"







@app.route("/getGlobalModel", methods = ['GET'])   #funciona subiendo todos los ficheros y zip al bucket. Hay que ver el tema de los nombres
def getGlobalModel():
 if flask.request.method == "GET":
  print("mirando si esta updated")
  #habra que mirar una variable o algo
  if modelUpdated: # mando el fichero checkpoints
    Contador()
    modeloSencillo()
    Contador()
    #fileaux = modeloSencillo()
    #return fileaux

    print("se ha mandado el modelo")
    return "OK"

  else: # actualizo el modelo
    return

@app.route("/getModelPrueba", methods = ['GET'])
def getModelPrueba():
 if flask.request.method == "GET":
  print("mirando si esta updated")
  #habra que mirar una variable o algo
  if modelUpdated: # mando el fichero checkpoints
    #modeloSencillo()
    #fileaux = modeloSencillo()
    #return fileaux


    print("se ha mandado el modelo")
    return


  else: # actualizo el modelo
    return


@app.route("/descargar1", methods = ['GET']) #FUNCIONA: DESCARGAS EL FICHERO
def descargar1():
 if flask.request.method == "GET":
  print("mirando si esta updated")
  #habra que mirar una variable o algo
  if modelUpdated: # mando el fichero checkpoints

      global numero
      numero = numero + 1
      global modelctr
      modelctr = modelctr + 1
      global NOMBRE_CHECKPOINTS
      NOMBRE_CHECKPOINTS = "checkpoints_name_" + str(modelctr)
      global NOMBRE_ZIP
      NOMBRE_ZIP = "Zip_Name_" + str(modelctr)
      ################################
      peso_w = 0
      peso_b = 0

      storage_client = storage.Client.from_service_account_json("tftalejandroaguilera-8712e9c215d2.json")
      BUCKET_NAME = 'bucket-alejandro-aguilera'  # Nombre del bucket que he creado en el google-cloud
      bucket = storage_client.get_bucket(BUCKET_NAME)

      blob = bucket.blob('fichero_pesos')

      blob.download_to_filename("ejemplo_pesos")
      print("descargado fichero: fichero_pesos")

      f = open('ejemplo_pesos')
      string_list = f.readlines()
      f.close()

      sub_string_w_aux = string_list[2] #la tercera linea del fichero
      sub_string_b_aux = string_list[3]

      sub_string_w = sub_string_w_aux[0] + sub_string_w_aux[1] + sub_string_w_aux[2] + sub_string_w_aux[3] + sub_string_w_aux[4] + sub_string_w_aux[5]
      sub_string_b = sub_string_b_aux[0] + sub_string_b_aux[1] + sub_string_b_aux[2] + sub_string_b_aux[3] + sub_string_b_aux[4] + sub_string_b_aux[5]

      peso_w = float(sub_string_w)
      peso_b = float(sub_string_b)

      ## EXTRA POR SI FUNCIONA
      peso_w = np.float32(peso_w)
      peso_b = np.float32(peso_b)

      ################################

      x = tf.placeholder(tf.float32, name='input')
      y_ = tf.placeholder(tf.float32, name='target')

    
      W = tf.Variable(peso_w, name='W')
      b = tf.Variable(peso_b, name='b')

     # y = x * W + b
      y = tf.add(tf.multiply(x, W), b)
      y = tf.identity(y, name='output')

      loss = tf.reduce_mean(tf.square(y - y_))
      optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
      train_op = optimizer.minimize(loss, name='train')

      init = tf.global_variables_initializer()

      # Creating a tf.train.Saver adds operations to the graph to save and
      # restore variables from checkpoints.

      saver_def = tf.train.Saver().as_saver_def
 
     
      saver = tf.train.Saver()
      # Training
      # saver.save(sess, your_path + "/checkpoint_name.ckpt")
      # TensorFlow session
     #### sess = tf.Session()
      sess = tf.keras.backend.get_session()
      sess.run(init)


      ### saver.save(sess, "+"+ NOMBRE_CHECKPOINTS + "-.ckpt")
      save_path = saver.save(sess, "+"+ NOMBRE_CHECKPOINTS + "-.ckpt")

      app.config["FICHERO_CHECK"] = ""
   
      zipObj = ZipFile('test.zip', 'w')
      zipObj.write("+"+NOMBRE_CHECKPOINTS + "-.ckpt.meta")
      zipObj.close()
      return send_from_directory(app.config["FICHERO_CHECK"], filename='test.zip', as_attachment=True)
  

  else: # actualizo el modelo
    return

@app.route("/descargar_graf_pesos_test", methods = ['GET']) 
def descargar_graph_pesos_test():
 if flask.request.method == "GET":
  print("mirando si esta updated")
  #habra que mirar una variable o algo
  if modelUpdated: # mando el fichero checkpoints

      global numero
      numero = numero + 1
      global modelctr
      modelctr = modelctr + 1
      global NOMBRE_CHECKPOINTS
      NOMBRE_CHECKPOINTS = "checkpoints_name_" + str(modelctr)
      global NOMBRE_ZIP
      NOMBRE_ZIP = "Zip_Name_" + str(modelctr)
      ################################
      peso_w = 0
      peso_b = 0

      storage_client = storage.Client.from_service_account_json("tftalejandroaguilera-8712e9c215d2.json")
      BUCKET_NAME = 'bucket-alejandro-aguilera'  # Nombre del bucket que he creado en el google-cloud
      bucket = storage_client.get_bucket(BUCKET_NAME)

      blob = bucket.blob('fichero_pesos')

      blob.download_to_filename("ejemplo_pesos")
      print("descargado fichero: fichero_pesos")

      f = open('ejemplo_pesos')
      string_list = f.readlines()
      f.close()

      sub_string_w_aux = string_list[2] #la tercera linea del fichero
      sub_string_b_aux = string_list[3]

      sub_string_w = sub_string_w_aux[0] + sub_string_w_aux[1] + sub_string_w_aux[2] + sub_string_w_aux[3] + sub_string_w_aux[4] + sub_string_w_aux[5]
      sub_string_b = sub_string_b_aux[0] + sub_string_b_aux[1] + sub_string_b_aux[2] + sub_string_b_aux[3] + sub_string_b_aux[4] + sub_string_b_aux[5]

      peso_w = float(sub_string_w)
      peso_b = float(sub_string_b)

      ## EXTRA POR SI FUNCIONA
      peso_w = np.float32(peso_w)
      peso_b = np.float32(peso_b)

      ################################

      x = tf.placeholder(tf.float32, name='input')
      y_ = tf.placeholder(tf.float32, name='target')

     # W = tf.Variable(5., name='W')
     # b = tf.Variable(3., name='b')
      W = tf.Variable(peso_w, name='W')
      b = tf.Variable(peso_b, name='b')

     # y = x * W + b
      y = tf.add(tf.multiply(x, W), b)
      y = tf.identity(y, name='output')

      loss = tf.reduce_mean(tf.square(y - y_))
      optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
      train_op = optimizer.minimize(loss, name='train')

      init = tf.global_variables_initializer()

     
      saver_def = tf.train.Saver().as_saver_def
     
      sess = tf.keras.backend.get_session()
      sess.run(init)


      ### saver.save(sess, "+"+ NOMBRE_CHECKPOINTS + "-.ckpt")
      save_path = saver.save(sess, "+"+ NOMBRE_CHECKPOINTS + "-.ckpt")
      with open('graph_pesos.pb', 'wb') as f:
           f.write(tf.get_default_graph().as_graph_def().SerializeToString())

      app.config["FICHERO_CHECK"] = ""
   
      zipObj = ZipFile('test.zip', 'w')
      zipObj.write("graph_pesos.pb")
      zipObj.close()
      return send_from_directory(app.config["FICHERO_CHECK"], filename='test.zip', as_attachment=True)

  else: # actualizo el modelo
    return



@app.route("/descargar9", methods = ['GET'])
def descargar9():
 if flask.request.method == "GET":
  print("mirando si esta updated")
  #habra que mirar una variable o algo
  if modelUpdated: # mando el fichero checkpoints

      peso_w = 0
      peso_b = 0

      storage_client = storage.Client.from_service_account_json("tftalejandroaguilera-8712e9c215d2.json")
      BUCKET_NAME = 'bucket-alejandro-aguilera'  # Nombre del bucket que he creado en el google-cloud
      bucket = storage_client.get_bucket(BUCKET_NAME)

   #   blob = bucket.blob('fichero_pesos')
      global nombre_fichero_descarga

      print("fichero descargado deberia ser " + nombre_fichero_descarga)

     # blob = bucket.blob(NOMBRE_CHECKPOINTS+'_fichero_pesos_')
      blob = bucket.blob(nombre_fichero_descarga)
      print("Descargando fichero:  "+nombre_fichero_descarga)
      blob.download_to_filename("ejemplo_pesos")
      print("descargado fichero: fichero_pesos")

      f = open('ejemplo_pesos')
      string_list = f.readlines()
      f.close()

      sub_string_w_aux = string_list[2] #la tercera linea del fichero
      sub_string_b_aux = string_list[3]

      sub_string_w = sub_string_w_aux[0] + sub_string_w_aux[1] + sub_string_w_aux[2] + sub_string_w_aux[3] + sub_string_w_aux[4] + sub_string_w_aux[5]
      sub_string_b = sub_string_b_aux[0] + sub_string_b_aux[1] + sub_string_b_aux[2] + sub_string_b_aux[3] + sub_string_b_aux[4] + sub_string_b_aux[5]

      peso_w = float(sub_string_w)
      peso_b = float(sub_string_b)

      ################################

      x = tf.placeholder(tf.float32, name='input')
      y_ = tf.placeholder(tf.float32, name='target')

      W = tf.Variable(peso_w, name='W')
      b = tf.Variable(peso_b, name='b')

     # y = x * W + b
      y = tf.add(tf.multiply(x, W), b)
      y = tf.identity(y, name='output')

      loss = tf.reduce_mean(tf.square(y - y_))
      optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
      train_op = optimizer.minimize(loss, name='train')

      init = tf.global_variables_initializer()

      # Creating a tf.train.Saver adds operations to the graph to save and
      # restore variables from checkpoints.

      saver_def = tf.train.Saver().as_saver_def
     
      sess = tf.Session()
      sess.run(init)
   
      saver.save(sess, "checkpoint_actualizado_"+modelctrstr+".ckpt")
      print("se han creado fichero con nombre ... "+ modelctrstr)

      #
      app.config["FICHERO_CHECK"] = ""
  
      zipObj = ZipFile('test.zip', 'w')
      zipObj.write("checkpoint")
  
      zipObj.write("checkpoint_actualizado_"+modelctrstr+".ckpt" + '.index')
      zipObj.write("checkpoint_actualizado_"+modelctrstr+".ckpt" + '.data-00000-of-00001')
      zipObj.write("checkpoint_actualizado_"+modelctrstr+".ckpt.meta") # no se si igual .meta
      zipObj.close()
      return send_from_directory(app.config["FICHERO_CHECK"], filename='test.zip', as_attachment=True)
 

  else: # actualizo el modelo
    return


@app.route("/descargar_graph", methods = ['GET']) #FUNCIONA: DESCARGAS EL FICHERO
def descargar_graph():
 if flask.request.method == "GET":
  print("mirando si esta updated")
  #habra que mirar una variable o algo
  if modelUpdated: # mando el fichero checkpoints

      global numero
      numero = numero + 1
      global modelctr
      modelctr = modelctr + 1
      global NOMBRE_CHECKPOINTS
      NOMBRE_CHECKPOINTS = "checkpoints_name_" + str(modelctr)
      global NOMBRE_ZIP
      NOMBRE_ZIP = "Zip_Name_" + str(modelctr)

      x = tf.placeholder(tf.float32, name='input')
      y_ = tf.placeholder(tf.float32, name='target')

      W = tf.Variable(5., name='W')
      b = tf.Variable(3., name='b')

      y = tf.add(tf.multiply(x, W), b)
      y = tf.identity(y, name='output')

      loss = tf.reduce_mean(tf.square(y - y_))
      optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
      train_op = optimizer.minimize(loss, name='train')

      init = tf.global_variables_initializer()

      # Creating a tf.train.Saver adds operations to the graph to save and
      # restore variables from checkpoints.

      saver_def = tf.train.Saver().as_saver_def()
      ###NO VA EL SAVER DE GRAH DEF##########################
      with open('graph.pb', 'wb') as f:
           f.write(tf.get_default_graph().as_graph_def().SerializeToString())



      app.config["FICHERO_CHECK"] = ""


      return send_from_directory(app.config["FICHERO_CHECK"], filename='graph.pb', as_attachment=True)
  else: # actualizo el modelo
    return


@app.route("/descargar_graph_dense", methods = ['GET']) #FUNCIONA: DESCARGAS EL FICHERO
def descargar_graph_dense():
 if flask.request.method == "GET":
  print("mirando si esta updated")
  #habra que mirar una variable o algo
  if modelUpdated: # mando el fichero checkpoints

      global numero
      numero = numero + 1
      global modelctr
      modelctr = modelctr + 1
      global NOMBRE_CHECKPOINTS
      NOMBRE_CHECKPOINTS = "checkpoints_name_" + str(modelctr)
      global NOMBRE_ZIP
      NOMBRE_ZIP = "Zip_Name_" + str(modelctr)

      model = tf.keras.models.Sequential([tf.keras.layers.Dense(1, input_shape=(1,)),
      tf.keras.layers.Dense(25, activation=tf.keras.activations.relu),
      tf.keras.layers.Dense(1, activation=tf.keras.activations.relu)])

      model.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.mean_squared_error)
      optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)

      init = tf.global_variables_initializer()

      saver_def = tf.train.Saver().as_saver_def()
    
      with open('graph.pb', 'wb') as f:
           f.write(tf.get_default_graph().as_graph_def().SerializeToString())



      app.config["FICHERO_CHECK"] = ""


      return send_from_directory(app.config["FICHERO_CHECK"], filename='graph.pb', as_attachment=True)
  else: # actualizo el modelo
    return


@app.route("/descargar_checkpoint", methods = ['GET']) #FUNCIONA: DESCARGAS EL FICHERO ****si
def descargar_checkpoint():
 if flask.request.method == "GET":
  print("mirando si esta updated")

  if modelUpdated: # mando el fichero checkpoints
    app.config["FICHERO_TEXTO1"] = ""

    x = tf.placeholder(tf.float32, name='input')
    y_ = tf.placeholder(tf.float32, name='target')

    W = tf.Variable(5., name='W')
    b = tf.Variable(3., name='b')

    y = x * W + b
    y = tf.identity(y, name='output')

    loss = tf.reduce_mean(tf.square(y - y_))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
    train_op = optimizer.minimize(loss, name='train')

    init = tf.global_variables_initializer()

    # Creating a tf.train.Saver adds operations to the graph to save and
    # restore variables from checkpoints.

    saver_def = tf.train.Saver().as_saver_def
    

    saver = tf.train.Saver()
    # Training
    # saver.save(sess, your_path + "/checkpoint_name.ckpt")
    # TensorFlow session
    sess = tf.Session()
    sess.run(init)
    saver.save(sess, "checkpoint_name.ckpt")


    #igual hay que ponerlo como zip y mandarlo

    return send_from_directory(app.config["FICHERO_TEXTO1"], filename= "checkpoint_name.ckpt.meta", as_attachment=True)


  else: # actualizo el modelo
    return


@app.route("/upload", methods = ['POST'])   
def upload():
 global numero
 numero = numero + 1
 global modelctr
 modelctr = modelctr + 1
 global NOMBRE_CHECKPOINTS
 NOMBRE_CHECKPOINTS = "checkpoints_name_" + str(modelctr)
 global NOMBRE_ZIP
 NOMBRE_ZIP = "Zip_Name_" + str(modelctr)

 if flask.request.method == "POST":
  modelUpdated = False # ahora el modelo no está actualizado. hay que sacar los pesos y evaluarlos para volver a entrenar el modelo y sacar el fichero checkpoints
  print("Uploading File")
  if flask.request.files["file"]:                       #se coge la infomracion de file y se pone en weights
    weights = flask.request.files["file"].read()
    weights_stream = io.BytesIO(weights)
    #bucket = storage.bucket()

    storage_client = storage.Client.from_service_account_json("tftalejandroaguilera-8712e9c215d2.json")
    BUCKET_NAME = 'bucket-alejandro-aguilera'  # Nombre del bucket que he creado en el google-cloud
    bucket = storage_client.get_bucket(BUCKET_NAME)


    #Uploading Files to Firebase
    print("Saving at Server")
    with open("delta.bin", "wb") as f:             #se crea un fichero delta.bin con los weigths descargados que llegan desde la app
      f.write(weights_stream.read())
    print("Starting upload to Firebase")                        ####*************esto es para usbirlo a la firebase queno es mio. O uso una o lo creo en una dirección local
    with open("delta.bin", "rb") as upload:
      byte_w = upload.read()
      #Preprocessing data before upload. File to be sent to Firebase is named "Weights.bin"
    with open("Weights.bin", "wb") as f: #nombre del fichero que se envia desde la app
      pickle.dump(weights, f)
    with open("Weights.bin", "rb") as f:    #manda a google-cloud el fichero Weights.bin
      blob = bucket.blob('weight__'+ str(modelctr))
      blob.upload_from_file(f)
      print("File Successfully Uploaded to Firebase")
      return "File Uploaded\n"
  else:
    print("File not found")


@app.route("/upload_test", methods = ['POST'])   #PONER BIEN LOS NOMBRES
def upload_test():
 global numero
 numero = numero + 1
 global modelctr
 modelctr = modelctr + 1
 global NOMBRE_CHECKPOINTS
 NOMBRE_CHECKPOINTS = "checkpoints_name_" + str(modelctr)
 global NOMBRE_ZIP
 NOMBRE_ZIP = "Zip_Name_" + str(modelctr)
 global modelctrstr
 modelctrstr = str(modelctr)

 if flask.request.method == "POST":
    modelUpdated = False # ahora el modelo no está actualizado. hay que sacar los pesos y evaluarlos para volver a entrenar el modelo y sacar el fichero checkpoints
    print("Uploading File")
                      #se coge la infomracion de file y se pone en weights
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)


        storage_client = storage.Client.from_service_account_json("tftalejandroaguilera-8712e9c215d2.json")
        BUCKET_NAME = 'bucket-alejandro-aguilera'  # Nombre del bucket que he creado en el google-cloud
        bucket = storage_client.get_bucket(BUCKET_NAME)


    #Uploading Files to Firebase
        print("Saving at Server")

        with open(uploaded_file.filename, "rb") as f:    #manda a google-cloud el fichero Weights.bin
       #  blob = bucket.blob(uploaded_file.filename + str(modelctr))
         blob = bucket.blob(NOMBRE_CHECKPOINTS+'_fichero_pesos_')
         blob.upload_from_file(f)
         print("File Successfully Uploaded to Firebase")
         print("subido el fichero "+NOMBRE_CHECKPOINTS+'_fichero_pesos_')
         global nombre_fichero_descarga
         nombre_fichero_descarga = NOMBRE_CHECKPOINTS+'_fichero_pesos_'
         print("fichero con nombre " + nombre_fichero_descarga)


        return "File Uploaded\n"
    else:
        print("File not found")


def modeloSencillo():
    global numero
    numero = numero + 1
    global modelctr
    modelctr = modelctr + 1
    global NOMBRE_CHECKPOINTS
    NOMBRE_CHECKPOINTS = "checkpoints_name_" + str(modelctr)
    global NOMBRE_ZIP
    NOMBRE_ZIP = "Zip_Name_" + str(modelctr)

    x = tf.placeholder(tf.float32, name='input')
    y_ = tf.placeholder(tf.float32, name='target')

    W = tf.Variable(5., name='W')
    b = tf.Variable(3., name='b')

    y = x * W + b
    y = tf.identity(y, name='output')

    loss = tf.reduce_mean(tf.square(y - y_))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
    train_op = optimizer.minimize(loss, name='train')

    init = tf.global_variables_initializer()

    # Creating a tf.train.Saver adds operations to the graph to save and
    # restore variables from checkpoints.

    saver_def = tf.train.Saver().as_saver_def


    saver = tf.train.Saver()
  
    sess = tf.Session()
    sess.run(init)
    saver.save(sess,  NOMBRE_CHECKPOINTS+".ckpt")

    storage_client = storage.Client.from_service_account_json("tftalejandroaguilera-8712e9c215d2.json")
    BUCKET_NAME = 'bucket-alejandro-aguilera'  # Nombre del bucket que he creado en el google-cloud
    bucket = storage_client.get_bucket(BUCKET_NAME)

 
    with open(NOMBRE_CHECKPOINTS+".ckpt.data-00000-of-00001", "rb") as f:            #mando a google-cloud el fichero FINAL_GRAPH.ckpt.data
        blob = bucket.blob(NOMBRE_CHECKPOINTS+'.ckpt.data-00000-of-00001')
        blob.upload_from_file(f)
    with open(NOMBRE_CHECKPOINTS+".ckpt.index", "rb") as f:                  #mando a google-cloud el fichero final_graph.ckpt.index
        blob = bucket.blob(NOMBRE_CHECKPOINTS+'.ckpt.index')
        blob.upload_from_file(f)
    with open(NOMBRE_CHECKPOINTS+".ckpt.meta", "rb") as f:              #mando a google-cloud el fichero final_graph.ckpt.meta
        blob = bucket.blob(NOMBRE_CHECKPOINTS+".ckpt.meta")
        blob.upload_from_file(f)

    print("Files Uploaded")
    print("Global Model Updated")
    zipf = zipfile.ZipFile('model' + str(modelctr) + '.zip', 'w', zipfile.ZIP_DEFLATED)
  
    zipObj = ZipFile(NOMBRE_ZIP + "_"+ str(modelctr) + '.zip', 'w')
    zipObj.write('checkpoint')
    zipObj.write(NOMBRE_CHECKPOINTS+".ckpt.meta")
    zipObj.close()
    print("zip created")


    with open(NOMBRE_ZIP + "_"+ str(modelctr) + '.zip', 'rb') as f:
       blob = bucket.blob(NOMBRE_ZIP+ "_"+ str(modelctr) + '.zip')
       blob.upload_from_file(f)

    global isModelUpdated
    isModelUpdated = True
    return


def mandar_fichero():
    app.config["FICHERO_TEXTO"] = ".idea/almacen" #igual poner ruta completa
    return send_from_directory(app.config["FICHERO_TEXTO"], filename = ficheromandar.txt, as_attachment= True )

# return checkpoint_name.ckpt.meta



def averageWeights():
    # Average the weights

    ##memWeights es par diferenciar los wights leiods en stream vs los de memoria

    w1 = []
    b1 = []

    w1.append(8.5)
    w1.append(10)
    w1.append(9.3)

    b1.append(2)
    b1.append(1.6)
    b1.append(1.8)

    n_w = 3
    sumatorio_b1 =0
    sumatorio_w1 =0

    #w1 /= n_w
    #b1 /= n_w

    for i in range (1,n_w):
      #  global sumatorio_b1
        sumatorio_b1 = b1[i]
      #  global sumatorio_w1
        sumatorio_w1 = w1[i]


    w1 = [sumatorio_w1/n_w]
    b1 = [sumatorio_b1 / n_w]

    print("W1: ")
    print(w1)
    print("B1: ")
    print(b1)


    model_weights = [w1, b1]

    model = tf.keras.models.Sequential(
        [tf.keras.layers.Dense(1, input_shape=(1,)),
         # tf.keras.layers.Dense(25, activation=tf.keras.activations.relu),
         tf.keras.layers.Dense(1, activation=tf.keras.activations.relu)])
    model.compile(optimizer=tf.keras.optimizers.SGD(lr=0.01), loss=tf.keras.losses.mean_squared_error)

    print(model_weights)
    model.set_weights(model_weights)
    saver = tf.train.Saver()
    sess = tf.keras.backend.get_session()
    save_path = saver.save(sess, "model_linear.ckpt")



