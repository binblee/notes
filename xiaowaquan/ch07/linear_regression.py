# 导入函数库
from jqdata import *
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge


# 初始化函数，设定基准等等
def initialize(context):
    set_params()
    set_backtest()
    run_daily(trade, 'every_bar')
    
def set_params():
    g.days = 0
    g.refresh_rate = 5
    g.stocknum = 10
    
def set_backtest():
    set_benchmark('000001.XSHG')
    set_option('use_real_price', True)
    log.set_level('order', 'error')
    
def trade(context):
    if g.days % 5 == 0:
        stocks = get_index_stocks('000016.XSHG', date=None)
        q = query(valuation.code, valuation.market_cap, 
                  balance.total_assets - balance.total_liability,
                  balance.total_assets/balance.total_liability,
                  income.net_profit, indicator.inc_revenue_year_on_year,
                  balance.development_expenditure).filter(valuation.code.in_(stocks))
        df = get_fundamentals(q, date=None)
        df.columns=['code','mcap', 'na', '1/DA ratio', 'net income', 'growth', 'RD']
        df.index = df['code'].values
        df = df.drop('code', axis=1)
        df = df.fillna(0)
        X = df.drop('mcap', axis=1)
        y = df['mcap']
        X = X.fillna(0)
        y = y.fillna(0)
        reg = LinearRegression()
        model = reg.fit(X, y)
        predict = pd.DataFrame(model.predict(X), index = y.index, columns=['predict_mcap'])
        diff = df['mcap'] - predict['predict_mcap']
        diff = pd.DataFrame(diff, index = y.index, columns=['diff'])
        diff = diff.sort_values(by = 'diff', ascending=True)
        stockset = list(diff.index[:10])
        sell_list = list(context.portfolio.positions.keys())
        cash = 0
        num = 0
        for stock in sell_list:
            if stock not in stockset[:g.stocknum]:
                stock_sell = stock
                order_target_value(stock_sell, 0)
        cash = 0
        num = 0
        if len(context.portfolio.positions) < g.stocknum:
            num = g.stocknum - len(context.portfolio.positions)
            cash = context.portfolio.cash / num

        for stock in stockset[:g.stocknum]:
            if stock in sell_list:
                pass
            else:
                stock_buy = stock
                order_target_value(stock_buy, cash)
                num = num -1
                if num == 0:
                    break
    g.days += 1
