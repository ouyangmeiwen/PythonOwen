django-admin startproject djapps
cd djapps

python manage.py startapp api




python manage.py makemigrations

python manage.py migrate 

python manage.py createsuperuser   
    admin 123456




打包

settings.py
     DEBUG = False

pyinstaller --onefile --name djapps manage.py



./dist/djapps runserver 0.0.0.0:9001 --noreload



#windows djapps.exe runserver 0.0.0.0:9001

gunicorn djapps.wsgi:application --bind 0.0.0.0:9001 --workers 4


//get
http://127.0.0.1:9001/api/hello?name=Owen

//get
http://127.0.0.1:9001/api/libitem?page=1&size=1

//GetItemList  post
curl -X POST http://127.0.0.1:9001/api/libitems/GetItemList/ \
     -H "Content-Type: application/json" \
     -d '{"SkipCount": 0, "MaxResultCount": 10}'

curl -X GET http://127.0.0.1:9001/api/sysmenu/QueryMenus/



docker build -t djapps:latest . -f Dockerfile
docker run -d -p 9001:9001 --restart=always   --name djapps djapps:latest
docker run -d -p 9001:9001    --name djapps djapps:latest




docker build -t djapps:1.0 . -f Dockerfiledist
docker run -d -p 9001:9001 --restart=always   --name djapps1.0 djapps:1.0
docker run -d -p 9001:9001   --name djapps1.0 djapps:1.0





增加jwt 认证
pip install djangorestframework
pip install djangorestframework-simplejwt


curl -X POST http://127.0.0.1:9001/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "123456"}'



curl -X POST http://127.0.0.1:9001/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA2MzkzMCwiaWF0IjoxNzQwOTc3NTMwLCJqdGkiOiIzOTg0MWYxMTU2Njg0ZTVlOTdjZWU5ZDQ1OGZlNjA0MSIsInVzZXJfaWQiOjF9.vmhrtcmnYc3e2ClQKfHRKM6sMZLdcHj_1tjJvIBaIYY","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxMDYzOTMwLCJpYXQiOjE3NDA5Nzc1MzAsImp0aSI6IjZiOTEzMzMwY2RkYTQyNTI4MDlhZjg5NDIyODUzMjU1IiwidXNlcl9pZCI6MX0.YkpO_QAgtRqp2WnjE7bXZ8AKgXQFGntYzs-Fzd7JNVc"}'

curl -X GET http://127.0.0.1:9001/api/libitem?name=Owen \
     -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxMDY0MTA3LCJpYXQiOjE3NDA5Nzc3MDcsImp0aSI6IjhmOTcxNjUwMGFiOTQzNWI4NGRiNjc0Mzk2NzExZGIzIiwidXNlcl9pZCI6MX0.Lw743p2P7-BWBra4cKjgC5bHAghyCm_54fwVfN3O7ig"
