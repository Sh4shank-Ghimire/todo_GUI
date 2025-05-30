from datetime import datetime
from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

@app.route("/", methods=['GET','POST'])
def func():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')

        if not title or not desc:
            return redirect("/")
        try:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
            return redirect("/")
        
        except Exception:
            db.session.rollback()

        return redirect("/")
    
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['POST', 'GET'])
def update(sno):
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')

        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc

        db.session.commit()  
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


if __name__ == "__main__":
    app.run(debug=True)