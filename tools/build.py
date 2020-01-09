import twinejs

templateFileName = '../template/index.html'
outputFileName = '../release/index.html'
nFiles = 22 #22 files. 1.html > 22.html

def getTemplate(fileName):
    print('getTemplate(): ' + fileName)

    with open (fileName, 'rt') as myfile:  # Open lorem.txt for reading text
        return myfile.read()

def saveBuild(fileName, contents):
    print('saveBuild(): ' + fileName)

    with open(fileName, 'w+') as f:
        f.write(contents)

def getAllIndex():
    print('getAllIndex()')

    mergedIndexData = ''

    for x in range(nFiles):
        fileName = '../Stories/' + str(x+1) + '.html'
        print('parse file: ' + fileName)

        mergedIndexData += 'Chapter ' + str(x+1) + '\n'
        mergedIndexData += twinejs.getIndex(fileName) + '\n\n'

    return mergedIndexData

def renderTemplete(fileName, contents):
    print('renderTemplete(): ' + fileName)

    with open (fileName, 'rt') as myfile:
        template = myfile.read()
        renderContents = template.replace('<contents>', contents)
        return renderContents

def build():
    print('build()')

    mergedPassageData = ''
    mergedPassageData += renderTemplete('../template/toc.html', getAllIndex())

    for x in range(nFiles):
        fileName = '../Stories/' + str(x+1) + '.html'
        print('parse file: ' + fileName)
        mergedPassageData = mergedPassageData + '\n' + twinejs.getAllPassagesFromFile(fileName)

    finalContents = renderTemplete(templateFileName, mergedPassageData)

    saveBuild(outputFileName, finalContents)

build()
