#!/bin/bash

docker build -t avrora_tests .

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

CONTAINER_ID=$(docker run -d -v /dev/shm:/dev/shm avrora_tests)

docker wait "$CONTAINER_ID"

docker cp "$CONTAINER_ID:/app/send_results/allure-report" "$SCRIPT_DIR/final_results"
docker cp "$CONTAINER_ID:/app/send_results/logs/test.log" "$SCRIPT_DIR/final_results"

docker stop "$CONTAINER_ID"
docker rm "$CONTAINER_ID"
docker system prune -f
docker rmi avrora_tests
docker system prune -f

echo "Тесты завершены. Отчет Allure находится в: $SCRIPT_DIR/allure-report"
