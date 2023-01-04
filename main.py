""""A intenção do código é criar um site de classificação de livros, onde a pessoa poste o livro e
 a sua classificação. É um site para ensinar a utilizar DATABASE"""

"""importada os módulos do Flaks que irão ser utilizados, render_template para lidar com o código html,
request para requerer informações, redirect e url for para redirecionar a rota automaticamente"""
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
"""a sintaxe básica de inicialização do Flask"""
app = Flask(__name__)
"""aqui a sintaxe básica de criação do SQLAlchemy,  configuração que já traz uma classe Model que
é uma classe declarativa...sabe Deus para q..."""

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db.init_app(app)

"""essa linha é opcional, mas silencia o deprecation warning no console"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

"""abaixo a sintaxe para a criação da tabela. Book é o nome da tabela,
 id INTEGER PRIMARY KEY é uma informação única que vai identificar aquele objeto
 para os demais campos db.string aceita uma string de até 250 caracteres
  unique significa que não podem ter dois títulos iguais na tabela
   nullable signifca que não pode ser deixado em branco
    db.Float só aceita float numbers"""


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


"""para criar a inicial database, acima se importa o db e abaixo se usa essas linhas. No código da Angela
só tem a segunda linha, mas não funcionou sem a primeira, que está na documentação"""
with app.app_context():
    db.create_all()

# new_book = Book(id=1, title="Harry", author="JKKK", rating=4.5)
# db.session.add(new_book)
# db.session.commit()

"""criado um dicionário vazio que irá guardar as informações inseridas"""
all_books = []

"""aqui a rota principal levando a página inicial que trabalha com o index.html.
 A variável all_books recebe todas as informações inseridas da db através da rota /add.
 Reparar na sintaxe para obter/buscar (query) as informação no db"""


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


"""aqui a rota para adicionar livros. A lógica é que se for requisitado o método post, ou seja, se o usuário postar
 alguma informação através do botão do tipo submit, então a variável new_book vai receber as 3 informações abaixo.
Reparar que title: (é o nome do campo que será criado), request.form é a sintaxe para
obter a informação do formulário e ["title"] é o nome do input no html e então a variável new_book será
adicionada ao banco de dados (db) e a rota será redirecionada para a rota principal (home) quando o botão for pressionado.
 Do contrário, o return mantém a rota /add. Reparar na importância da identação correta"""


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

"""aqui uma rota para a edição da nota de ranking do livro, usando o redirect e o url for, e
o id do livro como seu identificador para fins de sua edição"""
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        #UPDATE RECORD
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit_rating.html", book=book_selected)

"""aqui uma rota para deletar o livro através do seu id, o código trabalha junto com o código
 
 <a href="{{ url_for('delete', id=book.id) }}">Delete</a>
 
 que está no index.html, ou seja, não foi criado um html só para essa rota.
 Depois de deletado, volta para a home page"""
@app.route("/delete")
def delete():
    book_id = request.args.get('id')

    # DELETE A RECORD BY ID
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


"""aqui o código para o sistema rodar e gerar o link do site, já com o debug como true para atualizar automaticamente"""

if __name__ == "__main__":
    app.run(debug=True)
