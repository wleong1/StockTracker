StockTracker
The StockTracker project is designed to process and analyze stock performance data for a list of companies. It provides valuable insights by displaying graphs of historical performance, showcasing the latest available prices, and presenting the most recent news related to the companies. With a user-friendly graphical interface, it enables users to compare and analyze the performance of multiple companies simultaneously.

Usage
To get started with StockTracker, follow the steps below:

Clone the project repository using Git.

Ensure that your pip package manager is up to date by running the command pip install --upgrade pip.

Install the required modules by executing the command pip install -r ./requirements.txt.

Download the stock data from the following source: https://www.kaggle.com/datasets/camnugent/sandp500.

Extract the downloaded file and navigate to the extracted folder.

Locate the directory named "individual_stocks_5yr" within the first "individual_stocks_5yr" directory and copy it.

Paste the "individual_stocks_5yr" directory into the StockTracker repository.

Within the src directory of the project, create a new Python file named "parameter.py".

Inside "parameter.py", create two variables: NEWS_API_KEY and ALPHA_VANTAGE_API_KEY.

Assign your News API and Alpha Vantage API keys to the respective variables in "parameter.py".

Run the main.py file to start the StockTracker application.

Please note that this project relies on external data sources and requires valid API keys to access the necessary information. Make sure to provide your own API keys to ensure proper functionality.

License
This project is licensed under the MIT License.

Support or Contact
For any issues or questions related to the StockTracker project, please feel free to reach out by creating an issue on the GitHub repository or contacting the project maintainers through the provided channels.

We appreciate your interest in StockTracker and look forward to your feedback and contributions!
