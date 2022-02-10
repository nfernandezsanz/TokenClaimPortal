from   rpsfront import db
import datetime

class systemvars(db.Model):
    system       = db.Column(db.String(50), primary_key=True)              
    fee          = db.Column(db.Integer ,default=0)
    airdrop      = db.Column(db.Boolean ,default=0)
    preventa     = db.Column(db.Boolean ,default=0) 
    login        = db.Column(db.Boolean ,default=0) 
    max          = db.Column(db.Integer ,default=0) 
    send         = db.Column(db.Integer ,default=0)
    ip           = db.Column(db.String(50), primary_key=True)  
    
    def __init__(self, system = "claim", fee = 1,  airdrop = 0, preventa = 1, login = 0, send = 0, max = 1, ip = "10.0.1.4"):
        self.system      = system
        self.fee         = fee
        self.airdrop     = airdrop
        self.preventa    = preventa
        self.login       = login
        self.max         = max
        self.send        = send
        self.ip          = ip        

    def __repr__(self):
        return "<System %s status ==> Login %d, Airdrop:%d , Preventa:%d, TransactionsSend:%d, IP:%s ==> Fee:%d , MaxClaim:%d>" % (self.system, self.login, self.airdrop, self.preventa, self.send, self.ip, self.fee, self.max)

class taskSender(db.Model):
    id           = db.Column(db.String(80),default="",primary_key=True)              # uuid
    destino      = db.Column(db.String(50))                                          # Wallet destino
    origen       = db.Column(db.String(50))                                          # Wallet origen
    cantidad     = db.Column(db.Float   ,default=0)                                  # Cantidad a transferir
    progreso     = db.Column(db.Integer ,default=0)                                  # Progreso
    checked      = db.Column(db.Boolean ,default=0)                                  # Fue verificada?
    error        = db.Column(db.Boolean ,default=0)                                  # Hubieron errores?
    #started      = db.Column(db.DateTime)

    def __init__(self, id, destino,  origen, cantidad, progreso = 0, check = False, error = False):
        self.id           = id
        self.destino      = destino
        self.origen       = origen
        self.cantidad     = cantidad
        self.progreso     = progreso
        self.check        = check
        self.error        = error

class transactions(db.Model):
    TX           = db.Column(db.String(100),default="",primary_key=True)                # TX
    wallet       = db.Column(db.String(50))                                             # Wallet
    timestamp    = db.Column(db.DateTime  ,default=datetime.datetime.utcnow)            # TimeStamp
    ammount      = db.Column(db.Float     ,default=0)                                   # Ammount
    id           = db.Column(db.String(80),default="")                                  # uuid       

    def __init__(self, wallet, TX, id, ammount, result):
        self.wallet        = wallet
        self.TX            = TX
        self.ammount       = ammount
        self.result        = result
        self.id            = id

class User(db.Model):
    wallet       = db.Column(db.String(50),primary_key=True)  # Wallet
    discord      = db.Column(db.String(40))                   # Usuario Discord
    telegram     = db.Column(db.String(40))                   # Usuario Telegram
    twitter      = db.Column(db.String(40))                   # Usuario Twitter
    email        = db.Column(db.String(80))                   # Email
    nombre       = db.Column(db.String(50))                   # Nombre 
    airdrop      = db.Column(db.Float ,default=0)             # Airdrop Tokens
    preventa     = db.Column(db.Float ,default=0)             # Airdrop Tokens
    auth         = db.Column(db.Integer,default=0)            # Admin o Mod
    pais         = db.Column(db.String(40))                   # Pais
    DiscordToken = db.Column(db.String(50))

    def __init__(self, wallet, discord, telegram, twitter, picture, pais = "", auth = 0, airdrop = 0, preventa = 0, email = "none", nombre = "RPSUser", DiscordToken = "none"):
        self.wallet       = wallet
        self.discord      = discord
        self.telegram     = telegram
        self.twitter      = twitter
        self.airdrop      = airdrop
        self.preventa     = preventa
        self.auth         = auth
        self.pais         = pais
        self.email        = email
        self.nombre       = nombre
        self.DiscordToken = DiscordToken

class info_preventa(db.Model):
    wallet       = db.Column(db.String(50),primary_key=True)   # Wallet
    total        = db.Column(db.Float  ,default=0)             # 
    enviado      = db.Column(db.Float  ,default=0)             # 
    diario       = db.Column(db.Float  ,default=0)             # 
    unlocked     = db.Column(db.Float  ,default=0)             # 
    Dias         = db.Column(db.Integer,default=0)             # 
    pending      = db.Column(db.Boolean)                       # 
    block        = db.Column(db.Boolean)                       # 

    def __init__(self, wallet, total, enviado, diario, unlocked, Dias = 0, pending = 0, block = 0):
        self.wallet        = wallet
        self.total         = total
        self.enviado       = enviado
        self.diario        = diario
        self.unlocked      = unlocked
        self.Dias          = Dias
        self.pending       = pending
        self.block         = block

class info_airdrop(db.Model):
    wallet       = db.Column(db.String(50),primary_key=True)        # Wallet
    totalUSD     = db.Column(db.Float ,default=0)                   # 
    diarioUSD    = db.Column(db.Float ,default=0)                   # 
    unlockedUSD  = db.Column(db.Float ,default=0)                   # 
    enviadoRPS   = db.Column(db.Float ,default=0)                   # 
    unlockedRPS  = db.Column(db.Float ,default=0)                   # 
    dias         = db.Column(db.Integer,default=0)                  # 


    def __init__(self, wallet, totalUSD, diarioUSD,unlockedUSD, dias, enviadoRPS, unlockedRPS):
        self.wallet       = wallet
        self.totalUSD     = totalUSD
        self.diarioUSD    = diarioUSD
        self.unlockedUSD  = unlockedUSD
        self.enviadoRPS   = enviadoRPS
        self.unlockedRPS  = unlockedRPS
        self.dias         = dias

class sesion(db.Model):
    wallet = db.Column(db.String(50),primary_key=True)
    uuid   = db.Column(db.String(50))

    def __init__(self, wallet, uuid):
        self.wallet = wallet
        self.uuid   = uuid

#db.create_all()