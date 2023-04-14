docker-compose up -d
cd frontend
npm run dev & disown
cd ..
cd backend
python manage.py runserver & disown
cd ..