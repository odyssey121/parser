import re
import json
from queries import getSourceByName, insertSource
from findFeed import findFeed
from bs4 import BeautifulSoup as bs4
import requests
from sys import argv
import sys
sys.path.append("..")


class GetSource:

    REG_EXP = {
        'youtube': re.compile(
            r'(https?:\/\/)?(www\.)?youtu((\.be)|(be\..{2,5}))\/((user)|(channel))\/', re.IGNORECASE
        ),
        'tg': re.compile(
            r'(https?:\/\/)?(www\.)?t(\.me)\/.+', re.IGNORECASE
        ),
        'vk': re.compile(
            r'(https?:\/\/)?(www\.)?vk(\.com|\.ru)\/.+', re.IGNORECASE
        ),
    }
    SOURCE = {
        'type': None
    }

    def __init__(self, name):
        self.normalizeName = self.handlingName(name)
        self.sourceId = self.checkInDb(self.normalizeName)
        self.SOURCE['type'] = self.getType(self.normalizeName)

    def handlingName(self, name):
        newName = None
        regex = re.compile(
            r'^((?:http)s?://)|(www.)', re.IGNORECASE)
        try:
            newName = re.sub(re.match(regex, name).group(), '', name) if re.match(
                regex, name) is not None else name
        except Exception as error:
            print(error)
        return newName.strip().rstrip('/')

    def checkInDb(self, name):
        checkStatus = None
        response = getSourceByName(name)
        checkStatus = response[0]['id'] if len(response) else checkStatus
        return checkStatus

    def getType(self, name):
        source = None
        for key in self.REG_EXP:
            if re.match(self.REG_EXP[key], name) is not None:
                source = key
        return source if source else 'site' if name else None

    def validateSource(self):
        sourceObj = self.SOURCE
        sourceObj['name'] = self.normalizeName
        if self.SOURCE['type'] not in self.REG_EXP.keys():
            sourceObj['service_link'] = findFeed(self.normalizeName)
        return sourceObj if 'service_link' not in sourceObj.keys() or sourceObj['service_link'] else False

    @staticmethod
    def saveSource(name=None, service_link=None, kind='site'):
        regex = re.compile(r'^((?:http)s?://)|(www.)', re.IGNORECASE)
        if name and service_link:
            narmalizeName = re.sub(re.match(regex, name).group(), '', name) if re.match(
                regex, name) is not None else name

            sourceObj = {
                'type': kind,
                'name': narmalizeName.strip().rstrip('/'),
                'service_link': service_link.strip()
            }
            response = insertSource(sourceObj)
        else:
            raise Exception('error! Not name or service link')
        return response

    def start(self):
        response = None
        if self.sourceId is None:
            result = self.validateSource()
            if result:
                service_link = result.get('service_link', None)
                if service_link and len(service_link) > 1:
                    response = result['service_link']
                else:
                    link = result.get('service_link', None)
                    if link:
                        result['service_link'] = ''.join(link)
                    response = insertSource(result)
            else:
                response = 'Error service link not found'
        else:
            response = self.sourceId
        return response


if __name__ == '__main__':
    if len(argv) == 2:
        getSource = GetSource(argv[1])
        print(getSource.start())
    # elif len(argv) == 1:
    #     getSource = GetSource('https://reorga.ru/')
    #     print(getSource.start())
    #     # print(GetSource.saveSource('yaplakal.com','https://www.yaplakal.com/news.xml'))
    else:
        print('error введите название источника')
