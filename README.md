# **StockTracker**

StockTracker is a Python application that help analyse and visualise stock performance data for a list of companies. It provides a user-friendly GUI for comparing stock prices, viewing historical trends, and staying updated with the latest news.

## Table of Contents

- [Project Description](#project-description)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Tests](#tests)
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
- PyQt5
- Bokeh
- Matplotlib
- Numpy
- Pandas
- Unittest

## **Installation**

1. Clone the project repository using Git.
2. Ensure that your pip package manager is up to date by running the command 
```pip install --upgrade pip```.
3. Install the required modules by executing the command 
```pip install -r ./requirements.txt```

## **Usage**

1. Download the stock data from the following source: https://www.kaggle.com/datasets/camnugent/sandp500.
2. Extract the downloaded file and navigate to the extracted folder.
3. Locate the directory named _individual_stocks_5yr_ within the first _individual_stocks_5yr_ directory and copy it.
4. Paste the _individual_stocks_5yr_ directory into the __StockTracker__ repository.
5. Within the _src_ directory of the project, create a new Python file named _parameter.py_.
6. Inside _parameter.py_, create two variables: __NEWS_API_KEY__ and __ALPHA_VANTAGE_API_KEY__.
7. Assign your __News API__ and __Alpha Vantage API__ keys to the respective variables in _parameter.py_.
8. Run the _main.py_ file to start the __StockTracker__ application.
    
Note: 
- This project relies on external data sources and requires valid API keys to access the necessary information. Make sure to provide your own API keys to ensure proper functionality.
- The demonstration of the GUI functionality utilises older data. To ensure you have the most recent graph representation, replace the provided data with updated information.

## **Screenshots**

![image](https://github.com/wleong1/StockTracker/assets/122815453/bd739475-5fe7-4342-99ef-a28674e004f9)

The image showcases the GUI, featuring elements such as the company selection dropdown menu, latest closing price, current news, and historical performance.

## **Tests**

StockTracker incorporates various tests to ensure its stability and reliability. To execute these tests, follow these steps:

1. Go to the tests directory.
2. Replace the sample_data files with a subset of files you intend to test, maintaining a similar naming convention.
3. Adjust the test scripts as necessary.

## **Contributing**

Contributions to StockTracker are welcome! If you'd like to contribute, please follow these guidelines:

1. Fork the project.
2. Create your feature branch (git checkout -b feature/your-feature-name).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/your-feature-name).
5. Open a pull request.

# **License**

This project is licensed under the MIT License.
