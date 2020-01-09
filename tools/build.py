import twinejs

templateFileName = '../template/index.html'
outputFileName = '../release/index.html'

def getTemplate(fileName):
    print('getTemplate(): ' + fileName)

    with open (fileName, 'rt') as myfile:  # Open lorem.txt for reading text
        return myfile.read()

def saveBuild(fileName, contents):
    print('saveBuild(): ' + fileName)

    with open(fileName, 'w+') as f:
        f.write(contents)

def build():
    print('build()')

    templateContents = getTemplate(templateFileName)

    mergedPassageData = ''

    #22 files. 1.html > 22.html
    for x in range(22):
        fileName = '../Stories/' + str(x+1) + '.html'
        print('parse file: ' + fileName)
        mergedPassageData = mergedPassageData + '\n' + twinejs.getAllPassagesFromFile(fileName)

    finalContents = templateContents.replace('<content>', mergedPassageData)

    saveBuild(outputFileName, finalContents)

build()
