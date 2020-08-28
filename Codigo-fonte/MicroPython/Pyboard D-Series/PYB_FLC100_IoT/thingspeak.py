from umqtt.simple import MQTTClient

class Thingspeak:
    def __init__(self):
        self.user = "3SOPC2X6DEHXW2JC"
        self.pswd = "K7H9CQYEFCAVZG4F"
        self.channel_id = "907446"
        self.keyWrite = "7ENQCDJCAUM34K9T"
        self.client = MQTTClient("","","")
    
    def openConnection(self):
        self.client = MQTTClient(client_id = "umqtt_client", server = "mqtt.thingspeak.com", user =  self.user , password= self.pswd , ssl = False)
        self.client.connect()
    
    def closeConnection(self):
        self.client.disconnect()
    
    def uploadData(self, *data):
        topic = "channels/"+self.channel_id+"/publish/"+self.keyWrite
        
        pyload = ""
        for i,x in enumerate(data):
            pyload += "&field%d=%s" % (i+1,x)
        pyload = pyload[1:]
        
        self.client.publish(topic, pyload)
