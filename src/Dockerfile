FROM ubuntu:22.04

# Set a directory for the app
WORKDIR /usr/src/

# Copy all the files to the container
COPY . .

# Install dependencies
RUN apt-get update
RUN apt-get install -y python3
RUN apt install -y python3-pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the shell script into the image
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the shell script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
