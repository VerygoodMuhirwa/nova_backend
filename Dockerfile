FROM python:3.11.1
ENV PYTHONBUFFERED 1;

WORKDIR /code 

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .
EXPOSE 3500

CMD [ "python","manage.py" ,"runserver"]