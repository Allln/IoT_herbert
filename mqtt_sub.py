import paho.mqtt.client as mqtt
import json
import urllib.request

SERVER = '147.228.124.68'  # RPi
# TOPIC = 'ite/fake/control'
TOPIC = 'ite/#'

counter = 0

blue = [25]
blue_av = 0.0
blue_t = 0
black = [25]
black_av = 0.0
black_t = 0
green = [25]
green_av = 0.0
green_t = 0
pink = [25]
pink_av = 0.0
pink_t = 0
red = [25]
red_av = 0.0
red_t = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, mid, qos):
    print('Connected with result code qos:', str(qos))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)

def apiSend(jsonir):   
    server = "https://6zl322zc2j.execute-api.eu-central-1.amazonaws.com/Prod/measurements"
    UUID = "353e2362-932a-442c-9518-bd0017b5f630"
    status = "OK"
    date = jsonir["ite_message"]["created_on"]
    temp = jsonir["ite_message"]["temperature"]
    body = {   
    "createdOn": date,
    "sensorUUID": UUID,
    "temperature": temp,
    "status": status
    }
    json_api = json.dumps(body)
    b_jsondata = json_api.encode('utf-8')

    req = urllib.request.Request(server)
    req.add_header('UUID', UUID)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(b_jsondata))
    
    response = urllib.request.urlopen(req, b_jsondata)
    raw_data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    data = json.loads(raw_data.decode(encoding))
    print(data)

    
def average_c(list_x):
    return(sum(list_x)/len(list_x)) 

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global counter
    
    global red
    global red_av
    global red_t
    global green
    global green_av
    global green_t
    global pink
    global pink_av
    global pink_t
    global blue
    global blue_av
    global blue_t
    global black
    global black_av
    global black_t
    
    if (msg.payload == 'Q'):
        client.disconnect()
    json_msg = json.loads(msg.payload)
    print(json_msg["ite_message"])
    
    if json_msg["ite_message"]["team_name"] == "blue":
        counter = counter + 1
        if(counter == 10):
            apiSend(json_msg)
            counter = 0
        if len(blue) > 720:
            blue.pop(0)
            blue.append(float(json_msg["ite_message"]["temperature"]))
            blue_av = average_c(blue)
            blue_t = json_msg["ite_message"]["created_on"]
        else:
            blue.append(float(json_msg["ite_message"]["temperature"]))
            blue_av = average_c(blue)
            blue_t = json_msg["ite_message"]["created_on"]              
    if json_msg["ite_message"]["team_name"] == "black":
        if len(black) > 720:
            black.pop(0)
            black.append(float(json_msg["ite_message"]["temperature"]))
            black_av = average_c(black)
            black_t = json_msg["ite_message"]["created_on"]
        else:
            black.append(float(json_msg["ite_message"]["temperature"]))
            black_av = average_c(black)
            black_t = json_msg["ite_message"]["created_on"]
    if json_msg["ite_message"]["team_name"] == "red":
        if len(red) > 720:
            red.pop(0)
            red.append(float(json_msg["ite_message"]["temperature"]))
            red_av = average_c(red)
            red_t = json_msg["ite_message"]["created_on"]
        else:
            red.append(float(json_msg["ite_message"]["temperature"]))
            red_av = average_c(red)
            red_t = json_msg["ite_message"]["created_on"]
    if json_msg["ite_message"]["team_name"] == "green":
        if len(green) > 720:
            green.pop(0)
            green.append(float(json_msg["ite_message"]["temperature"]))
            green_av = average_c(green)
            green_t = json_msg["ite_message"]["created_on"]
        else:
            green.append(float(json_msg["ite_message"]["temperature"]))
            green_av = average_c(green)
            green_t = json_msg["ite_message"]["created_on"]
    if json_msg["ite_message"]["team_name"] == "pink":
        if len(pink) > 720:
            pink.pop(0)
            pink.append(float(json_msg["ite_message"]["temperature"]))
            pink_av = average_c(pink)
            pink_t = json_msg["ite_message"]["created_on"]
        else:
            pink.append(float(json_msg["ite_message"]["temperature"]))
            pink_av = average_c(pink)
            pink_t = json_msg["ite_message"]["created_on"]
    
    temp_json = json.dumps({'blue':{'data': blue,
                                'avg': round(blue_av,2),
                                'max': max(blue), 
                                'min': min(blue),
                                'time': blue_t},
                            'green':{'data': green,
                                'avg': round(green_av,2),
                                'max': max(green),
                                'min': min(green),
                                'time': green_t},
                            'black':{'data': black,
                                'avg': round(black_av,2),
                                'max': max(black),
                                'min': min(black),
                                'time': black_t},
                            'red':{'data': red,
                                'avg': round(red_av,2),
                                'max': max(red),
                                'min': min(red),
                                'time': red_t},
                            'pink':{'data': pink,
                                 'avg': round(pink_av,2),
                                 'max': max(pink),
                                 'min': min(pink),
                                 'time': pink_t}})
    
    with open("jsonir.json", 'w') as fout:    
        fout.write(temp_json)    
    

def main():  
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set('kitt', password='itejefaktzabava')

    client.connect(SERVER, 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and
    # a manual interface.
    client.loop_forever()


if __name__ == '__main__':
    main()