FROM python:3.10-slim

# Set a directory for the app
WORKDIR /app

# Copy all the files to the container
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 8501

# Check the health of app
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Set the entrypoint
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
