from AlgorithmImports import *

class MACDTrendAlgorithm(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        #Set Start Date
        self.SetStartDate(2018, 1, 1)
        #Set End Date
        #self.SetEndDate(2018, 1, 1)
        #Set Strategy Cash
        self.SetCash(100000)             
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage)
        # Find more symbols here: http://quantconnect.com/data
        self.instrument = "ACN"
        #self.AddCrypto(self.instrument, Resolution.Hour, Market.GDAX)
        self.AddEquity("ACN", Resolution.Daily)

        # define our daily macd(12,26) with a 9 day signal
        self.__macd = self.MACD(self.instrument, 12, 26, 9, MovingAverageType.Simple, Resolution.Daily)
        self.__previous = datetime.min
        
        # create a bollinger band
        self.Bolband = self.BB(self.instrument, 20, 2, MovingAverageType.Simple, Resolution.Daily)




        
    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        # wait for our macd to fully initialize
        if not self.__macd.IsReady: return

        # only once per day
        if self.__previous.date() == self.Time.date(): return

        # define a small tolerance on our checks to avoid bouncing
        tolerance = 0.0025

        holdings = self.Portfolio[self.instrument].Quantity

        signalDeltaPercent = (self.__macd.Current.Value - self.__macd.Signal.Current.Value)/self.__macd.Fast.Current.Value
        self.Debug(self.__macd.Current.Value)
        self.Debug(self.__macd.Signal.Current.Value)
        self.Debug("----")
        
                
        price = self.Securities[self.instrument].Close
        # of our macd is less than our signal, then let's go short
        bbMid = self.Bolband.MiddleBand.Current.Value
        bbLow = self.Bolband.LowerBand.Current.Value
        
        # if our macd is greater than our signal, then let's go long
        # if closing price hits below bband, buy
        if holdings <= 0 and (signalDeltaPercent > tolerance or price > bbLow):  # 0.01%
            # longterm says buy as well
            self.SetHoldings(self.instrument, 1.0)

        elif holdings >= 0 and (signalDeltaPercent < -tolerance or price < bbMid):
            if price < bbMid:
                self.Debug("Hit BB, exiting")
            if self.Portfolio[self.instrument].Invested:
                self.Liquidate(self.instrument)


        self.__previous = self.Time
