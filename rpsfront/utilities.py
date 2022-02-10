from   rpsfront               import db
from   rpsfront.models        import systemvars,taskSender,transactions,User,sesion
from   flask                  import session, jsonify
import rpsfront.globals       as gl
import datetime

def getWallet():
    wallet       = str(session.get("wallet"))
    wallet       = gl.validaParametroStr(wallet)
    if(not wallet):
        return ""
    return wallet

def getUUID():
    uuid         = str(session.get("uuid"))
    uuid         = gl.validaParametroStr(uuid)
    if(not uuid):
        return ""
    return uuid

def getAuthCode():
    code = str(session.get("code_"))
    if(code == "body{font-size: 14px;}"):
        return True
    else:
        return False

def getSystemStatus():

    retry = 0

    try:
        systemStatus = systemvars.query.filter_by(system="claim").first()
    except:
        systemStatus = ""

    if(not systemStatus):
        return systemvars()
    else:
        if(systemStatus.max < 0):
            systemStatus.max = 0
        if(systemStatus.fee < 0):
            systemStatus.fee = 0

    return systemStatus
            
def prepareTX():
    wallet = getWallet()
    current_time = datetime.datetime.utcnow()
    one_day_ago  = current_time - datetime.timedelta(hours=1)


    try:
        info = db.session.query(transactions).filter(transactions.wallet == wallet, transactions.timestamp > one_day_ago).first()
    except:
        return ("Error obteniendo TX!", "Error")
        
    if(not info):
        return ("",0)
    else:
        return (info.TX, info.ammount)

def getsessioninfo():
    wallet = getWallet()
    uuid   = getUUID()

    skip   = session.get("discordSkip")
    if(skip != 1):
        slip = 0

    lvl  = session.get("level")

    if(not wallet or not uuid):
        #print("Usuario sin datos!")
        return gl.client(wallet = "")
    
    try:
        usr_info    = User.query.filter_by(wallet=wallet).first()
        sesionInfo  = sesion.query.filter_by(wallet=wallet).first()
    except:
        return gl.client(wallet = "")
        
    if(sesionInfo.uuid != uuid):
        #print("Usuario no autenticado!")
        return gl.client(wallet = "")

    return (gl.client(wallet = wallet, wallet_disp=gl.walletDisp(wallet), preventa= gl.validaParametroFloat(usr_info.preventa), airdrop = gl.validaParametroFloat(usr_info.airdrop), discordToken = gl.validaParametroStr(usr_info.DiscordToken), key = gl.validaParametroStr(uuid), skip = gl.validaParametroInt(skip), level = gl.validaParametroInt(lvl)), usr_info)

def getProgress(wallet):
    task = db.session.query(taskSender).filter(taskSender.destino == wallet, taskSender.checked == False, taskSender.error == False).first()
    if(not task):
        return jsonify(progress=100)
    return jsonify(progress=task.progreso)
