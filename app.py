from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://marceh:prueba1234@marceh.mysql.pythonanywhere-services.com/marceh$bycicleride'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino las tablas
class Bycicle(db.Model):   # la clase Producto hereda de db.Model
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    descripcion=db.Column(db.String(45))
    rodado=db.Column(db.String(45))
    tipo=db.Column(db.String(45))
    grupoEtario=db.Column(db.String(45))
    genero=db.Column(db.String(45))
    suspension=db.Column(db.String(45))
    frenos=db.Column(db.String(45))
    velocidad=db.Column(db.String(45))
    foto=db.Column(db.String(255))
    def __init__(self,descripcion,rodado,tipo,grupoEtario,genero,suspension,frenos,velocidad,foto):   #crea el  constructor de la clase
        self.descripcion=descripcion  # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.rodado=rodado
        self.tipo=tipo
        self.grupoEtario=grupoEtario
        self.genero=genero
        self.suspension=suspension
        self.frenos=frenos
        self.velocidad=velocidad
        self.foto=foto




    #  si hay que crear mas tablas , se hace aqui




with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class BycicleSchema(ma.Schema):
    class Meta:
             fields=('id','descripcion','rodado','tipo','grupoEtario','genero','suspension','frenos','velocidad','foto')




bycicle_schema=BycicleSchema()            # El objeto producto_schema es para traer un producto
bycicles_schema=BycicleSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto




# crea los endpoint o rutas (json)
@app.route('/bycicle',methods=['GET'])
def get_Bycicles():
    all_bycicles=Bycicle.query.all()         # el metodo query.all() lo hereda de db.Model
    result=bycicles_schema.dump(all_bycicles)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla




@app.route('/bycicle/<id>',methods=['GET'])
def get_bycicle(id):
    bycicle=Bycicle.query.get(id)
    return bycicle_schema.jsonify(bycicle)   # retorna el JSON de un producto recibido como parametro



@app.route('/bycicle/<id>',methods=['DELETE'])
def delete_bycicle(id):
    bycicle=Bycicle.query.get(id)
    db.session.delete(bycicle)
    db.session.commit()                     # confirma el delete
    return bycicle_schema.jsonify(bycicle) # me devuelve un json con el registro eliminado


@app.route('/bycicle', methods=['POST']) # crea ruta o endpoint
def create_bycicle():
    #print(request.json)  # request.json contiene el json que envio el cliente
    descripcion=request.json['descripcion']
    rodado=request.json['rodado']
    tipo=request.json['tipo']
    grupoEtario=request.json['grupoEtario']
    genero=request.json['genero']
    suspension=request.json['suspension']
    frenos=request.json['frenos']
    velocidad=request.json['velocidad']
    foto=request.json['foto']

    new_bycicle=Bycicle(descripcion,rodado,tipo,grupoEtario,genero,suspension,frenos,velocidad,foto)
    db.session.add(new_bycicle)
    db.session.commit() # confirma el alta
    return bycicle_schema.jsonify(new_bycicle)


@app.route('/bycicle/<id>' ,methods=['PUT'])
def update_bycicle(id):
    bycicle=Bycicle.query.get(id)
    bycicle.descripcion=request.json['descripcion']
    bycicle.rodado=request.json['rodado']
    bycicle.tipo=request.json['tipo']
    bycicle.grupoEtario=request.json['grupoEtario']
    bycicle.genero=request.json['genero']
    bycicle.suspension=request.json['suspension']
    bycicle.frenos=request.json['frenos']
    bycicle.velocidad=request.json['velocidad']
    bycicle.foto=request.json['foto']

    db.session.commit()    # confirma el cambio
    return bycicle_schema.jsonify(bycicle)    # y retorna un json con el producto

@app.route('/')
def hello_world():
    return 'Hello from Flask!'
