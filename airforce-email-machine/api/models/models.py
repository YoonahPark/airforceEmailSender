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
        
    def setEmailWritingPeriod(self, emailWritingPeriod):
        self.emailWritingPeriod = emailWritingPeriod
        
    def __str__(self):
        informationString = "name : "+self.name+"\n"
        informationString += "birthDate : "+self.birthDate+"\n"
        informationString += "division : "+self.division+"\n"
        informationString += "enlisted at : "+self.enlistedAt+"\n"
        informationString += "discharged at : "+self.dischargedAt+"\n"
        informationString += "memberSequence : "+self.memberSequence+"\n\n"
        return informationString