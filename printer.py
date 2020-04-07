import requests
import json
import jsonpath
import datetime
import re

url = "http://10.0.0.63/api/"
key = "?apikey=BCDE97A05BB04135BD2B9097AE2F5B0A"

# url = 'http://localhost:5000/'
# key = "?apikey=0ED88487E13B445CAA56462107C6D0E6"


def print_commands(greeting):
    if "printer state" in greeting:
        response = requests.get(url + 'printer' + key)
        # finds specific part of state operational or not
        json_response = json.loads(response.text)
        if response.status_code == 200:
            print('state:', json_response['state']['text'])
        elif response.status_code == 500:
            print('server error occured')
        elif response.status_code == 409:
            print("couldn't get any data")

    if greeting == "start print":
        data = {
        "command": "start"
        }
        response = requests.post(url + 'job' + key, json = data) # starts the 3d printer
        if response.status_code == 200:
            print('Printer has started')
        if response.status_code == 409:
            print("print couldn't be started")
        if response.status_code == 204:
            print("haven't loaded a print yet")

    if "cancel print" in greeting:
        data = {
        "command": "cancel"
        }
        response = requests.post(url + 'job' + key, json = data)
        if response.status_code == 200:
            print('print has cancelled')
        if response.status_code == 409:
            print("print couldn't be cancelled")

    if greeting == "restart print":
        data = {
        "command": "restart"
        }
        response = requests.post(url + 'job' + key, json = data)
        if response.status_code == 200:
            print('print has restarted')
        if response.status_code == 409:
            print("print couldn't restart")

    if "pause print" in greeting:
        data = {
        "command": "pause",
        "action": "pause"
        }
        response = requests.post(url + 'job' + key, json = data)
        if response.status_code == 200:
            print('print has paused')
        if response.status_code == 409:
            print("print couldn't be paused")

    if greeting == "resume print":
        data = {
        "command": "pause",
        "action": "resume"
        }
        response = requests.post(url + 'job' + key, json = data)
        if response.status_code == 200:
            print('print has resumed')
        if response.status_code == 409:
            print("print couldn't be resumed")

    if "temp of bed" in greeting:
        response = requests.get(url + 'printer' + key)
        # determines the temps of all printer parts
        json_response = json.loads(response.text)
        if response.status_code == 200:
            print('temp:', json_response['temperature']['bed']['actual'])
        if response.status_code == 409:
            print("bed temperature couldn't be found")

    if "temp of nozzle" in greeting:
        response = requests.get(url + 'printer' + key)
        # determines the temps of all printer extruder
        json_response = json.loads(response.text)
        if response.status_code == 200:
            print('temp:', json_response['temperature']['tool0']['actual'])
        if response.status_code == 409:
            print("extruder temperature couldn't be found")

    if "time remaining on print" in greeting:
        response = requests.get(url + 'job' + key)
        json_response = json.loads(response.text)
        print('time remaining:', json_response['progress']['printTimeLeft'])

    if "how long has the print been going" in greeting:
        response = requests.get(url + 'job' + key)
        json_response = json.loads(response.text)
        print('time:', json_response['progress']['printTime'])

    if "estimated print time" or "how long is the print" in greeting:
        response = requests.get(url + 'job' + key)
        json_response = json.loads(response.text)
        print('estimated time:', json_response['job']['estimatedPrintTime'])

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
            print('temperature set to ' + str(temp) + 'degrees')
        if response.status_code == 409:
            print("couldn't set temperature")
        if response.status_code == 400:
            print("couldn't determine the temperature you wanted")
        if response.status_code == 404:
            print("couldn't connect to server")

    elif "list all print files" in text:
        response = requests.get(url + 'files' + key)
        json_response = json.loads(response.text)
        print(status_code)
        if response.status_code == 200:
            print('there is', json_response['files']['name'])
        if response.status_code == 404:
            print("Couldn't")


    #if "percent complete" or "completion percentage" in greeting:
        #response = requests.get(url + 'job' + key)
        #json_response = json.loads(response.text)
        #print('percent complete:', json_response['progress']['completion'])

#def general(greeting):
#    if "what time is it" or "tell me the time" in greeting:
#        currentDT = datetime.datetime.now()
#        print (currentDT.strftime("%I:%M %p")

while True:
    if __name__ == '__main__':
        try:
            greeting = input('What would you like?: ')
            print_commands(greeting)
        except KeyboardInterrupt:
            print('Manual break by user')
            exit()
        except ConnectionError:
            print('Connection error occured')
        except TypeError:
            print('Invalid input')
        except TimeoutError:
            print('Request took to long to respond')
        except json.decoder.JSONDecodeError:
            print("printer couldn't connect to the server")
        #except:
            #print('other error occurred')
