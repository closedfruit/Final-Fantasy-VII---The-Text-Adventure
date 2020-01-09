import re

def getStoryData(fileName):
    print('getStoryData: ' + fileName)
    with open (fileName, 'rt') as myfile:  # Open lorem.txt for reading text
        contents = myfile.read()              # Read the entire file into a string
        pattern = '<tw-storydata.*?>(.*)</tw-storydata>'
        result = re.findall(pattern, contents, re.MULTILINE|re.DOTALL)
        return result[0]

def getStory():
    print('getStoryData: ' + fileName)
    with open (fileName, 'rt') as myfile:  # Open lorem.txt for reading text
        contents = myfile.read()              # Read the entire file into a string
        pattern = '<tw-storydata.*?>(.*)</tw-storydata>'
        result = re.findall(pattern, contents, re.MULTILINE|re.DOTALL)
        return result[0]

def getIndex(fileName):
    print('getIndex(): ' + fileName)

    with open (fileName, 'rt') as myfile:  # Open lorem.txt for reading text
        contents = myfile.read()              # Read the entire file into a string
        pattern = '<tw-passagedata.*?pid="1".*?>(.*?)</tw-passagedata>'
        result = re.findall(pattern, contents, re.MULTILINE|re.DOTALL)
        return result[0]

def getAllPassagesFromFile(fileName):
    print('getAllPassagesFromFile: ' + fileName)
    with open (fileName, 'rt') as myfile:  # Open lorem.txt for reading text
        contents = myfile.read()              # Read the entire file into a string
        start = contents.find('<tw-passagedata')
        stop = contents.rfind('tw-passagedata>')
        allPassages = contents[start:stop]
        return allPassages
