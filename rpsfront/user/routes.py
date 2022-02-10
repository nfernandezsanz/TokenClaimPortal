from   flask                import render_template, abort,Blueprint
from   rpsfront.utilities   import getsessioninfo,getUUID
from   rpsfront.utilities   import getSystemStatus,getUUID,getsessioninfo,prepareTX
from   rpsfront.claim.utils import prepareParams
from   zenora               import APIClient
import rpsfront.log         as log
import rpsfront.globals     as gl

user = Blueprint('user', __name__)

@user.route("/oauth")
def authDiscord():  
    uuid        = getUUID()
    usr_info    = getsessioninfo()
    usr         = usr_info[0]
    info_db     = usr_info[1]

    if(not usr.wallet or usr.key != uuid):
        abort(403)
    
    if((usr.discordToken != "none" and (len(usr.discordToken) > 5)) or usr.skip == True):
        
        #print("Discord aceptado!")

        if(usr.skip == True):
            discord_user             = gl.EmptyUser()
            #print("Skipeo Discord!")
        else:
            try:
                bearer_client        = APIClient(str(usr.discordToken), bearer=True)
                discord_user         = bearer_client.users.get_current_user()
            except:
                log.print_("Error zenora ==> Token:" + str(usr.discordToken) + " ==> Token vencido!")
                #print("Le debo pedir discord!")
                return render_template("index.html", wallet=usr.wallet, wallet_disp=usr.wallet_disp)   

        params = prepareParams(usr)

        lastTX = prepareTX()

        system = getSystemStatus()
        
        #Renderizo
        return render_template("user.html", usr = usr, preventa = params[0], airdrop = params[1], discord_user = discord_user, tx = lastTX[0], sent = lastTX[1], user_db=info_db, sys = system)

    else:
        #print("Discord rechazado!")
        return render_template("index.html", wallet=usr.wallet, wallet_disp=usr.wallet_disp) 
