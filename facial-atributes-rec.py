from deepface import DeepFace
import pandas as pd
# python 3.6
import random
import time
from paho.mqtt import client as mqtt_client
import json
#Variables y constantes
#Datos del broker
broker = '127.0.0.1'
port = 1883
topic = "codigoIoT/ejemplo/DeppFace"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

#Definicion de funciones
#Conexion al Broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#Publicador
def publish2(client, mensaje):
    #msg_count = 0
    #while True:
    time.sleep(1)
    msg = mensaje
    result = client.publish(topic, msg)
    time.sleep(1)
    print(result)
    # result: [0, 1]
    status = result[0]
    if status == 0:
         print(f"Send `{msg}` to topic `{topic}`")
    else:
         print(f"Failed to send message to topic {topic}")
    #msg_count += 0

# Buscar Rostro
print ("Identificando rostro")

# df = DeepFace.find(img_path = "img1.jpg", db_path = "C:/workspace/my_db")
# df = DeepFace.find (img_path = "/home/gustavo/Documents/GitHub/Apertura-puertas-reconocimiento-facial/test/Rami.jpeg", db_path = "/home/gustavo/Documents/GitHub/Apertura-puertas-reconocimiento-facial/DeepFace/my_db", enforce_detection = "false")
obj = DeepFace.analyze(img_path = "/home/gustavo/Desktop/foto/fotoesp32CAM.jpg", 
        actions = ['age', 'gender', 'race', 'emotion']
)
print ("El resultado del analisis es:")
print (obj)
#json_view=obj.to_json(orient="index")
json_view=json.dumps(obj, indent=4)
#print ("Seleccion")
#print(json_view)
#print (df.identity[0])
client = connect_mqtt()
client.loop_start()
print ("Enviando mensaje")
#publish2(client, df.identity[0])
publish2(client, json_view)
print ("mensaje Enviado!")

#from deepface import DeepFace
