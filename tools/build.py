import re
import twinejs

templateTwinejsFileName = '../template/twinejs.html'
templateEngineFileName = '../template/engine.html'
templateTocFileName = '../template/toc.html'

nFiles = 22 #22 files. 1.html > 22.html

outputFileName = '../release/index.html'

def getTemplate(fileName):
    print('getTemplate(): ' + fileName)

    with open (fileName, 'rt') as myfile:
        return myfile.read()

def saveBuild(contents):
    print('saveBuild(): ' + outputFileName)

    with open(outputFileName, 'w+') as f:
        f.write(contents)

def buildToc():
    print('buildToc()')

    contents = ''

    for x in range(nFiles):
        fileName = '../Stories/' + str(x+1) + '.html'
        print('parse file: ' + fileName)

        contents += 'Chapter ' + str(x+1) + '\n'
        contents += twinejs.getFirstPassage(fileName) + '\n\n'

    return contents

def renderTemplete(fileName, contents):
    print('renderTemplete(): ' + fileName)

    with open (fileName, 'rt') as myfile:
        template = myfile.read()
        renderContents = template.replace('<contents>', contents)
        return renderContents

# reindex the pid for twinejs. does not work yet.
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

def buildAsTwinejs():
    print('buildAsTwine()')

    contents = ''
    contents += renderTemplete(templateTocFileName, buildToc())

    for x in range(nFiles):
        fileName = '../Stories/' + str(x+1) + '.html'
        print('parse file: ' + fileName)
        contents += '\n' + twinejs.getAllPassagesFromFile(fileName)

    contents = renderTemplete(templateTwinejsFileName, contents)
    contents = reindexSource(contents)

    saveBuild(contents)

def buildAsNewEngine():
    print('buildWithNewEngine()')

    contents = ''
    contents += renderTemplete(templateTocFileName, buildToc())

    print('merge data.')
    for x in range(nFiles):
        fileName = '../Stories/' + str(x+1) + '.html'
        print('merge file: ' + fileName)
        contents += '\n' + twinejs.getAllPassagesFromFile(fileName)

    # manual replaces. order is important.
    contents = contents.replace('<tw', '\n<tw')
    contents = contents.replace('">', '">\n')
    contents = contents.replace('</tw', '\n</tw')
    #mergedPassageData = mergedPassageData.replace('\n\n', '\n')

    listRows = contents.split('\n')

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
    contents = "".join(listRows)

    # first the [[label|action]]
    pattern = '\[\[(.*?)\|(.*?)\]\]'
    replace = "<a href=\"#\" onclick=\"doIt(\\'\\2\\')\">\\1</a>"
    contents = re.sub(pattern, r"" + replace + "", contents)

    # then the [[label same as action]]
    pattern = '\[\[(.*?)\]\]'
    replace = "<a href=\"#\" onclick=\"doIt(\\'\\1\\')\">\\1</a>"
    contents = re.sub(pattern, r"" + replace + "", contents)

    # insert the break;
    contents = contents.replace('</tw-passagedata>', 'break;')

    contents = renderTemplete(templateEngineFileName, contents)

    #remove empty empty lines
    while contents.replace('\n\n', '\n') != contents:
        contents = contents.replace('\n\n', '\n')

    saveBuild(contents)


buildAsNewEngine()
