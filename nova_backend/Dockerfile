FROM python:3.11.1
ENV PYTHONBUFFERED 1;

WORKDIR /code 

COPY requirements.txt  /code/

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD [ "python"  ,"manage.py" ,"runserver", "0.0.0.0:8000"]