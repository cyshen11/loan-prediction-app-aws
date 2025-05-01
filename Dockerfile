FROM tiangolo/uwsgi-nginx-flask:python3.10
COPY ./app /app
RUN pip install pip --upgrade
RUN pip install --no-cache-dir -r /app/requirements.txt
ENV LISTEN_PORT=8080
EXPOSE 8080