FROM python:3.8

WORKDIR /rest_open_hours
COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

COPY . ./

CMD coverage run -m unittest discover -v /rest_open_hours/test && coverage report