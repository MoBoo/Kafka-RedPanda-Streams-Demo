# Kafka-RedPanda-Streams-Demo
Demo application using either [Kafka](https://kafka.apache.org/) or [Redpanda](https://redpanda.com/) and Python.
Application mocks a QnA-Forum where you can ask questions or submit answers. 
Upon answer submission the asking user is notified via Email (mocked via SMTP4DEV) about the new answer. 
This is done via Change-Data-Capture with Kafka and Kafka Connect and Debezium.

## Architecture Overview
![Overview Diagramm](docs/overview.png)

## Example Images
### Submitting a question
![Submit Question](docs/question.png)
### Submit an answer
![Submit Answer](docs/answer.png)
### Get Notified
![Get Notified](docs/mail.png)

## Usage
`start.sh redpanda|kafka`
