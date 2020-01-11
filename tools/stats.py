import re
import datetime

import twinejs

listFileContents = [] # contents from the twine-files
nFilesToLoad = 22 # 1.html->22.html
pathToStories = '../Stories/' # folder where twine-files are stored
listPassagedata = []
statsPassagedata = ''

def stats():

    def loadContentsFromFiles():
        print('loadContentsFromFiles()')

        global listFileContents

        for x in range(nFilesToLoad):
            fileName = pathToStories + str(x+1) + '.html'
            listFileContents += twinejs.getStoryData(fileName)

    def findDuplicates(listOfElems):
        print('find duplicates')

        listOfDuplicates = []
        for elem in listOfElems:
            if listOfElems.count(elem) > 1:
                listOfDuplicates.append(elem)
        listOfDuplicates = list(set(listOfDuplicates))
        return listOfDuplicates

    def parseActor():
        print('parseActor()')

        listActor = []
        for contents in listFileContents:
            print('look for actors')

            # Actor: name and maybe more name: blabla
            pattern = '^(\w*|\s*): '
            result = re.findall(pattern, contents, re.MULTILINE)
            #print(result)
            listActor = listActor + result;

        print('actors and lines of dialogue: ')

        listUniqueActors = list(set(listActor))
        listUniqueActors.sort()

        for actor in listUniqueActors:
            print(actor + ': ' + str(listActor.count(actor)))

    def parsePassagedata():
        print('parsePassagedata()')

        global listPassagedata

        for contents in listFileContents:
            pattern = '<tw-passagedata.*? name="(.*?)".*?>'
            result = re.findall(pattern, contents)

            listPassagedata += result

            #stats
            print('number of total passagedata: ' + str(len(listPassagedata)))
            #print('number of unique passagedata: ' + str(len(set(listPassagedata))))

            #duplicates
            print('following duplicates found and needs to be fixed before a join: ')
            listOfDuplicates = findDuplicates(listPassagedata)
            print(listOfDuplicates)

    def saveToFile():
        print('saveToFile()')
        with open('stats.txt', 'w') as f:
            #passagedata.sort()
            final = ''
            ##final = final + 'date: ' + str(datetime.date.today()) + '\n'
            #final = final + 'passages: ' + str(len(passagedata)) + '\n'
            #final = final + 'story characters: ' + str(nAllText) + '\n'
            f.write(final)
            print('a list of stats dumped to stats.txt')

    def dosomething():
        with open('list-passage.txt', 'w') as f:
            passagedata.sort()
            final = ''
            for item in passagedata:
                final = final + item + '\n'
            f.write(final)
            print('a list of passagenames dumped to list-passage.txt')

    loadContentsFromFiles();
    parseActor()
    parsePassagedata()
    saveToFile()

print('start stats.py')
stats()
