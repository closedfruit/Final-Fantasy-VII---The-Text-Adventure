import re

def findDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''
    listOfDuplicates = []
    for elem in listOfElems:
        if listOfElems.count(elem) > 1:
            listOfDuplicates.append(elem)
    listOfDuplicates = list(set(listOfDuplicates))
    return listOfDuplicates

passagedata = []

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
