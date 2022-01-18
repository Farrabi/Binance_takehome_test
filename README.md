# Binance Takehome Test
## About The Test
Below are the question to be answered using any programming language.

1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.
2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.
3. Using the symbols from Q1, what is the total notional value of the top 200 bids and asks currently on each order book?
4. What is the price spread for each of the symbols from Q2?
5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.
6. Make the output of Q5 accessible by querying http://localhost:8080/metrics using the Prometheus Metrics format.

## Requirements
Install python3.x. (preferably between 3.5 and 3.8)
Install requirements.txt using the below command line.

```
pip3 install -r requirements.txt on Linux/MacOs. 
or
pip install -r requirements.txt on Windows
```

## How to use
Instruction on how to run the script.
Open your terminal and run the below command line. 
```
python3 binance_client.py
or
python binance_client.py
```

Answers of Q1, Q2, Q3, Q4 will appear on the terminal right away. 
Answers of Q5 will be printed every 10 seconds on the terminal as well. 
Visit http://localhost:8080/metrics to see the answer of Q6. 

## To Do / Next Steps
- Unit tests. 
- Handling of exceptions. 
- Make a proper api in case if those values need to be queried regularly. 
- Maybe refresh the localhost:8080/metrics page every 10 seconds (not sure if needed). 

