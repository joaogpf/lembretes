from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime

# Inicializando o App Flask
app = Flask(__name__)
api = Api(app)

# Configurando o banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Criando o modelo do banco de dados
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    notificacao = db.Column(db.DateTime, nullable=False)

# Criando a estrutura do banco de dados
with app.app_context():
    db.create_all()

# Criando uma API Resource
class TarefasResource(Resource):
    def get(self):
        tarefas = Tarefa.query.all()
        return jsonify([{"id": t.id, "titulo": t.titulo, "descricao": t.descricao, "notificacao": t.notificacao} for t in tarefas])

    def post(self):
        dados = request.get_json()
        nova_tarefa = Tarefa(titulo=dados["titulo"], descricao=dados.get("descricao", ""), notificacao = datetime.fromisoformat(dados["notificacao"]))
        db.session.add(nova_tarefa)
        db.session.commit()
        return jsonify({"mensagem": "Tarefa adicionada com sucesso!"})

class TarefaResource(Resource):
    def get(self, id):
        tarefa = Tarefa.query.get(id)
        if tarefa:
            return jsonify({"id": tarefa.id, "titulo": tarefa.titulo, "descricao": tarefa.descricao, "notificacao": tarefa.notificacao})
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    def delete(self, id):
        tarefa = Tarefa.query.get(id)
        if tarefa:
            db.session.delete(tarefa)
            db.session.commit()
            return jsonify({"mensagem": "Tarefa deletada com sucesso!"})
        return jsonify({"erro": "Tarefa não encontrada"}), 404

# Adicionando recursos à API
api.add_resource(TarefasResource, "/tarefas")
api.add_resource(TarefaResource, "/tarefas/<int:id>")

# Rodar o servidor
if __name__ == "__main__":
    app.run(debug=True)
