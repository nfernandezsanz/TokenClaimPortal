from   flask              import render_template, request, abort, redirect, session,Blueprint
from   rpsfront           import db
from   rpsfront.models    import User,sesion
from   rpsfront.utilities import getWallet,getSystemStatus,getUUID
from   zenora             import APIClient
from   uuid               import uuid4
import rpsfront.globals   as gl
import rpsfront.secret    as secret

logger = Blueprint('logger', __name__)

#Discord API
client = APIClient(secret.ds_token, client_secret=secret.ds_secret)

@logger.route("/")
@logger.route("/home")
def home():
    wallet = getWallet()
    #print(wallet)
    #Tengo que pedir wallet
    if(not wallet):
        #log.print_("Solicito Wallet!")
        return render_template("index.html",  wallet = 0, wallet_disp = 0 )
    else:
        #log.print_("Tengo wallet! Redirecciono!")
        return redirect("/auth/" + wallet)

@logger.route("/auth/<wallet>")
def authWallet(wallet):
    #print("Recibo la wallet ==> ", wallet)

    session["wallet"] = wallet

    return redirect("/sesiontoken")

@logger.route("/sesiontoken")
def sessionToken():
    wallet = getWallet()
    #uuid   = getUUID()

    if(not wallet):
        abort(403)
    else:
        system      = getSystemStatus()
        if(not system.login):
            return render_template("notservice.html", error = "entire",  wallet=wallet, wallet_disp=gl.walletDisp(wallet))

        try:
            query       = sesion.query.filter_by(wallet=wallet).first()
            usr_info    = User.query.filter_by(wallet=wallet).first()
        except:
            return render_template("error.html", wallet=wallet, wallet_disp=gl.walletDisp(wallet))

        #Levanto el nivel de acceso
        level = gl.habilitarPaso(usr_info, system)

        if(level < 1):
            #print("El usuario no tiene acceso!")
            return render_template("out.html", wallet=wallet, wallet_disp=gl.walletDisp(wallet))
        else:
            #print("El usuario tiene acceso ==> nivel ", level)
            session["level"]   = level  

        if(not query):
            try:
                uuid = str(uuid4())
                session["uuid"]   = uuid
                new = sesion(wallet = wallet, uuid = uuid)
                db.session.add(new)
                db.session.commit()
            except:
                return render_template("error.html", wallet=wallet, wallet_disp=gl.walletDisp(wallet))

        else:
            #print("Ya tenias sesion...")
            session["uuid"]   = query.uuid
    
    return redirect("/oauth")

@logger.route("/loginDiscord")
def login():
    uuid   = getUUID()
    if(not uuid):
        abort(403)
    return redirect(secret.ds_oauth)

@logger.route("/skipDiscord")
def skipDiscord():
    uuid   = getUUID()
    if(not uuid):
        abort(403)

    session["discordSkip"] = 1
    return redirect("/oauth")

@logger.route("/logout")
def logout():
    session.clear()
    return redirect("/home")

@logger.route("/oauth/callback")
def oauth_callback():

    uuid   = getUUID()
    wallet = getWallet()

    if(not uuid or not wallet):
        abort(403)

    code = request.args["code"]

    access_token = client.oauth.get_access_token(
        code, redirect_uri=secret.ds_redirect
    ).access_token

    try:
        usr = User.query.filter_by(wallet=wallet).first() 
        usr.DiscordToken = access_token
        db.session.commit()
    except:
        return render_template("error.html", wallet=wallet, wallet_disp=gl.walletDisp(wallet))

    return redirect("/oauth")