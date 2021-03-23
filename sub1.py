import paho.mqtt.client as mqtt
import json
import sys
from concurrent.futures import ThreadPoolExecutor
import time
from func import Get_device,Set_device,Get_map
# Get Cursor
a = 0
data = open("/Users/vuhainam/Desktop/server_devine.txt", "r").read()
json1 = json.loads(data)
device_id = json1['device']['id']
mqtt_sub_topic = ["/d/resp/s/{0}/REG".format(device_id),"/d/req/s/c/LIST","/d/req/s/{0}/SET".format(device_id),"/d/req/s/{0}/GET".format(device_id),"/d/req/s/{0}/NOTIFY".format(device_id)]

data_att = open("/Users/vuhainam/Desktop/attributes.txt", "r").read()


client=mqtt.Client()
executor = ThreadPoolExecutor(100)
def on_connect(client, userdata, flags, rc):
    client.connected_flag=True
    client.disconnect_flag=False
    for i in mqtt_sub_topic:
        client.subscribe(i)
    
    print("Connected")
    print("rc: " + str(rc))
    
        


def on_subscribe(client, userdata, mid, granted_qos):
    
    print("ok")

def on_disconnect(client, userdata, rc):
    print("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True

def on_message(client, userdata, message):
    print("message topic  ",str(message.topic))
    executor.submit(thread_process_message, ((message)))


def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def thread_process_message(message):
    global a
    try:
        my_json = message.payload.decode('utf8')
        data = json.loads(my_json)
        print("message received  ",data)
        ls = message.topic.split('/')
        if message.topic == "/d/resp/s/{0}/REG".format(device_id):
            if data['status'] == 1 :
                a = 1
        elif message.topic == "/d/req/s/c/LIST":
            global data_att
            topic_1 = "/d/resp/{0}/s/LIST".format(device_id)
            json_att = json.loads(data_att)
            payload_1 = json_att
            client.publish(str(topic_1),str(payload_1))
        elif message.topic == "/d/req/s/{0}/SET".format(device_id):
            ls_json = Get_map()
            #gui xuong
            for i in ls_json:
                for j in data['attributes']:
                    if i['name'] == j['name']:
                        resp = Set_device(point=i,value=j['value'])
                        print(resp)
                print(i)
            #gui len serv

        elif message.topic == "/d/req/s/{0}/GET".format(device_id):
            ls_json = Get_map()
            #gui xuong
            for i in ls_json:
                resp = Get_device(point=i)
                print(resp)
            #gui len serv

        elif message.topic == "/d/req/s/{0}/NOTIFY".format(device_id):#lap lich gui 
            pass
    except Exception as ex:
        print(ex)
def init_mqtt(client,mqtt_host,mqtt_port,mqtt_uid,mqtt_password):
    mqtt.Client.connected_flag=False
    #client.username_pw_set(username=mqtt_uid,password=mqtt_password)
    client.on_connect = on_connect  
    client.on_subscribe=on_subscribe
    client.on_message=on_message
    client.on_publish = on_publish
    client.connect(mqtt_host, int(mqtt_port))
    client.loop_start()

def handler1(): 
    global a
    global data_att
    topic_reg = "/d/req/{0}/s/REG".format(device_id)
    topic_noti = "/d/req/{0}/s/NOTIFY".format(device_id)
    json1 = json.loads(data_att)
    payload = json1
    while True:
        if(a == 0):
            ls_json_map = Get_map() 
            for i in ls_json_map:
                resp = Get_device(point=i)
                client.publish(str(topic_noti),str(resp))
            client.publish(str(topic_reg),str(payload))
            time.sleep(5)
        else:
            ls_json_map = Get_map() 
            for i in ls_json_map:
                resp = Get_device(point=i)
                client.publish(str(topic_noti),str(resp))
            time.sleep(5)


def handler():
    mqtt_host="broker.hivemq.com"
    mqtt_port="1883"
    mqtt_uid=""
    mqtt_password=""
    #Connection initiated
    init_mqtt(client,mqtt_host,mqtt_port,mqtt_uid,mqtt_password)



if __name__ == "__main__": 
    handler()
    handler1()