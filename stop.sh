docker-compose down
kill $(lsof -t -i:3000)
kill $(lsof -t -i:8000)


