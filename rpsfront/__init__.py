from   flask               import Flask
from   flask_cors          import CORS
from   flask_sqlalchemy    import SQLAlchemy
import rpsfront.secret     as secret

#Flask Server
app = Flask(__name__)
#Cors Security
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']        = 'mysql+pymysql://' + secret.db_usr + ":" + secret.db_psk + "@" + secret.db_ip + '/RPS-DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"]                     = secret.secret_key

#DataBase
db = SQLAlchemy(app)


from rpsfront.login.routes  import logger
from rpsfront.user.routes   import user
from rpsfront.claim.routes  import claim

app.register_blueprint(logger)
app.register_blueprint(user)
app.register_blueprint(claim)