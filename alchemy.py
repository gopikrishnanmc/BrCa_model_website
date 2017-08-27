from flask import Flask, render_template
from flask import request
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://db_test:111222@localhost/ok_brca_validation'
app.debug = True
db = SQLAlchemy(app)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(50))
    year_of_birth = db.Column(db.String(50))
    relative = db.relationship('Relative', backref='relative', lazy='dynamic')


class Relative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    relative_name = db.Column(db.String(50))
    type_of_relative_affected = db.Column(db.String(20))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))


@app.route('/')
def index():
    return render_template('add_user.html')


@app.route('/post_user/', methods=['POST'])
def post_user():
    user = Patient(request.form['patient_name'], request.form['year_of_birth'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()

