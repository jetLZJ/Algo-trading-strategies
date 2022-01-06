from AlgorithmImports import *

class MACDTrendAlgorithm(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        #Set Start Date
        self.SetStartDate(2015, 1, 1)
        #Set End Date
        self.SetEndDate(2018, 1, 1)
        #Set Strategy Cash
        self.SetCash(100000)             
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage)
        self.__previous = datetime.min
        self.__numberOfSymbols = 5
        self.stateData = { }
        self._changes = None
        
        # define our daily macd(12,26) with a 9 day signal
        #self.__macd = self.MACD(self.instrument, 12, 26, 9, MovingAverageType.Simple, Resolution.Daily)
        self.__previous = datetime.min
        
        # create a bollinger band
        #self.Bolband = self.BB(self.instrument, 20, 2, MovingAverageType.Simple, Resolution.Daily)

        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)
        
        
    def CoarseSelectionFunction(self, coarse):
        self.stateData = { }
        # We are going to use a dictionary to refer the object that will keep the moving averages
        for c in coarse:
            if c.Symbol not in self.stateData:
                self.stateData[c.Symbol] = SelectionData(c.Symbol)

            # Updates the SymbolData object with current EOD price
            avg = self.stateData[c.Symbol]
            avg.update(c.EndTime, c.AdjustedPrice, c.DollarVolume)
        values = [x for x in self.stateData.values()]
        
        # sort by the largest in volume.
        values.sort(key=lambda x: x.volume, reverse=True)

        # we need to return only the symbol objects
        return [ x.symbol for x in values[:self.__numberOfSymbols]]
    

        
    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        # wait for our macd to fully initialize
        
        # only once per day
        if self.__previous.date() == self.Time.date(): return
    
        self.Log(f"OnData({self.UtcTime}): Keys: {', '.join([key.Value for key in data.Keys])}")
        # if we have no changes, do nothing
        if self._changes is None: return
        
        
        self.Log(f"OnData({self.UtcTime}): Keys: {', '.join([key.Value for key in data.Keys])}")
        # if we have no changes, do nothing
        if self._changes is None: return

        for security in self._changes.RemovedSecurities:
            if security.Invested:
                self.Liquidate(security.Symbol)

        for security in self._changes.AddedSecurities:
            stock = security.Symbol
            stockUptrend = self.stateData[stock].is_uptrend
            signalDeltaPercent = ((self.stateData[stock].fast.Current.Value - self.stateData[stock].slow.Current.Value) - self.stateData[stock].signal.Current.Value)/self.stateData[stock].fast.Current.Value
            # define a small tolerance on our checks to avoid bouncing
            tolerance = 0.0025
            holdings = self.Portfolio[stock].Quantity
            
    
            #stockBB = self.stateData[stock].Bolband
            #if not stockMACD.IsReady: return
           
           
            # only once per day
            if self.__previous.date() == self.Time.date(): return
            #price = self.Securities[stock].Close
            # of our macd is less than our signal, then let's go short
            #bbMid = stockBB.MiddleBand.Current.Value
           # bbLow = stockBB.LowerBand.Current.Value
            
            # if our macd is greater than our signal, then let's go long
            # if closing price hits below bband, buy
            #if holdings <= 0 and (signalDeltaPercent > tolerance or price > bbLow):  # 0.01%
            # longterm says buy as well
            if holdings <= 0 and (signalDeltaPercent > tolerance):
                self.SetHoldings(stock, 1.0/self.__numberOfSymbols)
    
            elif holdings >= 0 and (signalDeltaPercent < -tolerance):
                self.Liquidate(stock)
    
    
        self.__previous = self.Time
        self._changes = None
        
                # this event fires whenever we have changes to our universe
    def OnSecuritiesChanged(self, changes):
        self._changes = changes
        self.Log(f"OnSecuritiesChanged({self.UtcTime}):: {changes}")

    def OnOrderEvent(self, fill):
        self.Log(f"OnOrderEvent({self.UtcTime}):: {fill}")
    

class SelectionData(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.tolerance = 1.01
        self.fast = ExponentialMovingAverage(12)
        self.slow = ExponentialMovingAverage(26)
        self.signal = ExponentialMovingAverage(9)
        self.macd = self.fast.Current.Value - self.slow.Current.Value
        self.volume = 0

    def update(self, time, value, volume):
        if self.fast.Update(time, value) and self.slow.Update(time, value) and self.signal.Update(time, value):
            fast = self.fast.Current.Value
            slow = self.slow.Current.Value
            signal = self.signal.Current.Value
            self.volume = volume
            self.macd = fast - slow
