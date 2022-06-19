#!/bin/bash

BROKER=$1

echo ">>> Starting web app..."
docker-compose -f web/docker-compose.yml up -d postgresql pgadmin
sleep 5
docker-compose -f web/docker-compose.yml up -d web_app

if [ "$BROKER" = "kafka" ]; then
  echo ">>> Starting Kafka...:"
elif [ "$BROKER" = "redpanda" ]; then
  echo ">>> Starting Redpanda..."
  docker-compose -f redpanda/docker-compose.yml up -d
  sleep 5
  echo ">>> Creating topics..."
  docker-compose -f redpanda/docker-compose.yml exec broker rpk topic create qna.public.question
  docker-compose -f redpanda/docker-compose.yml exec broker rpk topic create qna.public.answer
else
  echo $'>>> Please specify which broker to run: \n\t ./start.sh redpanda|kafka'
  echo ">>> Exiting..."
  docker-compose -f web/docker-compose.yml down -v
  exit
fi

echo ">>> Starting connect..."
docker-compose -f connect/docker-compose.yml up -d
sleep 5
echo "Creating connector config"
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d "@connect/connector.json" -o /dev/null -s

echo ">>> Starting streams app..."
docker-compose -f streams/docker-compose.yml up -d


echo ">>> Setup completed."
echo $'>>> Visit\n\thttp://localhost:5000 for webapp\n\thttp://localhost:3000 for email notifications\n\thttp://localhost:8080 for pgadmin'

read -n 1 -p "Press any key to shutdown"

docker-compose -f streams/docker-compose.yml down -v
docker-compose -f connect/docker-compose.yml down -v

if [ "$BROKER" = "kafka" ]; then
  docker-compose -f kafka/docker-compose.yml down -v
elif [ "$BROKER" = "redpanda" ]; then
  docker-compose -f redpanda/docker-compose.yml down -v
fi

docker-compose -f web/docker-compose.yml down -v

echo ">>> Bye. :)"