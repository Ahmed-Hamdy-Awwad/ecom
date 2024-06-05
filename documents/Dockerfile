FROM python:3.8
EXPOSE 8000
WORKDIR /app 
COPY . /app
RUN python3 -m pip install -r requirements.txt
ENV LIVE 1
ENTRYPOINT ["python3"]
CMD ["manage.py", "migrate"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]