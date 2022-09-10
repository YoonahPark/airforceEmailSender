import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api.models.models import Sender, Email, Airman
from api.crawler import AirmanCrawler
from api.sender import EmailSender

airman = Airman("이름", "생일")
sender = Sender("이름", "주소", "상세주소")
email = Email("관계", "제목", "내용", "생일")

with open("local/userinputs/airmanInformations.txt", 'rt', encoding='UTF8') as f:
    airmanInformations = f.readlines()
    airman.name = airmanInformations[0].strip('\n')
    airman.birthDate = airmanInformations[1].strip('\n')

with open("local/userInputs/userInformations.txt", 'rt', encoding='UTF8') as f:
    userInformations = f.readlines()
    sender.name = userInformations[0].strip('\n')
    sender.address = userInformations[1].strip('\n')
    sender.addressDetail = userInformations[2].strip('\n')
    
with open("local/userInputs/email/contents.txt", 'rt', encoding='UTF8') as f:
    email.contents = f.read()
    wordCount = len(email.contents)
    if(wordCount>=1200):
        raise Exception("글자 수가 총 "+str(wordCount)+"입니다. 1200자 이상으로는 편지를 보낼 수 없습니다.")
    
with open("local/userInputs/email/emailInformations", 'rt', encoding='UTF8') as f:
    emailInformations = f.readlines()
    email.relationship = emailInformations[0].strip('\n')
    email.title = emailInformations[1].strip('\n')
    email.password = emailInformations[2].strip('\n')

airmanCrawler = AirmanCrawler(airman)
airmans = airmanCrawler.getList()
airman = airmanCrawler.selectAirman(0)
success = EmailSender(airman).send(sender, email)
print(success)