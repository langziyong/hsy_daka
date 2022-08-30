python3 daka/Task.py&
gunicorn --workers=4 --threads=2 --worker-class=gthread -b 0.0.0.0:8012 app:app