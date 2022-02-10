import rpsfront.blockchain as bq

class EmptyUser():
    nombre       = "RPSUser"
    username     = "none"
    avatar_url   = "none"

emptyUsr = EmptyUser()

class client():
    wallet       = "none"
    wallet_disp  = "none"
    discordToken = "none"
    key          = ""
    skip         = 0
    token        = 0
    nft          = 0
    level        = 0
    name         = "RPSUser"

    def __init__(self, wallet, preventa = 0, airdrop = 0, wallet_disp = "none", discordToken = "none", key = "", skip = 0, token = 0, nft = 0, level = 0, name = "RPSUser"):
        self.wallet       = wallet
        self.wallet_disp  = wallet_disp
        self.discordToken = discordToken
        self.key          = key
        self.preventa     = preventa
        self.airdrop      = airdrop
        self.skip         = skip
        self.token        = token
        self.nft          = nft
        self.level        = level
        self.name         = name
    
    def blockchain(self):
        self.token =  round(bq.CantTokens(self.wallet),2)
        self.nft   =  bq.CantNFTs(self.wallet)
    
    def __repr__(self):
        return "<Client wallet:%s discordToken:%s (%d) key:%s ==> Preventa:%d , Airdrop:%d ==> Tokens %f, NFTs %d>" % (self.wallet, self.discordToken, self.skip, self.key, self.preventa, self.airdrop, self.token, self.nft)

def validaParametroStr(parametro):
    if(not parametro or str(parametro).lower() == "none"):
        parametro = ""
    return parametro

def validaParametroFloat(parametro):
    if(not parametro or str(parametro).lower() == "none"):
        parametro = 0.0
    return parametro

def validaParametroInt(parametro):
    if(not parametro or str(parametro).lower() == "none"):
        parametro = 0
    return parametro

def walletDisp(wallet):
    return wallet[0:4] + "..." + wallet[38:]

def habilitarPaso(usr, system):
    if(usr == "none" or not usr):
        return -1
    elif(usr.preventa > 0 and usr.airdrop > 0):
        return 3
    elif(usr.preventa > 0 and system.preventa == True):
        return 1
    elif(usr.airdrop > 0  and system.airdrop  == True):
        return 2
    else:
        return 0