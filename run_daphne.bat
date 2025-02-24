@echo off
cd /d "C:\Users\oluwa\Desktop\Desktop apps\pythonprojects\facebook"
call .venv\Scripts\activate
daphne -b 0.0.0.0 -p 8000 facebook.asgi:application
pause
