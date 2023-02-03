import datetime
import numpy as np
import seaborn as sns
import scipy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import datetime



def calc_returns(srs: pd.Series, day_offset: int = 1) -> pd.Series:

    returns = srs / srs.shift(day_offset) - 1.0
    return returns




class TSMOM_strategy:
    def __init__(self,srs,VOL_LOOKBACK, VOL_TARGET, volatility_scaling=True):
        self.srs = srs
        self.VOL_LOOKBACK= VOL_LOOKBACK
        self.VOL_TARGET =VOL_TARGET
        self.volatility_scaling = volatility_scaling
        
    def trend_estimation(self,TS_LENGTH):
        '''
        This function will provide the trend estimation use for the position sizing below
        '''
        trend_estimation = calc_returns(self.srs, TS_LENGTH)
#         return self.estimation
        return trend_estimation
    
    
    def position_sizing(self,trend,activation='sign'):
        '''
        This is position sizing function which return value range from [-1,1] which indicate
        long, short, or do nothing.
        '''
        if activation=='sign':
            signal = np.maximum(0,np.sign(trend))
        elif activation =='tanh':
            signal = np.maximum(0,np.tanh(trend))
        return signal

    def calc_daily_vol(self,daily_returns):
        return (
            daily_returns.ewm(span=self.VOL_LOOKBACK, min_periods=self.VOL_LOOKBACK)
            .std()
            .fillna(method="bfill")
        )

    def calc_vol_scaled_returns(self,daily_returns):
        # if not len(daily_vol):
        daily_vol = self.calc_daily_vol(daily_returns)
        annualised_vol = daily_vol * np.sqrt(252)  # annualised
        position_map = self.VOL_TARGET / annualised_vol.shift(1)
        for idx, val in enumerate(position_map.close):
            if val > 2.0:
                position_map['close'].iloc[idx] = 2.0
        return daily_returns * position_map

    def volatility_target_map(self):
        daily_vol = self.calc_daily_vol(calc_returns(self.srs))
        annualised_vol = daily_vol * np.sqrt(252)  # annualised
        position_map = self.VOL_TARGET / annualised_vol.shift(1)
        for idx, val in enumerate(position_map.close):
            if val > 2.0:
                position_map['close'].iloc[idx] = 2.0
        return position_map

    def cal_strategy_returns(self,signal):
        '''
        This is return calculation which based on position sizing
        '''
        
        daily_returns = calc_returns(self.srs)
        next_day_returns = (
            self.calc_vol_scaled_returns(daily_returns).shift(-1)
            if self.volatility_scaling
            else daily_returns.shift(-1)
            )
        
#         signal = self.position_sizing()
        cap_returns = signal * next_day_returns
        return cap_returns