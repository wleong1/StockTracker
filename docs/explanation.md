# StockTracker
## Compatibility

This project has been tested on:

- WSL 2 on Windows running Ubuntu 22.04
- Ubuntu 22.04

## Motivation

The motivation behind this project is to improve the developer's financial literacy and learn software engineering best practices.

## Project Structure

The main components of this project are:

- *Web app*: Built using Python Streamlit
- *Business logic*: Implemented using Python and Flask
- *Database*: PostgreSQL

## Technologies Used

- Python 3.10
- Flask
- Plotly
- Pandas
- psycopg2-binary
- Streamlit
- yfinance
- PostgreSQL

## User Interface

### User Interface
![alt text](user-interface-diagram.png)

The image above illustrates what a user would see if the project is set up successfully.

## Architecture

### Architecture Diagram

![alt text](architecture-diagram.png)

The idea behind the project is to split each microservice into respective containers:

- Web app container
- Business logic container
- Database container

An ***NFS server*** is set up to allow sharing of PostgreSQL backup files (*.dump*) with the PostgreSQL ***database container***, which acts as the *NFS client*. Any user interactions with the ***web app container*** will send requests via *RESTful API* to the ***business logic container***, which in turn sends the requests to the ***database container*** via the *database connection*.

## Demo

A version of the web app that contains part of the database has been deployed. Feel free to give that a go.

[Demo link](https://wleong1-stocktracker.streamlit.app/)