from   flask                    import render_template,abort, Blueprint
from   rpsfront.models          import info_preventa
from   rpsfront.claim.sender    import SendThread
from   rpsfront.utilities       import getWallet,getSystemStatus,getUUID,getAuthCode,getProgress
from   uuid                     import uuid4
import rpsfront.globals         as gl
import rpsfront.BSConf          as BSConf

claim = Blueprint('claim', __name__)

@claim.route("/claimpresale")
def presale_claim():
    uuid   = getUUID()
    wallet = getWallet()
    auth   = getAuthCode()

    if(not uuid or not wallet or not auth):
        abort(403)
    
    system = getSystemStatus()

    if(not system.send):
        return render_template("notservice.html", error = "claim",  wallet=wallet, wallet_disp=gl.walletDisp(wallet))
    
    try:
        query = info_preventa.query.filter_by(wallet=wallet).first()
    except:
        return render_template("error.html", wallet=wallet, wallet_disp=gl.walletDisp(wallet))

    if(not query):
        abort(404)
    
    if(not query.block):
        cantidad = query.unlocked - query.enviado
    else:
        abort(403)
    
    if(cantidad <= 0):
        abort(404)

    t  = SendThread(args=(wallet,BSConf.wallet, cantidad, True, str(uuid4())))
    t.start()

    return render_template('sending.html', ip = system.ip, wallet = wallet)

@claim.route('/progress/<wallet>', methods = ['GET'])
def progress(wallet):
    return getProgress(wallet)

