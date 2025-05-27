FROM python:3.8-slim

WORKDIR /app

COPY app.py ./

RUN pip install flask requests redis mysql-connector-python

EXPOSE 3002

CMD ["python", "app.py"]
