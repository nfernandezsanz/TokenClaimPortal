from   rpsfront.claim.claims  import preventa,airdrop
from   flask                  import session

def prepareParams(usr):

    #Cargo datos de blockchain si no skipeo la parte de discord..
    if(usr.skip == False):
        usr.blockchain()
        pass
    
    pr  = preventa()
    air = airdrop()
    
    if(usr.level == 1 or usr.level == 3):
        #print("Calculo preventa")
        #Calculo preventa
        pr.cargar(usr.wallet)

    if(usr.level == 2 or usr.level == 3):
        #print("Calculo airdrop")
        air.cargar(usr.wallet)
    
    if(pr.disponible > 0 or air.disponible > 0):
        session["code_"]   = "body{font-size: 14px;}"
     
    return (pr,air)