import pandas as pd

class FatYellowGreenHornet(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 1, 1)  # Set Start Date
        #self.SetEndDate(2017, 12, 31)  # Set Start Date
        
        self.SetCash(100000)  # Set Strategy Cash

        self.long_list = []
        self.short_list = []
        self.stop = False
        self.betsize = 0.1
        self.long_betsize = 0.1
        self.short_betsize = 0.1
        
        #self.AddCrypto("BTCUSD", Resolution.Daily, Market.GDAX)
        
        self.AddForex("EURUSD", Resolution.Daily)
        self.AddForex("GBPJPY", Resolution.Daily)
        self.AddForex("USDJPY", Resolution.Daily)
        self.AddForex("AUDUSD", Resolution.Daily)
        self.AddForex("USDCHF", Resolution.Daily)
        self.AddForex("USDCAD", Resolution.Daily)
        
        self.AddEquity("SPY", Resolution.Daily)
        self.AddEquity("QQQ", Resolution.Daily)
        self.AddEquity("XLV", Resolution.Daily)
        self.AddEquity("XLY", Resolution.Daily)    
        self.AddEquity("XLF", Resolution.Daily)    
        self.AddEquity("XLI", Resolution.Daily)    
        #self.AddEquity("IWM", Resolution.Daily)
        
        
        self.AddEquity("BND", Resolution.Daily)
        self.AddEquity("BNDX", Resolution.Daily)
        self.AddEquity("HYG", Resolution.Daily)
        self.AddEquity("AGG", Resolution.Daily)
        self.AddEquity("VCIT", Resolution.Daily)
        self.AddEquity("LQD", Resolution.Daily)
        
        self.AddEquity("GLD", Resolution.Daily)
        self.AddEquity("SLV", Resolution.Daily)
        self.AddEquity("DBC", Resolution.Daily)
        self.AddEquity("USO", Resolution.Daily)
        self.AddEquity("DBA", Resolution.Daily)
        self.AddEquity("BTC", Resolution.Daily)        
        
        #self.gold=self.AddFuture(Futures.Metals.Gold) 
        #self.Debug(self.gold.Symbol) #/GC
        
        #self.AddCfd("US30_USD", Resolution.Daily, Market.Oanda)
        #self.AddCfd("CORN_USD", Resolution.Daily, Market.Oanda)

        #self.currencies = ["EURUSD", "GBPJPY", "BTCUSD"]
        self.currencies = ["EURUSD", "GBPJPY", "USDJPY", "AUDUSD", "USDCHF", "USDCAD", "SPY", "QQQ", "XLI", "XLV", "XLY", "XLF", "BND", "BNDX", "HYG", "AGG", "VCIT", "LQD", "GLD", "SLV", "DBC", "USO", "DBA", "BTC"]
        
        #self.currencies = ["EURUSD","GBPJPY", "USDJPY", "AUDUSD", "USDCHF", "USDCAD", "SPY","QQQ", "IWM", "VEA", "VNQ", "XLF", "BND", "BNDX", "HYG", "GLD", "SLV"]
        #self.currencies = ["SPY", "QQQ", "AAPL","AMZN"]
        
        
        #self.rsi = self.RSI("EURUSD", 14)
        #self.macd = self.MACD("EURUSD", 12, 26, 9, MovingAverageType.Exponential, Resolution.Daily)
        
        self.back_1= None
        self.back_2 = None
        self.current = None
        self.entry_price = None
        

    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''

        # if not self.Portfolio.Invested:
        #    self.SetHoldings("SPY", 1)
        
        if self.stop:
            return
        
        #1. Limit trading to happen once per week
        if not self.Time.weekday() ==0: #monday is 0
            return
        
        currencies = self.currencies
        
        for currency in currencies:
            #calculate moving averages
            currency_data = self.History([currency], 30, Resolution.Daily)
            
            #self.Debug(currency_data)
            
            #history_currency = currency_data["close"].tolist()
        
            #make a dataframe for easier visual and calculation
            #df = pd.DataFrame()
            #store previously obtained spy and tsla prices in dataframe
            
            #df[currency]= history_currency
            #self.Debug(df)
                  
            MA21_Pre = currency_data.close[8:29].mean()
            MA5_Pre = currency_data.close[24:29].mean()
            MA21_Current = currency_data.close[9:30].mean()
            MA5_Current = currency_data.close[25:30].mean()
            
            
            #first trade
            #check both conditions
            if currency not in self.long_list and currency not in self.short_list:
                #check bullish
                if MA5_Pre < MA21_Pre and MA5_Current> MA21_Current:
                    self.long_list.append(currency)
            
                    self.Debug('Bought: '+ currency)
            
                #check bearish
                if MA5_Pre > MA21_Pre and MA5_Current < MA21_Current:
                    self.short_list.append(currency)
                    
                    self.Debug('Sold: '+ currency)

            
            #exit and again entry
            if currency in self.long_list:
                #checking Bearish Crossover
                if MA5_Pre > MA21_Pre and MA5_Current < MA21_Current:
                    self.long_list.remove(currency)
                    self.short_list.append(currency)
            
                    self.Debug('Sold: '+ currency)
            
            
            if currency in self.short_list:
            #check bullish
                if MA5_Pre < MA21_Pre and MA5_Current > MA21_Current:
                    self.short_list.remove(currency)
                    self.long_list.append(currency)
        
                    self.Debug('Bought: '+ currency)
        
        '''
        #Calculate bet size
        stock_length= len(self.long_list) + len(self.short_list)
        if stock_length == 0:
            self.betsize = 1
        else: 
            self.betsize = 1/stock_length
        
        self.Debug('Betsize is ' + str(self.betsize))
        
        for currency in self.long_list :
            self.SetHoldings(currency, self.betsize)
            
        for currency in self.short_list:
            self.SetHoldings(currency, -self.betsize)

        '''
        

        #stock_length= len(self.long_list) + len(self.short_list)
        if len(self.long_list) == 0:
            self.long_betsize = 0
        else: 
            self.long_betsize = 0.5/len(self.long_list) * 0.98 #buffer
        
        if len(self.short_list) == 0:
            self.short_betsize = 0
        else: 
            self.short_betsize = -0.5/len(self.short_list) * 0.98 #buffer

        self.Debug('Long Betsize is ' + str(self.long_betsize) + 'Short betsize is'+ (str(self.short_betsize)))
        

        for currency in self.long_list :
            #quantity = self.CalculateOrderQuantity(currency, self.long_betsize)
            #self.MarketOnCloseOrder(currency, quantity)

            self.SetHoldings(currency, self.long_betsize)
            
        for currency in self.short_list:
            #quantity = self.CalculateOrderQuantity(currency, self.short_betsize)
            #self.MarketOnCloseOrder(currency, quantity)

            self.SetHoldings(currency, self.short_betsize)
            
       # if self.Portfolio.Cash < 85000:
        #    self.stop = True
         #   self.Liquidate()
            
