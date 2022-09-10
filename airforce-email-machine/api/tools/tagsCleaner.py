class InformationCleaner:
    def __init__(self, information):
        self.information = str(information)
    def clean(self):
        string = self.information
        string = string.replace(":", "")
        string = string.replace(" ", "")
        string = string.replace("\n", "")
        string = string.replace("\t", "")
        string = string.replace("<dd>", "")
        string = string.replace("</dd>", "")
        string = string.replace("\r", " ")
        string = string.strip()
        return string
    
class EmailWritingPeriodCleaner:
    def __init__(self, emailWritingPeriod):
        self.emailWritingPeriod = str(emailWritingPeriod)
    def clean(self):
        string = self.emailWritingPeriod
        string = string.replace("<dd>", "")
        string = string.replace("</dd>", "")
        string = string.replace("\t", "")
        string = string.replace('\r', '')
        string = string.replace('\n', '')
        string = string.replace("년 ", "-")
        string = string.replace("월 ", "-")
        string = string.replace("일 ", "-")
        string = string.replace("시 ", " ")
        string = string.replace("시", "")
        string = string.strip()
        return string