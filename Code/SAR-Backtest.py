import talib
import pandas as pd
if __name__=='__main__':

    USD = 1000
    SumUsd = 1000
    Money = 0
    Price = 0
    LastPrice = 0
    bnb = 0
    Commision = 0.00075
    SumComm = 0
    Coin=pd.read_csv('d://csv//BtcBinance.csv',parse_dates=True)

    Coin['Quote'] = Coin['Quote asset volume']
    Coin['Mean'] = Coin.Quote/Coin.Volume
    Coin['Mean'] = Coin['Mean'].fillna(method='backfill')
    EMA1 = 30
    Coin['EMA'] = Coin.Mean.ewm(span=EMA1, min_periods=EMA1 ,adjust=True,ignore_na=False).mean()
    Coin['EMA'] = Coin['EMA'].fillna(method='backfill')
    Coin['high'] = Coin['High'].rolling(EMA1, min_periods=EMA1 ).max()
    Coin['high'] = Coin['high'].fillna(method='backfill')
    Coin['low'] = Coin['Low'].rolling(EMA1, min_periods=EMA1 ).min()
    Coin['low'] = Coin['low'].fillna(method='backfill')
    high = pd.Series(Coin.high, index=Coin.high.index)
    low = pd.Series(Coin.low, index=Coin.low.index)
    Coin['SAR'] = 0
    Coin['SAR'] = talib.SAR(high=high,low=low, acceleration=0.02, maximum=0.2)
        
    Coin['SARSignal'] = 0
    Coin.SARSignal[Coin.SAR < Coin.Close] = -1
    Coin.SARSignal[Coin.SAR > Coin.Close] = 1

    ShortB = 0
    ShortS = 0
      
        # تنضیمات مربوط به بازه صعودی
    i = 0
    n = 3000

        # تنضیمات مربوط به بازه نزولی
#    i = 3000
#    n = 5500
 
        # تنضیمات مربوط به بازه خنثی
#    i = 15600
#    n = 17000 
    while(i<n):
        i += 1
        Price = Coin.iloc[i].Mean
        if bnb  < (USD / 500) :
            bnb += (USD / 500) 
            Temp = (USD / 500) * Commision
            SumComm += Temp
            Temp += (USD/500)
            USD = USD - Temp                               
            
        if Coin.iloc[i].SARSignal == -1 and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            USD = 0
            ShortB += 1
            continue
       
        if (Coin.iloc[i].SARSignal == 1 and Money > 0):
            USD = Money * Coin.iloc[i].Close
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = 0 
            ShortS += 1
        
    SumUsd = USD
    SumUsd += (Money * Coin.iloc[i-1].Mean)
    SumUsd += bnb

    print("USD : ",USD)
    print("SumUSD : ",SumUsd)
    print("Sum Commision : ",SumComm)
    print("BNB : ",bnb)
    print("Short Buy : ",ShortB)
    print("Short Sell : ",ShortS)