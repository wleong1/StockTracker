FROM ubuntu:22.04

# set a directory for the app
WORKDIR /usr/src/

# copy all the files to the container
COPY . .

# install dependencies
RUN apt-get update
RUN apt-get install -y python3
RUN apt install -y python3-pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask

# Copy the shell script into the image
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the shell script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# EXPOSE 8000

# CMD cd django-stock-tracker && python3 manage.py runserver 0.0.0.0:8000 Can run this in the terminal
# but need to specify docker run -it -p 8888:8000 stock