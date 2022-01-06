class MATestWithUniverse(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.SetEndDate(2018,1,1)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage)
        self.shortList = []
        self.longList = []

        self.stop = False
        
        self.__numberOfSymbols = 5
        self.__numberOfSymbolsFine = 5
        self._changes = None
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        
    def CoarseSelectionFunction(self, coarse):
        sortedByDollarVolume = sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)
        filtered = [ x.Symbol for x in sortedByDollarVolume if x.HasFundamentalData ]
        return filtered[:self.__numberOfSymbols]
    
    def FineSelectionFunction(self, fine):
        sortedByPeRatio = sorted(fine, key=lambda x: x.ValuationRatios.PERatio, reverse=True)
        return [ x.Symbol for x in sortedByPeRatio[:self.__numberOfSymbolsFine] ]
  
        
    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
        

        self.Log(f"OnData({self.UtcTime}): Keys: {', '.join([key.Value for key in data.Keys])}")
        # if we have no changes, do nothing
        if self._changes is None: return

        
        #stocks = self.stocks
        
        for security in self._changes.RemovedSecurities:
            if security.Invested:
                self.Liquidate(security.Symbol)

        
        
        
        for security in self._changes.AddedSecurities:
            stock = security.Symbol
            stockData = self.History([stock], 30, Resolution.Daily)
            MA21Pre = stockData.close[8:29].mean()
            MA5Pre = stockData.close[24:29].mean()
            MA21Curr = stockData.close[9:30].mean()
            MA5Curr = stockData.close[25:30].mean()
            
            
            if stock not in self.longList and stock not in self.shortList:
                self.Debug("Trading stock :" + str(stock))
                  #Checking Bullish Crossover
                if MA5Pre < MA21Pre and MA5Curr > MA21Curr:
                    #self.Debug("checking long condition")
                    self.SetHoldings (stock, 1 / (self.__numberOfSymbols + self.__numberOfSymbolsFine))
                    self.longList.append(stock)
                
                #Checking Bearish Crossover    
                if MA5Pre > MA21Pre and MA5Curr < MA21Curr:
                    #self.Debug("checking short condition")
                    self.SetHoldings (stock, -1 / (self.__numberOfSymbols + self.__numberOfSymbolsFine))
                    self.shortList.append(stock)
            
            #exit and again entry        
            if stock in self.longList:
                #Checking Bearish Crossover 
                if MA5Pre > MA21Pre and MA5Curr < MA21Curr:
                    self.SetHoldings (stock, -1 / (self.__numberOfSymbols + self.__numberOfSymbolsFine))
                    self.longList.remove(stock)
                    self.shortList.append(stock)
                
            if stock in self.shortList:
                #Checking Bullish Crossover
                if MA5Pre < MA21Pre and MA5Curr > MA21Curr:
                    self.SetHoldings (stock, 1 / (self.__numberOfSymbols + self.__numberOfSymbolsFine))
                    self.shortList.remove(stock)
                    self.longList.append(stock)
        
        self._changes = None
        

        
                    
        # this event fires whenever we have changes to our universe
    def OnSecuritiesChanged(self, changes):
        self._changes = changes
        self.Log(f"OnSecuritiesChanged({self.UtcTime}):: {changes}")

    def OnOrderEvent(self, fill):
        self.Log(f"OnOrderEvent({self.UtcTime}):: {fill}")
    


