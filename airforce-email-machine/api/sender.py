from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class _DriverAction:
    def __init__(self, driver):
        self.driver = driver
        
    def click(self, by, value):
        element = self.driver.find_element(by, value)
        element.click()
        
    def send_keys(self, by, value, keys):
        element = self.driver.find_element(by, value)
        element.send_keys(keys)
    
class _InitialWindowSetter(_DriverAction):
    def set(self):
        self.click(By.CSS_SELECTOR, "input[value='인터넷 편지쓰기']")
        self.click(By.CSS_SELECTOR, "input[value='우편번호 검색']")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.click(By.CSS_SELECTOR, "button[id='proceed-button']")

class _AddressSetter(_DriverAction):
    def set(self, sender):
        self.sender = sender
        self.__searchAddress()
        self.__selectAddress()
        self.__writeAddressDetail()
        self.__submitAddress()
        
    def __searchAddress(self):
        self.click(By.ID, "ckHstryYn")
        self.send_keys(By.ID, "keyword", self.sender.address)
        self.click(By.CSS_SELECTOR, "input[title='검색']")
        
    def __selectAddress(self): 
        self.click(By.ID, "roadAddrTd1")
        
    def __writeAddressDetail(self): 
        self.send_keys(By.NAME, "rtAddrDetail", self.sender.addressDetail)
        
    def __submitAddress(self):
        self.click(By.CSS_SELECTOR, "a[href='javascript:setParent();']")
        self.driver.switch_to.window(self.driver.window_handles[0])

class _EmailSender(_DriverAction):
    def send(self, sender, email):
        self.sender = sender
        self.email = email
        self.__writeEmail()
        self.__submitEmail()
        return self.__verifySubmissionSuccess()
        
    def __writeEmail(self):
        self.send_keys(By.ID, "senderName", self.sender.name)
        self.send_keys(By.ID, "relationship", self.email.relationship)
        self.send_keys(By.ID, "title", self.email.title)
        self.send_keys(By.ID, "contents", self.email.contents)
        self.send_keys(By.ID, "password", self.email.password)
        
    def __submitEmail(self):
        self.click(By.CSS_SELECTOR, "input[value='작성완료']")
        
    def __verifySubmissionSuccess(self):
        message = self.driver.find_element(By.CSS_SELECTOR, "div[class='message']").text
        return message=="정상적으로 등록되었습니다."
    
class EmailSender:
    def __init__(self, airman):
        self.name = airman.name
        self.birthDate = airman.birthDate
        self.memberSequence = airman.memberSequence
        self.__createDriver()
    
    def __createDriver(self):
        url = "https://www.airforce.mil.kr/user/indexSub.action?codyMenuSeq=156893223&siteId=last2&menuUIType=top&dum=dum&command2=getEmailList&searchName="+self.name+"&searchBirth="+self.birthDate+"&memberSeq="+self.memberSequence
        self.driver = webdriver.Edge(r"applications/msedgedriver.exe")
        self.driver.get(url)
        
    def send(self, sender, email):
        _InitialWindowSetter(self.driver).set()
        _AddressSetter(self.driver).set(sender)
        success = _EmailSender(self.driver).send(sender, email)
        return success
    
    
        