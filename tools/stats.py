import re
import datetime

def findDuplicates(listOfElems):
    print('find duplicates')
    ''' Check if given list contains any duplicates '''
    listOfDuplicates = []
    for elem in listOfElems:
        if listOfElems.count(elem) > 1:
            listOfDuplicates.append(elem)
    listOfDuplicates = list(set(listOfDuplicates))
    return listOfDuplicates

def getStoryData(fileName):
    print('getStoryData: ' + fileName)
    with open (fileName, 'rt') as myfile:  # Open lorem.txt for reading text
        contents = myfile.read()              # Read the entire file into a string
        pattern = '<tw-storydata.*?>(.*)</tw-storydata>'
        result = re.findall(pattern, contents, re.MULTILINE|re.DOTALL)
        return result[0]

def listActor():
    print('list actors')
    listActor = []
    #22 files. 1.html > 22.html
    for x in range(22):
        fileName = '../Stories/' + str(x+1) + '.html'
        contents = getStoryData(fileName)

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

listActor()

def listPassage():
    passagedata = []

    print('scan')
    #22 files. 1.html > 22.html
    for x in range(22):
        fileName = '../Stories/' + str(x+1) + '.html'
        with open (fileName, 'rt') as myfile:  # Open lorem.txt for reading text
            contents = myfile.read()              # Read the entire file into a string

            # Three digit number followed by space followed by two digit number
            pattern = '<tw-passagedata.*? name="(.*?)".*?>'
            result = re.findall(pattern, contents)

            print(fileName + ': ' + str(len(result)))

            passagedata = passagedata + result

            #print(result)

    #stats
    print('number of total passagedata: ' + str(len(passagedata)))
    print('number of unique passagedata: ' + str(len(set(passagedata))))

    #duplicates
    print('following duplicates found and needs to be fixed before a join: ')
    listOfDuplicates = findDuplicates(passagedata)
    print(listOfDuplicates)

    return passagedata

passageData = listPassage()

with open('list-passage.txt', 'w') as f:
    passagedata.sort()
    final = ''
    for item in passagedata:
        final = final + item + '\n'
    f.write(final)
    print('a list of passagenames dumped to list-passage.txt')




# write to file
print('write to file.')
with open('stats.txt', 'w') as f:
        passagedata.sort()
        final = ''
        final = final + 'date: ' + str(datetime.date.today()) + '\n'
        final = final + 'passages: ' + str(len(passagedata)) + '\n'
        final = final + 'story characters: ' + str(nAllText) + '\n'
        f.write(final)
        print('a list of stats dumped to stats.txt')
