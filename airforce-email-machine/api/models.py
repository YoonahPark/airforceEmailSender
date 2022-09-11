class Sender:
    def __init__(self, name, address, addressDetail):
        self.name = name
        self.address = address
        self.addressDetail = addressDetail
        
class Email:
    def __init__(self, relationship, title, contents, password):
        self.relationship = relationship
        self.title = title
        self.contents = contents
        self.password = password

class Airman:
    def __init__(self, name, birthDate):
        self.name = name
        self.birthDate = birthDate
        
    def setInformations(self, list):
        self.division = list[0]
        self.enlistedAt = list[1]
        self.dischargedAt = list[2]
    
    def setMemberSequence(self, memberSequence):
        self.memberSequence = memberSequence
        
    def setUrl(self, memberSequence):
        self.url = "https://www.airforce.mil.kr/user/indexSub.action?codyMenuSeq=156893223&siteId=last2&menuUIType=top&dum=dum&command2=getEmailList&searchName="+self.name+"&searchBirth="+self.birthDate+"&memberSeq="+memberSequence
        
    def setEmailWritingPeriod(self, emailWritingPeriod):
        self.emailWritingPeriod = emailWritingPeriod