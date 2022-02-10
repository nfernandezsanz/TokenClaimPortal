import rpsfront.globals as gl
from   rpsfront.models  import info_preventa,info_airdrop
import rpsfront.log     as log

class preventa():
    enviado       = 0
    unlocked      = 0
    total         = 0
    disponible    = 0
    porUnlocked   = 100
    porClaimeado  = 100

    def __init__(self,  enviado = 0, unlocked = 0, total = 0, disponible = 0, porUnlocked = 100, porClaimeado = 100):
        self.enviado         = enviado
        self.unlocked        = unlocked
        self.total           = total
        self.disponible      = disponible
        self.porUnlocked     = porUnlocked
        self.porClaimeado    = porClaimeado


    def calcular(self):
        if(self.unlocked != 0):
            self.porClaimeado  = round((self.enviado  / self.unlocked)*100 , 1)
        else:
            self.porClaimeado  = 0
        self.porUnlocked   = round((self.unlocked / self.total)   *100 , 1)
        if((self.unlocked - self.enviado) <= 1):
            self.disponible = 0
        else:
            self.disponible    = round(self.unlocked  - self.enviado, 1)

    def cargar(self, wallet):
        try:
            query = info_preventa.query.filter_by(wallet=wallet).first()
        except:
            query = info_preventa()

        if(not query):
            log.print_("ERROR ==> Wallet: " + str(wallet) + " no dispone de datos de preventa o hubo error en db!")
            return info_preventa()

        self.enviado    = gl.validaParametroFloat(query.enviado)
        self.unlocked   = gl.validaParametroFloat(query.unlocked)
        self.total      = max([gl.validaParametroFloat(query.total),1])

        self.calcular()

        return 1

class airdrop():
    enviadoRPS       = 0
    unlockedRPS      = 0
    unlockedUSD      = 0
    totalUSD         = 0
    disponible       = 0
    porUnlocked      = 100
    porClaimeado     = 100


    def __init__(self,  enviadoRPS = 0, unlockedRPS = 0, unlockedUSD = 0, totalUSD = 0, porUnlocked = 100, porClaimeado = 100, disponible = 0):
        self.enviadoRPS      = enviadoRPS
        self.unlockedRPS     = unlockedRPS
        self.unlockedUSD     = unlockedUSD
        self.totalUSD        = totalUSD
        self.porUnlocked     = porUnlocked
        self.porClaimeado    = porClaimeado
        self.disponible      = disponible

    def calcular(self):
        if(self.unlockedRPS != 0):
            self.porClaimeado  = round((self.enviadoRPS  / self.unlockedRPS)*100 , 1)
        else:
            self.porClaimeado  = 0
        self.porUnlocked   = round((self.unlockedUSD / self.totalUSD)   *100 , 1)
        self.disponible    = max([(self.unlockedRPS  - self.enviadoRPS), 0])

    def cargar(self, wallet):
        try:
            query = info_airdrop.query.filter_by(wallet=wallet).first()
        except:
            query = info_airdrop()

        if(not query):
            log.print_("ERROR ==> Wallet: " + str(wallet) + " no dispone de datos de airdrop o hubo error en la db!")
            return info_airdrop()
            
        self.enviadoRPS    = gl.validaParametroFloat(query.enviadoRPS)
        self.unlockedRPS   = gl.validaParametroFloat(query.unlockedRPS)
        self.unlockedUSD   = gl.validaParametroFloat(query.unlockedUSD)
        self.totalUSD      = max([gl.validaParametroFloat(query.totalUSD),1])

        self.calcular()

        return 1

