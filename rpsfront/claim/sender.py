from   rpsfront        import db
from   web3            import Web3
from   rpsfront.models import taskSender,transactions,info_preventa
from   sqlalchemy      import or_
import rpsfront.BSConf as BSConf
import rpsfront.log    as log
import threading
import json

class SendThread(threading.Thread):
    def __init__(self, args=()):
        self.args     = args
        self.destino  = args[0]
        self.origen   = args[1]
        self.cant     = args[2] 
        self.debug    = args[3]
        self.uuid     = args[4]
        self.retry    = 3
        self.contract = Web3.toChecksumAddress(BSConf.contract)
        self.progress = 0
        self.desc     = taskSender(id = self.uuid , destino = self.destino, origen = self.origen, cantidad = self.cant)
        super().__init__()
    
    def connectBSC(self):
        try:
            bsc  = BSConf.RPCURL
            web3 = Web3(Web3.HTTPProvider(bsc))
        except:
            web3 = False
        return web3 

    def aptoInicio(self):
        try:
            query = db.session.query(taskSender).filter(or_(taskSender.id == self.uuid, taskSender.destino == self.destino), taskSender.checked == 0, taskSender.error == 0).first()
        except:
            return 0
            
        if(not query):
            return 1
        else:
            return 0

    def updateProgress(self, cant):
        try:
            self.progress += cant
            if(self.debug == True):
                self.desc.progreso = self.progress
                db.session.commit()
        except:
            pass
            #print("Progreso PID:",  threading.get_ident(), "==> Wallet:" , self.destino , "==>" , self.progress , "%")

    def run(self):
        #if(self.debug == True):
            #print("Iniciando envio de tokens ==> Argumentos  " + str(self.args))
            #pass
        
        #Chequeo estar en regla y no repetir transaccion en proceso
        if(not self.aptoInicio()):
            log.print_("Solicitud de inicio de transferencia prohibida!" + str(self.wallet))
            self.updateProgress(-1)
            return

        self.updateProgress(5)


        try:
            db.session.add(self.desc)
            db.session.commit()
        except:
            try:
                self.updateProgress(-1000)
            except:
                log.print_("ERROR! ==> No puedo dejar registro de la transferencia en la db! Cancelada!")

        #Conectando a la red
        retry = self.retry
        web3  = self.connectBSC()

        while(not web3.isConnected() and retry > 0):
            web3 = self.connectBSC()
            retry -= 1
        
        if(not web3.isConnected()):
            log.print_("Error de red! Transaccion " + str(self.uuid) + " cancelada!")
            self.desc.error = True
            try:
                db.session.commit()
                self.updateProgress(-2)
            except:
                log.print_("ERROR! ==> No puedo dejar registro de la transferencia en la db! Cancelada!")
            return 
        
        self.updateProgress(10)

        #print("Estoy conectado!")
        contract_address = self.contract
        abi              = json.loads(BSConf.abi)
        contract         = web3.eth.contract(address=contract_address, abi=abi)
        #balanceOf        = contract.functions.balanceOf(self.origen).call()
        self.updateProgress(5)
        amount           = web3.toWei(self.cant, 'ether')
        nonce            = web3.eth.getTransactionCount(self.origen)
        self.updateProgress(5)

        token_tx = contract.functions.transfer(self.destino, amount).buildTransaction({
            'chainId':BSConf.chainID, 'gas': 90000,'gasPrice': web3.toWei('15','gwei'), 'nonce':nonce                                                      
        })

        sign_txn = web3.eth.account.signTransaction(token_tx, private_key="#PrivateKey")
    
        self.updateProgress(10)
        
        try:
            txn      = web3.eth.sendRawTransaction(sign_txn.rawTransaction)
            txn_     = txn.hex()
        except Exception as e:
            log.print_("ERROR transaccion" + str(self.uuid) + " ==> " + str(e) + " ==> Transaccion cancelada!" )
            self.desc.error = True
            db.session.commit()
            self.updateProgress(-100)
            return 

        self.updateProgress(50)

        receipt  = web3.eth.waitForTransactionReceipt(txn)
        succes   = receipt['status'] == 1

        if(succes == True):
            print("Transaccion exitosa de " + str(self.cant) + " RPS a " + str(self.destino) + " TX ==> ", txn_)
            
            try:
                info = info_preventa.query.filter_by(wallet=self.destino).first()
                info.enviado += self.cant
            except:
                log.print_("ERROR!! GRAVISIMO! No puedo dejar constancia de transfer ejecutada!" )

            self.desc.progreso = 100
            self.desc.checked  = True

            try:
                new_tx = transactions(wallet = self.destino, TX = txn_, id = self.uuid, ammount= self.cant, result=succes)
                db.session.add(new_tx)
                db.session.commit()
            except:
                log.print_("ERROR!! GRAVISIMO! No puedo dejar constancia de transfer ejecutada!" )
                
            return 
        else:
            log.print_("ERROR! TX ==> " + txn_)
            try:
                self.desc.error = True
                db.session.commit()
                self.updateProgress(-101)
            except:
                log.print_("ERROR reportando el error en la transaccion" + str(self.uuid) + " ==> Transaccion cancelada!" )
            return