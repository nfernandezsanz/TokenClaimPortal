import os
import datetime
import time
import logging as log

LOGLEVEL = 2

path   = './logs/'

def removeOldFiles():
    
    now = time.time()

    for filename in os.listdir(path):
        filestamp = os.stat(os.path.join(path, filename)).st_mtime
        filecompare = now - 7 * 86400
        if  filestamp < filecompare:
            os.remove(os.path.join(path, filename))


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
fn     = yesterday.strftime("%B-%d-%Y") + "%" + str(os.getpid()) + "%.log"

if not os.path.exists(path):
    os.makedirs(path)

removeOldFiles()
    
#Configuro el log file
log.basicConfig( level=log.DEBUG, filename= path+fn, format='%(process)d-%(levelname)s-%(message)s')

log.info("$$####################SISTEMA EJECUTADO " + str(datetime.datetime.now()) + "####################$$")

def print_(contenido, logL = LOGLEVEL):
    if(not logL):
        log.info(contenido)
    else:
        print(contenido)
        if(logL > 1):
            log.info(contenido)