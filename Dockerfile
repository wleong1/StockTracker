FROM ubuntu:22.04

# set a directory for the app
WORKDIR /usr/workspace/

# copy all the files to the container
COPY . .

# install dependencies
RUN apt-get update
RUN apt-get install -y python3
RUN apt install -y python3-pip
RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8000

# CMD cd django-stock-tracker && python3 manage.py runserver 0.0.0.0:8000 Can run this in the terminal
# but need to specify docker run -it -p 8888:8000 stock