import requests as re 
import pandas as pd 
import time
import json
from pathlib import Path
import time 

import paho.mqtt.client as mqtt

# Roba per collegarsi al server MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(topic)

    else:
        print(f"Connect failed with code {rc}")

def on_publish(client, userdata, mid, properties=None):
    print(f"Message {mid} has been published.")

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")

# Creo il client MQTT
client = mqtt.Client(client_id="aaaaaaaa", clean_session=False)

# Passo i metodi creati precendentemente al client
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message


# Mi collego al broker
broker_address = "mqtt-dashboard.com" 
port = 1883 
client.connect(broker_address, port)

# Nome del topic
topic = "testtopic/1"


def math(value):
    # Metodo che fa tutta la matematica
    A = 7.0405E-12  # mm/digit^3
    B = -1.0504E-07  # mm/digit^2
    C = 2.7117E-02  # mm/digit
    D = -7.3308E+01  # mm
    rcp = A * value**3 + B*value**2 + C * value + D
    return rcp


def openLog():
    # Metodo che crea un file di log se non esiste, lo apre e ne fa il return
    file_path = Path('./IoT/log.txt')
    if not file_path.exists():
        f = open('./IoT/log.txt', 'w')

    f = open('./IoT/log.txt', 'a')
    return f

def writeToLog(log, content, response):
    # Metodo che scrive sul file log il contenuto della request e la response
    content['response'] = response
    content['system_ts'] = time.time()
    log.write(f'\n {content}')


def api_reqs(jsons, log = None):
        # Metodo che, data una lista di dizionari, effettua un post per ogni dizionario
        for json_ in jsons:
            headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
            response = re.post('https://zion.nextind.eu:443/api/v1/test_device_2024/telemetry', json.dumps(json_), headers=headers)
            # Converto il dizionario in json e lo posto
            print(json_)
            
            # Con questo pubblico sul server MQTT
            client.publish(topic, json.dumps(json_)+' Sent by Davidino')

            print(response.status_code)
            if log != None:
                writeToLog(log, content=json_, response=response.status_code)
                print('Appended to log!')
            print('\n')

            time.sleep(0.5)



def main_csv():
    log = openLog()
    # Apro il file di log (o lo creo se non esiste)
    df = pd.read_csv('./IoT/Estensimetro Esempio Letture.csv', sep=';')
    big_dictlist = df.to_dict(orient='records')
    # Trasformo ogni riga in un dizionario
    jsons_dict_list = []

    # print(big_dictlist)

    for dict in big_dictlist:
        dict['rcp'] = math(float(dict['Value'].replace(',','.')))
        # Calcolo l'RCP

        json_dict = { 'ts' : dict['Timestamp'],
                     'value' : dict['rcp']
        }
        # Il dizionario finale che verrà trasformato in un json nell'API request

        jsons_dict_list.append(json_dict)

    api_reqs(jsons_dict_list, log)
    # Faccio le requests

    log.close()
    # Chiudo il file di log

main_csv()
# Per far rimanere il client in ascolto per nuovi messaggi
client.loop_forever()
