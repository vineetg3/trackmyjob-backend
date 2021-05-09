import datetime,os

def printResponse(response,status=200):
    if(os.environ['APP_SETTINGS']=="config.DevelopmentConfig"):
        print(response)
    return response,status

def convertToDate(date):
    if(date==None):
        return None
    y,m,d=date.split('-')
    return datetime.date(year=int(y),month=int(m),day=int(d))
