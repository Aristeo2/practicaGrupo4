FROM python:3.11-slim

RUN mkdir /sqlalchemy

COPY requirements.txt /sqlalchemy

WORKDIR /sqlalchemy

RUN pip install -r requirements.txt

COPY . /sqlalchemy

EXPOSE 8501

CMD ["python", "run", "sqlalchemy/data/creardb.py"]
