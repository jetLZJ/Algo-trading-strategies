class EthPsar(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.SetEndDate(2018, 1, 1)
        self.SetCash(10000)
        
        
        self.aapl = self.AddEquity("AMZN", Resolution.Daily)
        self.aapl.SetDataNormalizationMode(DataNormalizationMode.Raw)
        
        self.eth = self.AddCrypto("ETHUSD", Resolution.Daily, Market.GDAX)
        self.eth.SetDataNormalizationMode(DataNormalizationMode.Raw)
        
        self.asset_best_price = {}
        
        #Save Indicators
        self.psar = self.PSAR("ETHUSD", 0.02, 0.02, 0.2, Resolution.Daily)
        self.adx = self.ADX("ETHUSD", 14, Resolution.Daily)
        self.rsi = self.RSI("ETHUSD", 14)
        
    
    #Check if our indicators are ready
    def is_ready(self):
        return self.psar.IsReady and self.adx.IsReady and self.rsi.IsReady
    


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
        
        self.asset_best_price["ETHUSD"] = float(self.Portfolio["ETHUSD"].AveragePrice)
        if not self.Portfolio.Invested and self.psar.Current.Value < self.Securities["ETHUSD"].Price*0.95:# or self.rsi.Current.Value < 40): #and self.adx.Current.Value > 25 
            self.SetHoldings("ETHUSD",1)    
                
                
        #if self.Portfolio.Invested and self.adx.Current.Value > 25 and self.psar.Current.Value > self.Securities["ETHUSD"].Price:
         #   self.Liquidate()
        if self.Portfolio.Invested:
            
            # update best price
            self.asset_best_price["ETHUSD"] = np.maximum(self.asset_best_price["ETHUSD"], float(self.Securities["ETHUSD"].Price))
            # have we exceeded the target limits?
            if (float(self.Securities["ETHUSD"].Price)-self.asset_best_price["ETHUSD"])/self.asset_best_price["ETHUSD"] < -0.03:
                # cover the position
                self.Liquidate()
                del self.asset_best_price["ETHUSD"]
            
            elif self.psar.Current.Value > self.Securities["ETHUSD"].Price*1.05:#or self.rsi.Current.Value > 100: #self.adx.Current.Value > 25 
                self.Liquidate()
                del self.asset_best_price["ETHUSD"]
    def OnEndOfAlgorithm(self):
        self.Liquidate()
        self.Debug("Liquidated cash is USD " + str(self.Portfolio.Cash))
