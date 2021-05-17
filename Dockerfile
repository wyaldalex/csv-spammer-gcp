# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

# set work directory
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . /usr/src/app/

# install dependencies
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
#COPY ./Pipfile /usr/src/app/Pipfile
#RUN pipenv install --skip-lock --system --dev

# run development server
CMD python ./manage.py runserver 0.0.0.0:$PORT

#To run:
#docker build -t csv-messenger -f Dockerfile .
#docker run --env PORT=5000 -it -p 80:5000 csv-messenger