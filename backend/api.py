from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

import pandas as pd
import numpy as np
from pandas_datareader import data

from flask import Flask, request, jsonify, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Read in price data

@app.route('/getoptimizeportfolio', methods=["GET"])
def optimize_portfolio():
    
    '''
    example of json body
    {
        "start_date":"2017-01-01",
        "end_date": "2021-12-31",
        "tickers":["AAPL", "TSLA"],
        "total_portfolio_value": 20000
    }
    '''
    
    request_data = request.get_json()
    start_date = request_data["start_date"]
    end_date = request_data["end_date"]
    tickers = request_data["tickers"]
    total_portfolio_value = request_data["total_portfolio_value"]
    
# Use pandas_reader.data.DataReader to load data
    try:
        df = data.DataReader(tickers, 'yahoo', start_date, end_date)
        
        df = df["Adj Close"]

        # Calculate expected returns and sample covariance
        mu = expected_returns.mean_historical_return(df)
        S = risk_models.sample_cov(df)

        # Optimize for maximal Sharpe ratio
        ef = EfficientFrontier(mu, S)
        ef.add_objective(objective_functions.L2_reg, gamma=0.1)
        
        weights  = ef.max_sharpe() #raw output from the optimizer
        cleaned_weights = ef.clean_weights() #which truncates tiny weights to zero and rounds the rest
        
        portfolio_performance = ef.portfolio_performance() #expected performance of the portfolio with optimal weights
        expected_annual_return = portfolio_performance[0]
        annual_volatility = portfolio_performance[1]
        sharpe_ratio = portfolio_performance[2]

        latest_prices = get_latest_prices(df)
        da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=total_portfolio_value)
        allocation = da.lp_portfolio()
        
        weight_json = {}
        performance_json = {}
        
        for i in cleaned_weights:
            weight_json[i] = str(cleaned_weights[i])
            
        for x in allocation[0]:
            performance_json[x] = str(allocation[0][x])
        
        return jsonify({
                "code": 200,
                "response":{
                    "cleaned_weights": weight_json,
                    "allocation": performance_json, 
                    "performance": {
                        "expected_annual_return": expected_annual_return,
                        "annual_volatility": annual_volatility,
                        "sharpe_ratio": sharpe_ratio
                    }
                },
                "message": "success!"
            }),200
    
    except:
        return jsonify({
            "code": 404,
            "message": "No Data Found!"
        }),404
    
    

@app.route('/getlowestriskportfolio', methods=["GET"])
def lowestrisk_portfolio():
     
    '''
    example of json body
    {
        "start_date":"2017-01-01",
        "end_date": "2021-12-31",
        "tickers":["AAPL", "TSLA"],
        "total_portfolio_value": 20000
    }
    '''
    
    request_data = request.get_json()
    start_date = request_data["start_date"]
    end_date = request_data["end_date"]
    tickers = request_data["tickers"]
    total_portfolio_value = request_data["total_portfolio_value"]
    
# Use pandas_reader.data.DataReader to load data
    try:
        df = data.DataReader(tickers, 'yahoo', start_date, end_date)
        
        df = df["Adj Close"]

        # Calculate expected returns and sample covariance
        mu = expected_returns.mean_historical_return(df)
        S = risk_models.sample_cov(df)

        # Optimize for maximal Sharpe ratio
        ef = EfficientFrontier(mu, S)
        ef.add_objective(objective_functions.L2_reg, gamma=0.1)
        
        weights  = ef.min_volatility() #raw output from the optimizer
        cleaned_weights = ef.clean_weights() #which truncates tiny weights to zero and rounds the rest
        
        portfolio_performance = ef.portfolio_performance() #expected performance of the portfolio with optimal weights
        expected_annual_return = portfolio_performance[0]
        annual_volatility = portfolio_performance[1]
        sharpe_ratio = portfolio_performance[2]

        latest_prices = get_latest_prices(df)
        da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=total_portfolio_value)
        allocation = da.lp_portfolio()
        
        weight_json = {}
        performance_json = {}
        
        for i in cleaned_weights:
            weight_json[i] = str(cleaned_weights[i])
            
        for x in allocation[0]:
            performance_json[x] = str(allocation[0][x])
        
        return jsonify({
                "code": 200,
                "response":{
                    "cleaned_weights": weight_json,
                    "allocation": performance_json, 
                    "performance": {
                        "expected_annual_return": expected_annual_return,
                        "annual_volatility": annual_volatility,
                        "sharpe_ratio": sharpe_ratio
                    }
                },
                "message": "success!"
            }),200
    
    except:
        return jsonify({
            "code": 404,
            "message": "No Data Found!"
        }),404

if __name__ == '__main__':
  app.run(host='0.0.0.0')