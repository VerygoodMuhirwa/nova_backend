FROM python:3.11.1
ENV PYTHONBUFFERED 1;

WORKDIR /code 

COPY ./nova_backend/ /code

COPY ./nova_backend/requirements.txt  .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python3"  ,"manage.py" ,"runserver"]