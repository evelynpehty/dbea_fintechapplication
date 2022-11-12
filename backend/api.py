from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions
# from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

import pandas as pd
import numpy as np
import yfinance as yf
from pandas_datareader import data

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Read in price data


@app.route('/getoptimizeportfolio', methods=["POST"])
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
    # total_portfolio_value = request_data["total_portfolio_value"]

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

        weights = ef.max_sharpe()  # raw output from the optimizer
        # which truncates tiny weights to zero and rounds the rest
        cleaned_weights = ef.clean_weights()

        # expected performance of the portfolio with optimal weights
        portfolio_performance = ef.portfolio_performance()
        expected_annual_return = portfolio_performance[0]
        annual_volatility = portfolio_performance[1]
        sharpe_ratio = portfolio_performance[2]

        # latest_prices = get_latest_prices(df)
        # da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=total_portfolio_value)
        # allocation = da.lp_portfolio()

        weight_json = {}
        performance_json = {}

        for i in cleaned_weights:
            weight_json[i] = str(cleaned_weights[i])

        '''
        for x in allocation[0]:
            performance_json[x] = str(allocation[0][x])
        '''

        return jsonify({
            "code": 200,
            "response": {
                "cleaned_weights": weight_json,
                "performance": {
                    "expected_annual_return": expected_annual_return,
                    "annual_volatility": annual_volatility,
                    "sharpe_ratio": sharpe_ratio
                }
            },
            "message": "success!"
        }), 200

    except:
        return jsonify({
            "code": 404,
            "message": "No Data Found!"
        }), 404


@app.route('/getlowestriskportfolio', methods=["POST"])
def lowestrisk_portfolio():
    '''
    example of json body
    {
        "start_date":"2017-01-01",
        "end_date": "2021-12-31",
        "tickers":["AAPL", "TSLA"],
    }
    '''

    request_data = request.get_json()
    start_date = request_data["start_date"]
    end_date = request_data["end_date"]
    tickers = request_data["tickers"]
    # total_portfolio_value = request_data["total_portfolio_value"]

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

        weights = ef.min_volatility()  # raw output from the optimizer
        # which truncates tiny weights to zero and rounds the rest
        cleaned_weights = ef.clean_weights()

        # expected performance of the portfolio with optimal weights
        portfolio_performance = ef.portfolio_performance()
        expected_annual_return = portfolio_performance[0]
        annual_volatility = portfolio_performance[1]
        sharpe_ratio = portfolio_performance[2]

        '''
        latest_prices = get_latest_prices(df)
        da = DiscreteAllocation(
            cleaned_weights, latest_prices, total_portfolio_value=total_portfolio_value)
        allocation = da.lp_portfolio()
        '''

        weight_json = {}
        performance_json = {}

        for i in cleaned_weights:
            weight_json[i] = str(cleaned_weights[i])

        '''
        for x in allocation[0]:
            performance_json[x] = str(allocation[0][x])
        '''

        return jsonify({
            "code": 200,
            "response": {
                "cleaned_weights": weight_json,
                "performance": {
                    "expected_annual_return": expected_annual_return,
                    "annual_volatility": annual_volatility,
                    "sharpe_ratio": sharpe_ratio
                }
            },
            "message": "success!"
        }), 200

    except:
        return jsonify({
            "code": 404,
            "message": "No Data Found!"
        }), 404

#########################################################################################

# get highest sharpe ratio portfolio


@app.route('/gethighestriskportfolio', methods=["POST"])
def highestrisk_portfolio():
    '''
    example of json body
    {
        "start_date":"2017-01-01",
        "end_date": "2021-12-31",
        "tickers":["AAPL", "TSLA"],
    }
    '''

    # data input
    request_data = request.get_json()
    start_date = request_data["start_date"]
    end_date = request_data["end_date"]
    tickers = request_data["tickers"]
    n_portfolios = 10**5
    n_days = 252
    n_assets = len(tickers)

    try:
        # get data of the stocks
        prices_df = yf.download(tickers, start=start_date, end=end_date, adjusted=True)

        # efficient frontier codes
        returns_df = prices_df['Adj Close'].pct_change().dropna()
        avg_returns = returns_df.mean() * n_days
        cov_mat = returns_df.cov() * n_days
        np.random.seed(42)
        weights = np.random.random(size=(n_portfolios, n_assets))
        weights /= np.sum(weights, axis=1)[:, np.newaxis]
        portf_rtns = np.dot(weights, avg_returns)
        portf_vol = []
        for i in range(0, len(weights)):
            portf_vol.append(np.sqrt(np.dot(weights[i].T,
                                            np.dot(cov_mat, weights[i]))))
        portf_vol = np.array(portf_vol)
        portf_sharpe_ratio = portf_rtns / portf_vol
        portf_results_df = pd.DataFrame({'returns': portf_rtns,
                                 'volatility': portf_vol,
                                 'sharpe_ratio': portf_sharpe_ratio})
        N_POINTS = 100
        portf_vol_ef = []
        indices_to_skip = []

        portf_rtns_ef = np.linspace(portf_results_df.returns.min(), 
                                    portf_results_df.returns.max(), 
                                    N_POINTS)
        portf_rtns_ef = np.round(portf_rtns_ef, 2)    
        portf_rtns = np.round(portf_rtns, 2)

        for point_index in range(N_POINTS):
            if portf_rtns_ef[point_index] not in portf_rtns:
                indices_to_skip.append(point_index)
                continue
            matched_ind = np.where(portf_rtns == portf_rtns_ef[point_index])
            portf_vol_ef.append(np.min(portf_vol[matched_ind]))
            
        portf_rtns_ef = np.delete(portf_rtns_ef, indices_to_skip)
        max_sharpe_ind = np.argmax(portf_results_df.sharpe_ratio)
        max_sharpe_portf = portf_results_df.loc[max_sharpe_ind]

        min_vol_ind = np.argmin(portf_results_df.volatility)
        min_vol_portf = portf_results_df.loc[min_vol_ind]

        # prepare data for json
        weight_json = {}

        #for i in weights[np.argmax(portf_results_df.sharpe_ratio)]:
        #    weight_json[i] = str(i)
        
        for x, y in zip(tickers, weights[np.argmax(portf_results_df.sharpe_ratio)]):
            weight_json[x] = str(y)

        expected_annual_return = max_sharpe_portf[0]
        annual_volatility = max_sharpe_portf[1]
        sharpe_ratio = max_sharpe_portf[2]

        return jsonify({
            "code": 200,
            "response": {
                "cleaned_weights": weight_json,
                "performance": {
                    "expected_annual_return": expected_annual_return,
                    "annual_volatility": annual_volatility,
                    "sharpe_ratio": sharpe_ratio
                }
            },
            "message": "success!"
        }), 200

    except:
        return jsonify({
            "code": 404,
            "message": "No Data Found!"
        }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
