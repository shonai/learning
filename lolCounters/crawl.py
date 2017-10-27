import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup

champs = []
baseChampsUrl = "http://www.lolcounter.com/champions"
req = requests.get(baseChampsUrl).text
soup = BeautifulSoup(req, 'html.parser')
champNames = soup.find_all('div', {'class':'left champ-img'})
for item in champNames:
    tmp = []
    tmp.append(baseChampsUrl+ '/'+item['find'])
    tmp.append(item['find'])
    tmp.append([])
    champs.append(tmp)

for item in champs:
    print item[0]
    req = requests.get(item[0]).text
    soup = BeautifulSoup(req, 'html.parser')
    weakBlock = soup.find('div', {'class':'weak-block'})
    weakChampBlocks = weakBlock.find_all('div', {'class':'champ-block'})
    for champBlock in weakChampBlocks:
        champName = champBlock.find('div', {'class':'name'}).text
        item[2].append(str(champName))

print 'finish scan'

resFile = open('resFile.txt', 'w')
for item in champs:
    counters = ''
    for counter in item[2]:
        counters = counters + counter + '<br>'
    resFile.write(str(item[1])+'\t' + str(counters) + '\n')
    print 'champ written'
resFile.close()


html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lol Counters</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<style type="text/css">
    .bs-example{
        margin: 20px;
    }
</style>
</head>
<body>
<div class="bs-example">
    <div class="panel-group" id="accordion">
                            '''
resFile = open('resFile.txt', 'r')
i = 0
for line in resFile:
    champ, counters = line.split('\t')
    toAdd = '''<div class="panel panel-default">
            <div class="panel-heading">
                <h4 class="panel-title">
                    <a data-toggle="collapse" data-parent="#accordion" href="#collapse''' + str(i) + '">'
    toAdd = toAdd + champ
    toAdd = toAdd + '''</a>
                </h4>
            </div>
            <div id="collapse'''+str(i)+'''" class="panel-collapse collapse">
                <div class="panel-body">
                    <p>'''
    toAdd = toAdd + counters
    toAdd = toAdd + '''</p>
                </div>
            </div>
        </div>'''
    html = html+toAdd
    i+=1

html = html + '''
    </div>
</div>
</body>
</html>'''

htmlFile = open('counters.html', 'w')
htmlFile.write(html)