import re
import twinejs

templateFileName = '../template/index.html'
outputFileName = '../release/index.html'
nFiles = 22 #22 files. 1.html > 22.html

def getTemplate(fileName):
    print('getTemplate(): ' + fileName)

    with open (fileName, 'rt') as myfile:
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

def reindexSource(contents):
    print('reindexSource()')

    counter = 1

    pattern = '(pid="\d*")'
    items = re.findall(pattern, contents, re.MULTILINE|re.DOTALL)
    #does not work
    for item in items:
        newString = 'pid="' + str(counter) + '"'
        contents.replace(item, newString, 1)

    return contents

def build():
    print('build()')

    mergedPassageData = ''
    mergedPassageData += renderTemplete('../template/toc.html', getAllIndex())

    for x in range(nFiles):
        fileName = '../Stories/' + str(x+1) + '.html'
        print('parse file: ' + fileName)
        mergedPassageData = mergedPassageData + '\n' + twinejs.getAllPassagesFromFile(fileName)

    finalContents = renderTemplete(templateFileName, mergedPassageData)
    finalContents = reindexSource(finalContents)

    saveBuild(outputFileName, finalContents)

def buildWithNewEngine():
    print('buildWithNewEngine()')

    mergedPassageData = ''
    mergedPassageData += renderTemplete('../template/toc.html', getAllIndex())

    for x in range(nFiles):
        fileName = '../Stories/' + str(x+1) + '.html'
        print('parse file: ' + fileName)
        mergedPassageData = mergedPassageData + '\n' + twinejs.getAllPassagesFromFile(fileName)

    # manual replaces. order is important.
    mergedPassageData = mergedPassageData.replace('<tw', '\n<tw')
    mergedPassageData = mergedPassageData.replace('">', '">\n')
    mergedPassageData = mergedPassageData.replace('</tw', '\n</tw')
    #mergedPassageData = mergedPassageData.replace('\n\n', '\n')

    listRows = mergedPassageData.split('\n')

    for nRow in range(len(listRows)):
        striped = listRows[nRow].strip()
        if striped:
            if striped[0] != '<' and striped[0] != '}':
                listRows[nRow] = 'echo(\'' + listRows[nRow] + '\');'

        # is it's a starting element?
        pattern = '<tw-passagedata.*? name="(.*?)".*?>'
        result = re.findall(pattern, striped)
        if len(result) > 0:
            listRows[nRow] = 'case \'' + result[0] + '\':';
            #needs to clean name
        listRows[nRow] += '\n'

    #print(str(len(listRows)))
    #finalContents = renderTemplete(templateFileName, mergedPassageData)
    #finalContents = reindexSource(finalContents)
    newCode = "".join(listRows)

    # first the [[label|action]]
    pattern = '\[\[(.*?)\|(.*?)\]\]'
    replace = "<button type=\"button\" onclick=\"doIt(\\'\\2\\')\">\\1</button>"
    newCode = re.sub(pattern, r"" + replace + "", newCode)

    # then the [[label same as action]]
    pattern = '\[\[(.*?)\]\]'
    replace = "<button type=\"button\" onclick=\"doIt(\\'\\1\\')\">\\1</button>"
    newCode = re.sub(pattern, r"" + replace + "", newCode)

    # insert the break;
    newCode = newCode.replace('</tw-passagedata>', 'break;')

    finalContents = renderTemplete('../engine/index.html', newCode)
    with open('trash.html', 'w+') as f:
        f.write(finalContents)

    #saveBuild(outputFileName, finalContents)


buildWithNewEngine()
