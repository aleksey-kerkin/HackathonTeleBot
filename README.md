Для работы бота требуется:

В корневом каталоге создать файл .env в нем добавить  
```
TOKEN="ВАШ_ТОКЕН_ДЛЯ_ТЕЛЕГРАММ_БОТА" 
DATABASE_URL = postgresql://postgres:postgres@172.18.0.2/vacation
```

И запустить команду:

`docker-compose up --build`
