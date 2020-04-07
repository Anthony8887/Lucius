import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import requests
import json
import jsonpath
import datetime
import re

# url = 'http://localhost:5000/'
# key = "?apikey=0ED88487E13B445CAA56462107C6D0E6"
#
url = "http://10.0.0.63/api/"
key = "?apikey=BCDE97A05BB04135BD2B9097AE2F5B0A"



class PrinterHelper(object):
    def __init__(self):
        pass


    def speak(self, text):
        tts = gTTS(text=text, lang='en')
        filename = 'voice.mp3'
        tts.save(filename)
        playsound.playsound(filename)


    def get_audio(self):
        r =sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ''

            try:
                said = r.recognize_google(audio)
                print(said)
            except Exception as e:
                print("Exception" + str(e))
        return said


    def print_commands(self, text):
        if "printer state" in text:
            response = requests.get(url + 'printer' + key)
            # finds specific part of state operational or not
            json_response = json.loads(response.text)
            if response.status_code == 200:
                self.speak('the state is {}'.format(json_response['state']['text']))
            elif response.status_code == 500:
                self.speak('server error occured')
            elif response.status_code == 409:
                self.speak("couldn't get any data")

        elif text == "start print":
            data = {
            "command": "start"
            }
            response = requests.post(url + 'job' + key, json = data) # starts the 3d printer
            if response.status_code == 200:
                self.speak('Printer has started')
            if response.status_code == 409:
                self.speak("print couldn't be started")
            if response.status_code == 204:
                self.speak("haven't loaded a print yet")
            if response.status_code == 404:
                self.speak("couldn't connect to server")

        elif "cancel print" in text:
            data = {
            "command": "cancel"
            }
            response = requests.post(url + 'job' + key, json = data)
            if response.status_code == 200:
                self.speak('print has cancelled')
            if response.status_code == 409:
                self.speak("print couldn't be cancelled")
            if response.status_code == 404:
                self.speak("couldn't connect to server")

        elif text == "restart print":
            data = {
            "command": "restart"
            }
            response = requests.post(url + 'job' + key, json = data)
            if response.status_code == 200:
                self.speak('print has restarted')
            if response.status_code == 409:
                self.speak("print couldn't restart")
            if response.status_code == 404:
                self.speak("couldn't connect to server")

        elif "pause print" in text:
            data = {
            "command": "pause",
            "action": "pause"
            }
            response = requests.post(url + 'job' + key, json = data)
            if response.status_code == 200:
                self.speak('print has paused')
            if response.status_code == 409:
                self.speak("print couldn't be paused")
            if response.status_code == 404:
                self.speak("couldn't connect to server")

        elif text == "resume print":
            data = {
            "command": "pause",
            "action": "resume"
            }
            response = requests.post(url + 'job' + key, json = data)
            if response.status_code == 200:
                self.speak('print has resumed')
            if response.status_code == 409:
                self.speak("print couldn't be resumed")
            if response.status_code == 404:
                self.speak("couldn't connect to server")

        elif "temp of bed" in text:
            response = requests.get(url + 'printer' + key)
            # determines the temps of all printer parts
            json_response = json.loads(response.text)
            if response.status_code == 200:
                self.speak('temp:', json_response['temperature']['bed']['actual'])
            if response.status_code == 409:
                self.speak("bed temperature couldn't be found")

        elif "temp of nozzle" in text:
            response = requests.get(url + 'printer' + key)
            # determines the temps of all printer extruder
            json_response = json.loads(response.text)
            if response.status_code == 200:
                self.speak('temp:', json_response['temperature']['tool0']['actual'])
            if response.status_code == 409:
                self.speak("extruder temperature couldn't be found")

        elif "time remaining on print" in text:
            response = requests.get(url + 'job' + key)
            json_response = json.loads(response.text)
            self.speak('there is {} remaining on the print'.format(json_response['progress']['printTimeLeft']))

        elif "how long has the print been going" in text:
            response = requests.get(url + 'job' + key)
            json_response = json.loads(response.text)
            self.speak('the print has been going for {}'.format(json_response['progress']['printTime']))

        elif "set nozzle temp to" in text or "set temperature of nozzle to" in text:
            found = re.findall(r'\d+', text)
            default_temp = 50
            print(text)
            if len(found) > 0:
                temp = int(found[0])
            else:
                temp = default_temp
            data = {
                "command": "target",
                "targets": {
                "tool0": temp
                }
            }
            response = requests.post(url + 'printer/' + 'tool' + key, json = data)
            if response.status_code == 204:
                self.speak('temperature set to ' + str(temp) + 'degrees')
            if response.status_code == 409:
                self.speak("couldn't set temperature")
            if response.status_code == 400:
                self.speak("couldn't determine the temperature you wanted")
            if response.status_code == 404:
                self.speak("couldn't connect to server")

        elif "list all print files" in text:
            response = requests.get(url + 'files' + key)
            json_response = json.loads(response.text)
            print(status_code)
            if response.status_code == 200:
                self.speak('there is', json_response['files']['name'])
            if response.status_code == 404:
                self.speak("Could")

        # elif text == "set bed temp to" or text == "set bed temperature to":
        #     print(text)
        #     found = re.findall(r'\d+', text)
        #     if len(found) > 0:
        #        temp = int(found[0])
        #     data = {
        #        "command": "target",
        #        "target": temp
        #        }
        #     if response.status_code == 200:
        #        self.speak('temperature set to ' + temp + 'degrees')
        #     if response.status_code == 409 or 204:
        #        self.speak("couldn't set bed temperature")
        #     if response.status_code == 400:
        #        self.speak("couldn't determine the temperature you wanted")
        #     if response.status_code == 404:
        #        self.speak("couldn't connect to server")

        # elif "estimated print time" or "how long is the print" in greeting:
        #     response = requests.get(url + 'job' + key)
        #     json_response = json.loads(response.text)
        #     self.speak('the estimated print time is {}'.format(json_response['job']['estimatedPrintTime']))

        #elif "percent complete" or "completion percentage" in greeting:
            #response = requests.get(url + 'job' + key)
            #json_response = json.loads(response.text)
            #self.speak('the print is {} percent complete'.format(json_response['progress']['completion']))

    def general(self, text):
        if text == "what time is it":
            currentDT = datetime.datetime.now()
            self.speak(currentDT.strftime("%I:%M %p"))

        elif text == "what's todays date" or text == "todays date":
            x = datetime.datetime.now()
            self.speak(x.strftime("%B/%d/%Y"))



        # elif 'hello' in text:
        #     day_time = int(strftime('%H'))
        #     if day_time < 12:
        #        self.speak('Hello Sir. Good morning')
        #     elif 12 <= day_time < 18:
        #        self.speak('Hello Sir. Good afternoon')
        #     else:
        #        self.speak('Hello Sir. Good evening')


while True:
    if __name__ == '__main__':
        try:
            ph = PrinterHelper()
            text = ph.get_audio()
            ph.print_commands(text)
            ph.general(text)
        except KeyboardInterrupt:
            exit()
        except ConnectionError:
            speak('Connection error occured')
        except TypeError:
            speak('Invalid input')
        except TimeoutError:
            speak('Request took to long to respond')
        except json.decoder.JSONDecodeError:
            speak("printer couldn't connect to the server")
        #except:
           #print('other error occurred')



    # load model
    # while forever
        # Get text from person
        # command = model.predict(text)
        # no idea -
            # add new utterance to file, tell
            # retrain
        # run command
