__author__ = "Ian Chan"
__copyright__ = "Copyright 2020, Ian Chan"
__credits__ = ["Ian Chan"]
__license__ = "GPL v3"
__version__ = "1"
__maintainer__ = "Ian Chan"
__email__ = "me@ian-chan.me"
__status__ = "Production"

import json, requests #import

def messageFormat(composedMessage, inputType, compare = False, data = 'data', oldData = 'oldData', newData = 'newData'):
    if inputType == 'message':
        composedMessage = composedMessage.replace("{}", "\n")
        composedMessage = composedMessage.replace("{linebreak}", "\n\n")
        composedMessage = composedMessage.replace("{customizeBegin}", "")
        composedMessage = composedMessage.replace("{customizeEnd}", "")
    elif inputType == 'page':
        composedMessage = composedMessage.replace("{}", "</br>")
        composedMessage = composedMessage.replace("{linebreak}", "</br></br>")
        composedMessage = composedMessage.replace("{customizeBegin}", "")
        composedMessage = composedMessage.replace("{customizeEnd}", "")
    elif inputType == 'call':
        composedMessage = composedMessage.replace("{}", ". ")
        composedMessage = composedMessage.replace("{linebreak}", ". ")
        composedMessage = composedMessage.replace("{customizeBegin}", "Latest ")
        composedMessage = composedMessage.replace("{customizeEnd}", ". Thank you for calling.")
    elif inputType == 'raw':
        composedMessage = data
    if (compare == True) and (oldData == newData):
        composedMessage = 'No Change'
    else:
        pass
    return composedMessage

def getData(inputType, country = 'us', compare = False, altAPI = False):
    restore = False
    if compare == True:
        try:
            with open(country, "r") as readFile:
                oldData = readFile.read()
        except:
            oldData = 'None'
    else:
        pass
    #set url
    if altAPI == True: 
        url = 'https://corona.lmao.ninja/countries/' + country
    else:
        url = 'https://corona.lmao.ninja/countries/' + country
    r = requests.get(url)
    try:
        with open(country, 'r+') as src, open(country + '.bak', 'w+') as dst:
            dst.write(src.read()) #Backup
    except:
        pass
    with open(country, 'wb') as outfile:
        outfile.write(r.content) #Get latest and save
    with open(country, "r+") as dataFile:
        data = dataFile.read() #sets data to latest data
        if data == 'Country not found': #if not available
            print("API error") #restore
            restore = True
            altAPI = True
        else:
            if compare == True: newData = data #sets new data to latest data for comparison
            try:
                formattedData = json.loads(str(data)) #json decode
            except:
                restore = True
                altAPI = True
    if restore == True:
        #if restore was enabled previously
        with open(country + '.bak', 'r+') as src, open(country, 'w+') as dst:
            dst.write(src.read()) #restore backup
        with open(country, "r") as dataFile: #Re read restored data
            data = dataFile.read()
            if compare == True: newData = data #sets newData to restored value
            formattedData = json.loads(str(data)) #json decode
    data = formattedData #sets data variable to json decoded
    totalCases = data['cases']
    todayCases = data['todayCases']
    totalDeath = data['deaths']
    todayDeath = data['todayDeaths']
    recovered = data['recovered']
    critical = data['critical']
    active = data['active']
    fatalityRate = totalDeath / totalCases * 100
    fatalityRatePercentage = round(fatalityRate, 2)
    fatalityRateRounded = round(fatalityRate,0)
    fatalityRatio = 100 - fatalityRateRounded
    fatalityRatio = int(fatalityRatio)
    composedMessage = ("{customizeBegin}COVID-19 Updates{linebreak}Total cases: "+str(totalCases)+"{}Cases today: "+str(todayCases)+"{}Critical cases: "+str(critical)+"{}Recovered: "+str(recovered)+"{}Total deaths: "+str(totalDeath)+"{}Deaths today: "+str(todayDeath)+"{}Current fatality rate: "+str(fatalityRatePercentage)+"%{}"+str(fatalityRatio)+" in 100 people will live based on current statistics{customizeEnd}")
    if compare == True:
        composedMessage = messageFormat(composedMessage, inputType, compare, data, oldData, newData)
    elif compare == False:
        composedMessage = messageFormat(composedMessage, inputType)
    return composedMessage

def getWorld(inputType, altAPI = False):
    restore = False
    if altAPI == True: 
        url = 'https://corona.lmao.ninja/all'
    elif altAPI == False:  
        url = 'https://corona.lmao.ninja/all/'
    r = requests.get(url)
    try:
        with open('world', 'r+') as src, open('world' + '.bak', 'w+') as dst:
            dst.write(src.read()) #Backup
    except:
        pass
    with open('world', 'wb') as outfile:
        outfile.write(r.content) #Get latest and save
    with open('world', "r+") as dataFile:
        data = dataFile.read() #sets data to latest data
        if data == 'Country not found': #if not available
            print("API error") #restore
            restore = True
            altAPI = True
        else:
            try:
                formattedData = json.loads(str(data)) #json decode
            except:
                restore = True
                altAPI = True
    if restore == True:
        #if restore was enabled previously
        with open('world' + '.bak', 'r+') as src, open('world', 'w+') as dst:
            dst.write(src.read()) #restore backup
        with open('world', "r") as dataFile: #Re read restored data
            data = dataFile.read()
            formattedData = json.loads(str(data)) #json decode
    data = formattedData #sets data variable to json decoded
    cases = data['cases']
    death = data['deaths']
    recovered = data['recovered']
    fatalityRate = death / cases * 100
    fatalityRatePercentage = round(fatalityRate, 2)
    fatalityRateRounded = round(fatalityRate,0)
    fatalityRatio = 100 - fatalityRateRounded
    fatalityRatio = int(fatalityRatio)
    composedMessage = "COVID-19 Worldwide Data{linebreak}Total cases: "+str(cases)+"{}Total deaths: "+str(death)+"{}Total recovered: "+str(recovered)+"{}Current fatality rate: "+str(fatalityRatePercentage)+"%{}"+str(fatalityRatio)+" in 100 people will live based on current statistics{customizeEnd}"
    composedMessage = messageFormat(composedMessage, inputType)
    return composedMessage

def convertCountry(message):
    message = message.lower()
    if 'united kingdom' in message:
        message = 'uk'
    elif 'united states' in message:
        message = 'us'
    elif 'south korea' in message:
        message = 's. korea'
    elif 'united arab emirates' in message:
        message = 'uae'
    else:
        message = message
    return message