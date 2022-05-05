from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

FlaskMaster = Flask(__name__)
FlaskMaster.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FlaskMasterData.db'
db = SQLAlchemy(FlaskMaster)

class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@FlaskMaster.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        task = TaskList(content=content)

        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Could Not Add Task'
    else:
        tasks = TaskList.query.order_by(TaskList.created).all()
        return render_template('index.html', tasks=tasks)

@FlaskMaster.route('/delete/<int:id>')
def delete(id):
    task = TaskList.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'Could Not Delete Task'

@FlaskMaster.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = TaskList.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Could Not Update Task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    FlaskMaster.run(debug=True)
