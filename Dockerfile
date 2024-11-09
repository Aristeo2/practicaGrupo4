FROM python:3.11-slim

RUN mkdir /streamlit

COPY requirements.txt /streamlit

WORKDIR /streamlit

RUN pip install -r requirements.txt

COPY . /streamlit

EXPOSE 8501

CMD ["streamlit", "run", "Formulario.py", "--server.port=8501", "--server.address=0.0.0.0"]

