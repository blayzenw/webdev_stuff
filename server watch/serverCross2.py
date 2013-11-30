from BeautifulSoup import BeautifulSoup
import urllib2
import winsound, sys
import time

tollerence = 3
servers = [['Desertion','http://freedom001.game.wurmonline.com:8080/mrtg/wurm.html'],['Serenity','http://freedom002.game.wurmonline.com:8080/mrtg/wurm.html'],['Affliction','http://freedom002.game.wurmonline.com:8080/mrtg/wurm.html'],['Elevation','http://wild001.game.wurmonline.com:8080/mrtg/wurm.html']]

v = [42, 58, 58, 32]
v2 = [52, 48, 58, 32]

def playSound(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
    
def grabPlayers(url):
    #Grab page and parse it
    page = urllib2.urlopen(url)
    pageSource = page.read()
    soup = BeautifulSoup(pageSource)

    #The player count should be under <tr class="out">
    players = soup.findAll('td')[2]

    #Put it into a string so we can work with it
    playerStr = str(players)

    #Format the string so we only have the number of players
    playerStr = playerStr[4:len(playerStr)]
    count = 0
    while(playerStr[count] != ' '):
        count += 1
    playerStr = playerStr[0:count]

    #Convert it to an int
    playerInt = int(playerStr)
    return playerInt
    
def buildCountList():
    serverCount = []
    serverCount.append(grabPlayers(servers[0][1]))
    serverCount.append(grabPlayers(servers[1][1]))
    serverCount.append(grabPlayers(servers[2][1]))
    serverCount.append(grabPlayers(servers[3][1]))
    return serverCount

def checkServers():
    lastServerCount = buildCountList()
    serverCount = lastServerCount
    while(True):
        timeTillNextUpdate = time.localtime()[4]%5
        print 'sleeping for ' + str(timeTillNextUpdate)
        time.sleep((timeTillNextUpdate*60)+15)
        lastServerCount = serverCount
        serverCount = buildCountList()

        dif = checkDif(serverCount,lastServerCount)
        alertChange(dif)

def checkDif(serverCountOld, serverCountNew):
    report = []
    serverChange = [0,0,0]
    count = 0
    while(count < 3):
        serverChange[count] = serverCountNew[count]-serverCountOld[count]
        count += 1
    #print 'done'
    
    #print serverChange
    count = 0
    count2 = 0
    while(count < 3):
        while(count2 < 3):
            if abs(serverChange[count]) >= 3 and abs(serverChange[count2]) >= 3:
                if (abs(serverChange[count]-serverChange[count2])/2) >= tollerence:
                    report.append([serverChange.index(serverChange[count]), serverChange.index(serverChange[count2]), abs(serverChange[count]-serverChange[count2])/2])
                    #print report
            count2 += 1
        count += 1
        count2 = count

    return report

def alertChange(reports):
    if(reports == []):
        return
    
    for report in reports:
        server1 = servers[report[0]][0]
        server2 = servers[report[1]][0]
        playerChange = report[2]

        print 'There was a change of ' + str(playerChange) + ' players from ' + str(server1) + ' to ' + str(server2)

        
    playSound('beep')


#checkServers()
