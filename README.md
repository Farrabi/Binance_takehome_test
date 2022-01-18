# Binance Takehome Test
## About The Test
Below are the question to be answered using any programming language.

1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.
2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.
3. Using the symbols from Q1, what is the total notional value of the top 200 bids and asks currently on each order book?
4. What is the price spread for each of the symbols from Q2?
5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.
6. Make the output of Q5 accessible by querying http://localhost:8080/metrics using the Prometheus Metrics format.

## Pre-requisite
Install requirements.txt
```
pip3 install -r requirements.txt on Linux/MacOs. 
or
pip install -r requirements.txt on Windows
```

## Usage
Instruction on how to run the script.
```
python3 binance_client.py
or
python binance_client.py
```

Answer of Q1, Q2, Q3, Q4 will appear on the terminal right away. 
Answer of Q5 will be printed every 10 seconds. 
Visit http://localhost:8080/metrics to see the answer of Q6. 

## To Do / Next Steps
- Unit tests
- Handling of exceptions
- Create an API endpoint to serve near real-time data as the market is volatile and the top 5 crypto will fluctuate. This can be done using a websocket or simply refresh the endpoint every seconds.

