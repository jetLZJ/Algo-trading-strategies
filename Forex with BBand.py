class LogicalMagentaManatee(QCAlgorithm):

    def Initialize(self):
        #self.SetStartDate(2014, 1, 1)  # Set Start Date
        #self.SetEndDate(2018,1,1)
        self.SetStartDate(2018, 1, 1)
        self.cashStart = 100000
        self.SetCash(self.cashStart)  # Set Strategy Cash
        # self.AddEquity("SPY", Resolution.Minute)
        self.Resolution = Resolution.Hour
        self.numHoldings = 0
        self.lotSize = 1000
        self.yesterday_total_profit = 0
        self.yesterday_total_fees = 0
        self.yesterday_total_value = self.cashStart
        self.dayHalt = False

        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage)
        self.currencies = {'GBPUSD':{},'EURUSD':{}, 'CADHKD':{}, 'GBPSGD':{}, 'USDJPY':{}}
        for currency in self.currencies:
            self.AddForex(currency, self.Resolution, Market.Oanda)
            self.currencies[currency]["BB"] = self.BB(currency, 20, 2, MovingAverageType.Simple, Resolution.Daily)
            
        self.SetWarmUp(20)
    
    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
        # self.lotSize = self.Portfolio.Cash*0.01
        for currency in self.currencies:
            self.dayHalt = self.get_daily_realized_pnl()<-0.05*self.Portfolio.TotalHoldingsValue
            # self.Debug(str(self.dayHalt))
            bb = self.currencies[currency]["BB"]
            props = self.currencies[currency]
            if not bb.IsReady or self.dayHalt:
                self.Liquidate()
                self.Debug(str(self.Portfolio.Keys))
                return
            
            # if (bb.PercentB.Current.Value == 0) and self.Securities[currency].Invested:
            #     self.Liquidate(currency)
            #     props['pos']=''
            if bb.PercentB.Current.Value >=0.95:
                if props.get("pos") == 'short':
                    self.Liquidate(currency)
                self.MarketOrder(currency, -self.lotSize)
                props['pos']='long'
            if bb.PercentB.Current.Value <=0.05:
                if props.get("pos") == 'long':
                    self.Liquidate(currency)
                self.MarketOrder(currency,self.lotSize)
                props['pos']='short'
        # if not self.Portfolio.Invested:
        #    self.SetHoldings("SPY", 1)
    def onOrderEvent(self,order):
        if order.Status == OrderStatus.Filled:
            close = order.FillPrice
            stopPrice = close * .99 
            limitPrice = close * 1.01 
            self.StopLimitOrder(order.Symbol, order.FillQuantity, stopPrice, limitPrice)
            
    def get_daily_realized_pnl(self):
        daily_gross_profit = self.Portfolio.TotalProfit - self.yesterday_total_profit
        daily_fees = self.Portfolio.TotalFees - self.yesterday_total_fees
        return daily_gross_profit - daily_fees
        
    def OnEndOfDay(self):
        # self.Liquidate()
        self.yesterday_total_profit = self.Portfolio.TotalProfit
        self.yesterday_total_fees = self.Portfolio.TotalFees
        self.yesterday_total_value = self.Portfolio.TotalHoldingsValue
        self.dayhalt = False
