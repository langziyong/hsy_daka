FROM python
RUN pip install requests Flask PyMySQL schedule gunicorn Beautifulsoup4
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN mkdir /project
COPY ./ /project
WORKDIR /project
#CMD python3 daka/Task.py
#CMD gunicorn --workers=4 --threads=2 --worker-class=gthread -b 0.0.0.0:9999 app:app
CMD ./start.sh