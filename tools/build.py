import re
import twinejs

# sources to read from
pathToStories = '../Stories/'
templateTwinejsFileName = '../template/twinejs.html'
templateEngineFileName = '../template/engine.html'
templateTocFileName = '../template/toc.html'

nFiles = 22 #22 files. 1.html > 22.html

outputFileName = '../release/index.html' # the finished the product after build is done.

# save the build contents to pre-configed filename
def saveBuild(contents):
    print('saveBuild(): ' + outputFileName)

    with open(outputFileName, 'w+') as f:
        f.write(contents)

# build the 'table of contents' from multiple files and return the results as string
def buildToc():
    print('buildToc()')

    contents = ''

    for x in range(nFiles):
        fileName = pathToStories + str(x+1) + '.html'
        print('parse file: ' + fileName)

        contents += '<h3>Chapter ' + str(x+1) + '</h3>\n'

        firstPassage = twinejs.getFirstPassage(fileName)
        firstPassage = firstPassage.split('\n')

        for row in range(len(firstPassage)):
            firstPassage[row] = '<h4>' + firstPassage[row] + '</h4>\n\n'

        contents += "".join(firstPassage)#???

    return contents

# open file and replace <contents> with contents variable and returns the result as a string
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

# create a playable file in the format of twinejs.
def buildAsTwinejs():
    print('buildAsTwine()')

    contents = ''
    contents += renderTemplete(templateTocFileName, buildToc())

    for x in range(nFiles):
        fileName = pathToStories + str(x+1) + '.html'
        print('parse file: ' + fileName)
        contents += '\n' + twinejs.getAllPassagesFromFile(fileName)

    contents = renderTemplete(templateTwinejsFileName, contents)
    contents = reindexSource(contents)

    saveBuild(contents)

# create a playable file in the new format.
def buildAsNewEngine():
    print('buildWithNewEngine()')

    contents = ''
    contents += renderTemplete(templateTocFileName, buildToc())

    # get passage contents from all source files and merge it into one string.
    print('merge data.')
    for x in range(nFiles):
        fileName = pathToStories + str(x+1) + '.html'
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
            if striped[0] != '}' and listRows[nRow].find('</tw-passagedata>') < 0 and listRows[nRow].find('{') != len(listRows[nRow])-1 and listRows[nRow].find('//') < 0:
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

    # join the single rowns into one big string.
    contents = "".join(listRows)

    # [[variable:name]] -> 'name'.
    #pattern = '\[\[variable:(.*?)\]\]'
    #replace = "\\1"
    #contents = re.sub(pattern, r"" + replace + "", contents)

    # is the link inside an 'if' we dont want a <a> element. '[[passageName]]' -> 'passageName'.
    pattern = 'if(.*?)\[\[(.*?)\]\](.*?)'
    replace = "if\\1'\\2'\\3"
    contents = re.sub(pattern, r"" + replace + "", contents)

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

    # insert the contents into our template
    contents = renderTemplete(templateEngineFileName, contents)

    #remove double space
    print('remove double space.')
    while contents.replace('  ', ' ') != contents:
        contents = contents.replace('  ', ' ')

    #remove empty lines
    print('remove empty lines.')
    while contents.replace('\n\n', '\n') != contents:
        contents = contents.replace('\n\n', '\n')

    # fix special characters. needs improvement.
    contents = contents.replace('&lt;', '<') # needed for < in 'if' statments
    contents = contents.replace('&gt;', '>') # needed for > in 'if' statments

    saveBuild(contents)


buildAsNewEngine()
