FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
#need to modify ansible.cfg
EXPOSE 8000
CMD ["./manage.py makemigrations && ./manage.py migrate"]
CMD ["./manage.py runserver 0:8000"]
