import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base


db = SQLAlchemy()
Base = declarative_base()


def verifica_variaveis_ambiente():
    res = []
    chaves = ["MYSQL_USERNAME", "MYSQL_PASSWORD", "MYSQL_ADDRESS", "MYSQL_DBNAME"]

    for chave in chaves:
        valor = os.environ.get(chave)

        if valor is None:
            print("Faltou a variável de ambiente", chave)
            exit(1)

        res.append(valor)
    return res


class Usuario(Base):
    __tablename__ = "atividade02"

    id = Column(Integer, primary_key=True)
    FirstName = Column(String)
    LastName = Column(String)
    Age = Column(Integer)
    Height = Column(Float)

    def __str__(self) -> str:
        return f"{self.FirstName} {self.LastName}, {self.Age}, {self.Height}"


def create_app(test_config=None):
    app = Flask(__name__)

    username, password, server, dbname = verifica_variaveis_ambiente()
    userpass = f"mysql+pymysql://{username}:{password}@"

    app.config["SQLALCHEMY_DATABASE_URI"] = userpass + server + "/" + dbname
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    print(app.config["SQLALCHEMY_DATABASE_URI"])
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    @app.route("/")
    def testdb():
        try:
            a = db.session.query(Usuario).all()
            b = "<h1>Funciona!</h1>"

            for line in a:
                b += f"<h2>{line}</h2>"
            return b

        except Exception as e:
            error_text = "<h2>The error:<br>" + str(e) + "</h2>"
            hed = "<h1>Something is broken.</h1>"
            return hed + error_text

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=8200)
