import smtplib
import json
import os
from kafka import KafkaConsumer
from email.mime.text import MIMEText
from models import Question
from sqlalchemy.orm import Session
from sqlalchemy import select, create_engine

EMAIL_FROM = "info@qna.de"
EMAIL_SUBJECT = "New Reply to Question"
EMAIL_BODY = """Hi there,<br>
<br>
someone has left an answer to your Question: <strong>{title}</strong><br>
Check it out here: <a href="http://localhost:5000/question/{question_id}">here</a><br>
<br>
- The QnA Team
"""


def prepare_email(from_email, to_email, subject, body):
    msg = MIMEText(body, "html")

    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    return msg


def fetch_question(question_id, db):
    stmt = select(Question.title, Question.email).filter_by(id=question_id)
    return db.execute(stmt).one()


smtp = smtplib.SMTP(f"{os.getenv('SMTP_HOST')}", port=int(os.getenv('SMTP_PORT')))
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
db_session = Session(engine)

consumer = KafkaConsumer("qna.public.answer", bootstrap_servers=[f"{os.getenv('BROKER_HOST')}:{os.getenv('BROKER_PORT')}"], auto_offset_reset="earliest")
for msg in consumer:
    data = json.loads(msg.value.decode())
    question_id = data.get("payload").get("after").get("question_id")
    question = fetch_question(question_id, db_session)
    mail_text = EMAIL_BODY.format(title=question.title, question_id=question_id)
    msg = prepare_email(EMAIL_FROM, question.email, EMAIL_SUBJECT, mail_text)
    smtp.sendmail(msg.get("From"), (msg.get("To"),), msg.as_string())

smtp.quit()
db_session.close()
