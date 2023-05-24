from flask import Flask, render_template, flash, redirect, url_for
from flask import request
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))



app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dados.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']= "PALAVRA-SECRETA"
db = SQLAlchemy(app)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tarefa = db.Column(db.String(length=80), nullable=False)
    conteudo = db.Column(db.String(length=200), nullable=False)
    prioridade = db.Column(db.String(length=50), nullable=False)

    def __init__(self, tarefa, conteudo, prioridade):
        self.tarefa = tarefa
        self.conteudo = conteudo
        self.prioridade = prioridade

@app.route('/home', methods=['GET', 'POST'])
def Home():
    if request.method=='GET':
        return render_template('index.html')
    if request.method=='POST':
        tarefa = request.form.get('tarefa')
        conteudo = request.form.get('conteudo')
        prioridade = request.form.get('prioridade')
        t = Tasks(tarefa, conteudo, prioridade) 
        db.session.add(t)
        db.session.commit()
        flash("Dados Recebidos!")
        return redirect("/")

@app.route('/delete/<int:id>')
def delete(id):
    tarefa_delete = Tasks.query.get_or_404(id)
    try:
        db.session.delete(tarefa_delete)
        db.session.commit()
        flash("Atividade Removida com Sucesso!")
        return redirect("/")
    except:
        flash("Atividade Não Deletada")
        return redirect("/")

@app.route('/alta')   
def Alta():
    Ativ = Tasks.query.all()
    return render_template('alta.html', Ativ=Ativ) 

@app.route('/media')   
def Media():
    Ativ = Tasks.query.all()
    return render_template('media.html', Ativ=Ativ) 

@app.route('/baixa')   
def Baixa():
    Ativ = Tasks.query.all()
    return render_template('baixa.html', Ativ=Ativ) 

@app.route('/teste')
def teste():
    return print("Funcionando.....")

@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')         
def cadastro():
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True, extra_files=['./templates/', './static/'])    