from selenium import webdriver
from selenium.webdriver.common.by import By
class _DriverAction:
    def __init__(self, driver):
        self.driver = driver
        
    def click(self, by, value):
        element = self.driver.find_element(by, value)
        element.click()
        
    def send_keys(self, by, value, keys):
        element = self.driver.find_element(by, value)
        element.send_keys(keys)

class _EmailSender(_DriverAction):
    def send(self, sender, email):
        self.sender = sender
        self.email = email
        self.__clickSendEmail()
        self.__setAddress()
        self.__writeEmail()
        self.__submitEmail()
        return self.__verifySubmissionSuccess()
    
    def __clickSendEmail(self):
        self.click(By.CSS_SELECTOR, "input[value='인터넷 편지쓰기']")
        nextUrl = "https://www.airforce.mil.kr/user/indexSub.action?codyMenuSeq=156893223&siteId=last2&menuUIType=top&dum=dum&command2=writeEmail&searchCate=&searchVal=&page=1"
        if not self.driver.current_url.startswith(nextUrl):
            raise Exception("페이지 전환이 정상적으로 이루어지지 않았습니다.")
    
    def __setAddress(self):
        self.driver.execute_script('document.getElementById("senderZipcode").removeAttribute("readonly")')
        self.driver.execute_script('document.getElementById("senderAddr1").removeAttribute("readonly")')
        self.send_keys(By.ID, "senderZipcode", self.sender.zipCode)
        self.send_keys(By.ID, "senderAddr1", self.sender.address)
        self.send_keys(By.ID, "senderAddr2", self.sender.addressDetail)
        
    def __writeEmail(self):
        self.send_keys(By.ID, "senderName", self.sender.name)
        self.send_keys(By.ID, "relationship", self.email.relationship)
        self.send_keys(By.ID, "title", self.email.title)
        self.send_keys(By.ID, "contents", self.email.contents)
        self.send_keys(By.ID, "password", self.email.password)
        
    def __submitEmail(self):
        self.click(By.CSS_SELECTOR, "input[value='작성완료']")
        nextUrl = "https://www.airforce.mil.kr/user/indexSub.action?codyMenuSeq=156893223&siteId=last2&menuUIType=top&dum=dum&command2=saveEmailResult"
        if not self.driver.current_url.startswith(nextUrl):
            raise Exception("페이지 전환이 정상적으로 이루어지지 않았습니다.")
        
    def __verifySubmissionSuccess(self):
        message = self.driver.find_element(By.CSS_SELECTOR, "div[class='message']").text
        return message=="정상적으로 등록되었습니다."
    
def send(airman, sender, email, local=False):
    url = airman.url
    driver = None
    desired_capabilities = { "acceptInsecureCerts": True }
    options = webdriver.ChromeOptions()
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-errors")
    options.add_argument("--unsafely-treat-insecure-origin-as-secure")
    if(local):
        driver = webdriver.Chrome(executable_path="api/applications/chromedriver.exe", chrome_options=options)
    else:
        options.add_argument('--headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("--no-sandbox")
        options.add_argument(f'--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path="/usr/src/chrome/chromedriver", chrome_options=options, desired_capabilities=desired_capabilities)
    driver.get(url)
    
    success = _EmailSender(driver).send(sender, email)
    return {"success" : success, "url" : url, "password" : email.password}