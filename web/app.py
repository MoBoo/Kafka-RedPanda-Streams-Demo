import os

from flask import Flask, render_template, request, redirect, url_for
from models import db

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
db.init_app(app)

from models import Question, Answer


@app.route("/", methods=("GET",))
def list_questions():
    return render_template("list_questions.html", questions=Question.query.all())


@app.route("/question", methods=("POST",))
def add_question():
    question = Question(
        title=request.form.get("title"),
        body=request.form.get("question"),
        email=request.form.get("email")
    )

    db.session.add(question)
    db.session.commit()

    return redirect(url_for("get_question", question_id=question.id))


@app.route("/question/<int:question_id>", methods=("GET",))
def get_question(question_id):
    question = Question.query.get(question_id)
    return render_template("get_question.html", question=question)


@app.route("/question/<int:question_id>/answer", methods=("POST",))
def add_answer(question_id):
    answer = Answer(
        question_id=question_id,
        body=request.form.get("answer"),
    )

    db.session.add(answer)
    db.session.commit()

    return redirect(url_for("get_question", question_id=question_id))


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
