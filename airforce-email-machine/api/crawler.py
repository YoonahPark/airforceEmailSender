import requests
from bs4 import BeautifulSoup
from api.tools.tagsCleaner import InformationCleaner, EmailWritingPeriodCleaner
from api.models.models import Airman

class _AirmansWithSameProfileGetter:
    def __init__(self, airman):
        self.name = airman.name
        self.birthDate = airman.birthDate
        self.__createHtmlParser()
        
    def __createHtmlParser(self):
        url = "https://www.airforce.mil.kr/user/emailPicViewSameMembers.action?siteId=last2&searchName="+self.name+"&searchBirth="+self.birthDate
        response = requests.get(url, verify=False)
        htmlDoc = response.text
        self.parser = BeautifulSoup(htmlDoc, 'html.parser')
    
    def __getSameResultList(self):
        sameResultListTags = self.parser.find(class_='SameResultList')
        sameResultList = sameResultListTags.find_all('li')
        return sameResultList
    
    def __getInformations(self, sameResult):
        informationTags = sameResult.find(class_='info')
        informations = informationTags.find_all('dd')
        informations = [InformationCleaner(information).clean() for information in informations]
        return informations
    
    def __getMemberSequence(self, sameResult):
        choiceTag = sameResult.find(class_='choice')
        memberSequence = choiceTag.get('onclick')[14:23]
        return memberSequence
        
    def __getAirmanProfile(self, sameResult):
        airman = Airman(self.name, self.birthDate)
        airman.memberSequence = self.__getMemberSequence(sameResult)
        informations = self.__getInformations(sameResult)
        airman.setInformations(informations)
        return airman
    
    def getAirmansWithSameProfile(self):
        sameResultList = self.__getSameResultList()
        airmans = []
        for sameResult in sameResultList:
            airmans.append(self.__getAirmanProfile(sameResult))
        self.airmansWithSameProfile = airmans
        return airmans

class _EmailWritingPeriodGetter:
    def __init__(self, airman):
        self.name = airman.name
        self.birthDate = airman.birthDate
        self.memberSequence = airman.memberSequence
        self.indexOfEmailWritingPeriod = 4
        self.__createHtmlParser()
    
    def __createHtmlParser(self):
        url = "https://www.airforce.mil.kr/user/indexSub.action?codyMenuSeq=156893223&siteId=last2&menuUIType=top&dum=dum&command2=getEmailList&searchName="+self.name+"&searchBirth="+self.birthDate+"&memberSeq="+self.memberSequence
        response = requests.get(url, verify=False)
        htmlDoc = response.text
        self.parser = BeautifulSoup(htmlDoc, 'html.parser')
    
    def getAirmanWithEmailWritingPeriod(self):
        informationTags = self.parser.find(class_='info')
        informations = informationTags.find_all('dd')
        emailWritingPeriod = EmailWritingPeriodCleaner(informations[self.indexOfEmailWritingPeriod]).clean()
        return emailWritingPeriod
    
class AirmanCrawler:
    def __init__(self, airman):
        self.airman = airman
    
    def getList(self):
        self.airmans = _AirmansWithSameProfileGetter(self.airman).getAirmansWithSameProfile()
        return self.airmans
    
    def selectAirman(self, airmanIndex):
        self.airman = self.airmans[airmanIndex]
        _EmailWritingPeriodGetter(self.airman).getAirmanWithEmailWritingPeriod
        return self.airman
    