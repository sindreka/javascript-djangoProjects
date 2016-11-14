# Import lots of stuff
import django
from urllib import request
# This function must run every two hours.
from bracketVisualizer.model import bracketBatch, bracketMatch


class AppURLopener(request.FancyURLopener):
    version = "User-Agent:bracketVisualizer:v0.2 (by /u/schpere)"
 

def getBatchResults(batchNumber):
    batchNumber = str(batchNumber)
    request._urlopener = AppURLopener
    url = "http://reddit.com/r/mtgbracket.json"
    source = urllib.urlopen(url)
    posts = json.load(source)["data"]["children"]
    for post in posts:
        if post['data']['title'] == "Batch " + batchNumber + " results":
            url = "http://reddit.com" + post['data']['permalink']
            break
    source = urllib.urlopen(url + ".json")
    comments = json.load(source)[1]['data']['children']
    for comment in comments:
        if comment['data']['body'].count('%') >= 32:
            post = comment['data']['body']
            return post[post.find("*")+2:].split("\n* ")

def getInfoFromLine(line):
    info = line.split(" defeats ")
    info = [info[0]] + info[1].split(' with ')
    info[2] = info[2][0:info[2].find('%')]
    info.append(str(round(100-float(info[-1]),1)))
    return info

def getInfoFromPost(text):
    info = []
    for line in text:
        info.append(getInfoFromLine(line))
    return info

def getImageFromCardName(card):
    #card = card.replace('Ae','Æ') 
    # Ae won't work since magiccards.info uses æ

    infoSite = "http://magiccards.info/query?q=" + card.replace(' ','+').replace('ö','o') + "&v=card&s=cname"
    page = request.urlopen(infoSite)
    data = page.read()
    expression = '(?<=\<img src=")http://magiccards.info/scans/en/[a-z,0-9]{1,3}/[0-9]{0,3}.jpg(?="\s*alt="' + card + ')'
    img = re.search(expression,data.decode("utf-8"))
    return img.group(0)

def getResults(text):
    cardTable = getInfoFromPost(text)
    results = []
    for line in cardTable:
        results.append([[line[0], line[2], getImageFromCardName(line[0])], [line[1], line[3], getImageFromCardName(line[1])]])
    return results


def addToDatabase():
    # Get batchNumber
    try:
        batchNumber= bracketBatch.objects.all().order_by('-id')[0].batchNumber
    except:
        batchNumber = 1

    # Check if new batchResults are avilable
    results = getBatchResults(batchNumber)
    resultMatrix = getResults(results)

    # Add result key to matchBatch
    B = bracketBatch(batchNumber+1)
    B.save()
    for row in resultmatrix:
        # Add results to matchResult
        match = bracketMatch(batch=B, winnerURL = row[0][1], winnerName = row[0][1], winnerProsent = row[0][1],
                                       loserURL = row[0][1],  loserName = row[1][1],  loserProsent = row[1][1])
        match.save()
        #del match





addToDatabase()


