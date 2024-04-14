# **StockTracker**

StockTracker is a Python application that help analyse and visualise stock performance data for a list of companies. It provides a user-friendly GUI for comparing stock prices, viewing historical trends, and staying updated with the latest news.

## Table of Contents

- [Project Description](#project-description)
- [Technologies](#technologies)
- [Installation](#installation)
- [Screenshots](#screenshots)
- [Tests (Deprecated)](#tests)
- [Contributing](#contributing)
- [License](#license)

## Project Description

StockTracker is designed to simplify stock analysis and decision-making. It fetches stock data for multiple companies, plots interactive graphs, and offers real-time news updates. Key features include:

- Graphical representation of historical stock prices.
- Live stock price tracking and display.
- Integration with Alpha Vantage, providing the latest available closing price.
- Integrate with News API for up-to-date news related to selected companies.

## Technologies

- Python 3.10
- Flask
- Plotly
- Pandas
- psycopg2-binary
- Streamlit
- yfinance
- PostgreSQL

## **Installation**

Please refer to  for detailed installation instructions.

## **Screenshots**

![image](./docs/user-interface-diagram.png)

The image showcases the GUI, featuring elements such as the company selection dropdown menu, latest closing price, current news, and historical performance.

## **Tests (Deprecated)**

StockTracker incorporates various tests to ensure its stability and reliability. To execute these tests, follow these steps:

1. Go to the tests directory.
2. Run the tests.

NOTE: This section is deprecated due to the migration from csv files to PostgreSQL database.

## **Contributing**

Contributions to StockTracker are welcome! If you'd like to contribute, please follow these guidelines:

1. Fork the project.
2. Create your feature branch (git checkout -b feature/your-feature-name).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/your-feature-name).
5. Open a pull request.

# **License**

This project is licensed under the MIT License.
