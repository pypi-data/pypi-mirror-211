# -*- coding: cp950 -*-
##  @brief 
#  類別 : spdQuoteAPI
#  作者 : Allen Lee, Simon Chang
#  功能 : spdQuoteAPI 連接StarWave Marketdata Server.
#         提供對台灣交易所TWSE/OTC/TAIFEX行情的支援
#----------------------------------------------------------------------------
import ctypes, platform, os
## @cond  
class spdContract(ctypes.Structure):
    _fields_ = [('BullPx', ctypes.c_double), 
                ('BearPx', ctypes.c_double), 
                ('RefPx', ctypes.c_double), 
                ('ContractMultiplier', ctypes.c_double),
                ('StrikePx', ctypes.c_double), #for Options                
                ('Market', ctypes.c_int),
                ('TradeUnit', ctypes.c_int),
                ('DayTrade', ctypes.c_int),
                ('WarningStock', ctypes.c_int),
                ('TradeFlag', ctypes.c_bool),             
                ('IsWarrant', ctypes.c_bool),             
                ('CallPut', ctypes.c_char)] #for Options
## @endcond      
class ContractInfo:
    ## 商品基本資料類別建構式.        
    def __init__(self,Ex,Sym,Name,MMD, ProdID, Info ):
        ## 交易所名稱(TWSE,OTC,TAIFEX...) 
        self.Exchange = Ex 
        ## 商品名稱.例如 證券:2330 期貨:TXFF3
        self.Symbol = Sym 
        ## 商品顯示名稱. 例如 台積電
        self.DisplayName = Name 
        ## 期貨商品結算年月 YYYYMM
        self.MaturityDate = MMD
        ## 商品類別.例如 證券:17(金融保險); 期貨:TXF 
        self.Category =  ProdID
        ## 漲停價
        self.BullPx = Info.BullPx
        ## 跌停價
        self.BearPx = Info.BearPx
        ## 參考價
        self.RefPx = Info.RefPx
        ## 契約成數.例 TXF一點 200 
        self.ContractMultiplier = Info.ContractMultiplier
        ## 選擇權商品履約價
        self.StrikePx = Info.StrikePx
        ## 市場別. 下單時使用 'fut':期貨, 'opt':選擇權, 'tse':集中市場(證交所), 'otc':櫃買市場(OTC)          
        if Info.Market ==  0:
            self.Market = 'fut'
        elif Info.Market ==  1:
            self.Market = 'opt'
        elif Info.Market ==  2:
            self.Market = 'tse'
        elif Info.Market ==  3:
            self.Market = 'otc'
        elif Info.Market ==  4:
            self.Market = 'ffut'
        elif Info.Market ==  5:
            self.Market = 'fopt'
        else:
            self.Market = 'unknown'
        ## 交易單位. 例 股票一張是1000股 
        self.TradeUnit = Info.TradeUnit
        ## 商品是否可交易 1:是 0:否
        self.TradeFlag = Info.TradeFlag        
        ## 當沖註記. 'Yes'表示為可先買後賣或先賣後買現股當沖證券，'OnlyBuy' 表示為可先買後賣現股當沖證券. 'No'表示為不可現股當沖證券。
        self.DayTrade = 'Yes'  
        ## 是不是權證商品
        self.IsWarrant = Info.IsWarrant
        ## 警示股代碼. 0—正常 1—注意 2—處置 3—注意及處置 4—再次處置 5—注意及再次處置 6—彈性處置 7—注意及彈性處置
        self.WarringStock = Info.WarningStock  
        ## 'Call' 表示是call的選擇權,'Put'表示是Put的選擇權.'None'表示非選擇權商品        
        if Info.CallPut == 'C':
            self.CallPut = 'Call'
        elif  Info.CallPut == 'P':
            self.CallPut = 'Put'
        else:
            self.CallPut = 'None'
    ## 印出商品基本資料.   
    def Print(self):
        print( '----- [{0}][{1}] -----'.format(self.Exchange, self.Symbol))            
        print( 'Exchange[{0}] '.format(self.Exchange))            
        print( 'Symbol[{0}] '.format(self.Symbol))            
        print( 'Market[{0}] '.format(self.Market))            
        print( 'DisplayName[{0}] '.format(self.DisplayName))            
        print( 'Category[{0}] '.format(self.Category))            
        print( 'BullPx[{0}] '.format(self.BullPx))            
        print( 'BearPx[{0}] '.format(self.BearPx))            
        print( 'RefPx[{0}] '.format(self.RefPx))            
        if self.Market ==  'fut': # TAIFEX Taiwan Futures
            print( 'ContractMultiplier[{0}] '.format(self.ContractMultiplier))            
            print( 'MaturityDate[{0}] '.format(self.MaturityDate))    
            print( 'CallPut[{0}] '.format(self.CallPut))            
            print( 'StrikePx[{0}] '.format(self.StrikePx))            
            print( '----- TW Futures -----' )
        elif  self.Market ==  'opt': # TAIFEX Taiwan Options
            print( 'ContractMultiplier[{0}] '.format(self.ContractMultiplier))            
            print( 'MaturityDate[{0}] '.format(self.MaturityDate))            
            print( 'CallPut[{0}] '.format(self.CallPut))            
            print( 'StrikePx[{0}] '.format(self.StrikePx))            
            print( '----- TW Options -----' )
        elif  self.Market ==  'tse': # TWSE Taiwan equity
            print( 'TradeUnit[{0}] '.format(self.TradeUnit))            
            print( 'DayTrade[{0}] '.format(self.DayTrade))            
            print( 'WarringStock[{0}] '.format(self.WarringStock))            
            print( 'IsWarrant[{0}] '.format(self.IsWarrant))            
            print( '----- TWSE Stocks -----' )
        elif  self.Market ==  'otc': # OTC Taiwan over the counter
            print( 'TradeUnit[{0}] '.format(self.TradeUnit))            
            print( 'DayTrade[{0}] '.format(self.DayTrade))            
            print( 'WarringStock[{0}] '.format(self.WarringStock))            
            print( 'IsWarrant[{0}] '.format(self.IsWarrant))            
            print( '------ OTC Stocks -----' )
        else:
            print( 'TradeUnit[{0}] '.format(self.TradeUnit))            


#----------------------------------------------------------------------------
#
# prepare for class spdQuoteAPI define
#
#----------------------------------------------------------------------------
class spdMsgOrderBook(ctypes.Structure):
    ## 委託簿更新資料 
    # @param BidPrice1~BidPrice5	最佳買一到買五價
    # @param BidQty1~BidQty5	最佳買一到買五量
    # @param AskPrice1~AskPrice5	最佳賣一到賣五價
    # @param AskQty1~AskQty5	最佳賣一到賣五量
    # @param DerivedBidPrice	衍生Bid價格.(僅期交所提供)
    # @param DerivedBidQty	衍生Bid數量.(僅期交所提供)
    # @param DerivedAskPrice	衍生Ask價格.(僅期交所提供)
    # @param DerivedAskQty	衍生Ask數量.(僅期交所提供)
    # @param 說明	Derived Bid Ask 最佳虛擬一檔只會出現在期貨及選擇權商品， 為使未成交之ROD（Rest of day）跨月價差委託得留存於系統， 將視個別可撮合成交月份之最佳一檔委託價量，衍生虛擬委託至該跨月價差委託所屬之另一月份委託簿中。 故原個別月份除原單式委託最佳五檔買賣價量外，尚會再多揭露最佳一檔由跨月價差委託衍生之單式委託買賣價量。 該資訊由期交所提供。
    _fields_ = [('BidPrice1', ctypes.c_double), 
                ('BidPrice2', ctypes.c_double), 
                ('BidPrice3', ctypes.c_double), 
                ('BidPrice4', ctypes.c_double),
                ('BidPrice5', ctypes.c_double),
                ('BidQty1', ctypes.c_int), 
                ('BidQty2', ctypes.c_int), 
                ('BidQty3', ctypes.c_int), 
                ('BidQty4', ctypes.c_int), 
                ('BidQty5', ctypes.c_int),
                ('AskPrice1', ctypes.c_double), 
                ('AskPrice2', ctypes.c_double), 
                ('AskPrice3', ctypes.c_double), 
                ('AskPrice4', ctypes.c_double), 
                ('AskPrice5', ctypes.c_double),
                ('AskQty1', ctypes.c_int), 
                ('AskQty2', ctypes.c_int), 
                ('AskQty3', ctypes.c_int), 
                ('AskQty4', ctypes.c_int), 
                ('AskQty5', ctypes.c_int),
                ('DerivedBidPrice', ctypes.c_double),
                ('DerivedBidQty', ctypes.c_int), 
                ('DerivedAskPrice', ctypes.c_double), 
                ('DerivedAskQty', ctypes.c_int)]
                
## @cond                                 
#----------------------------------------------------------------------------
if platform.system() == 'Windows':
    print('\n----- spdQuoteAPI detect : Windows platform -----')
    print('Load['+os.path.dirname(__file__) + '\pySpeedyAPI_64.dll'+']')
    libSpeedy = ctypes.cdll.LoadLibrary( os.path.dirname(__file__) + '\pySpeedyAPI_64.dll')
elif platform.system() == 'Linux':
    print('\n----- spdQuoteAPI detect : Linux platform -----')
    print('Load['+os.path.dirname(__file__) + '\pySpeedyAPI_64.so'+']')
    libSpeedy = ctypes.cdll.LoadLibrary( os.path.dirname(__file__) + '\pySpeedyAPI_64.so')
#----------------------------------------------------------------------------
def spdQuoteDummyFun():
    pass
#----------------------------------------------------------------------------
# Declare the callback type
Def_pyQuoteOnConnected     = ctypes.CFUNCTYPE(None)
Def_pyQuoteOnDisconnected  = ctypes.CFUNCTYPE(None)
Def_pyQuoteOnLogonResponse =  ctypes.CFUNCTYPE(None, ctypes.c_bool, ctypes.c_wchar_p)
Def_pyQuoteOnContract = ctypes.CFUNCTYPE(None,  ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p,ctypes.POINTER(spdContract))
Def_pyQuoteOnContractDownloadComplete = ctypes.CFUNCTYPE(None, ctypes.c_int)
Def_pyQuoteOnOrderBook     = ctypes.CFUNCTYPE(None, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.POINTER(spdMsgOrderBook))
Def_pyQuoteOnTrade         = ctypes.CFUNCTYPE(None, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_double, ctypes.c_int)
# Keep "life cycle" of events function pointer to prevent "access violation"
gQuoteFunPtr_OnConnected     = spdQuoteDummyFun
gQuoteFunPtr_OnDisconnected  = spdQuoteDummyFun
gQuoteFunPtr_OnLogonResponse = spdQuoteDummyFun
gQuoteFunPtr_OnContract      = spdQuoteDummyFun
gQuoteFunPtr_OnComplete      = spdQuoteDummyFun
gQuoteFunPtr_OnOrderBook     = spdQuoteDummyFun
gQuoteFunPtr_OnTrade         = spdQuoteDummyFun
## @endcond
#----------------------------------------------------------------------------
#
# class spdQuoteAPI
#
#----------------------------------------------------------------------------
class spdQuoteAPI(object):    
    #------------------------------------------------------------------------
    # -- Functions --
    #------------------------------------------------------------------------
    ## 建構式中會宣告C對應在Python中的函數原形.
    #  並宣告對應C的callback function.並註冊給C的模組.     
    # @param self 物件本身 
    def __init__(self):
        # Functions definition
        # Constructor
        libSpeedy.pyQuoteAdapter_New.argtypes = []
        libSpeedy.pyQuoteAdapter_New.restype = ctypes.c_void_p
        # Delete
        libSpeedy.pyQuoteAdapter_Delete.argtypes = [ctypes.c_void_p]
        libSpeedy.pyQuoteAdapter_Delete.restype = None
        # IsConnected()
        libSpeedy.pyQuoteAdapter_IsConnected.argtypes = [ctypes.c_void_p]
        libSpeedy.pyQuoteAdapter_IsConnected.restype = ctypes.c_bool
        # Logon()
        libSpeedy.pyQuoteAdapter_Logon.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,ctypes.c_bool]
        libSpeedy.pyQuoteAdapter_Logon.restype = None
        # Subscribe()
        libSpeedy.pyQuoteAdapter_Subscribe.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyQuoteAdapter_Subscribe.restype = ctypes.c_bool
        # DownloadContracts()
        libSpeedy.pyQuoteAdapter_DownloadContracts.argtypes = [ctypes.c_void_p]
        libSpeedy.pyQuoteAdapter_DownloadContracts.restype = None
        # RegEvents()
        libSpeedy.pyQuoteAdapter_RegEvents.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        libSpeedy.pyQuoteAdapter_RegEvents.restype = None
        
        # Create pyQuoteAdapter object        
        ## 保留原生API的Handle
        self.Obj = libSpeedy.pyQuoteAdapter_New()
        ## 股票商品基本資料Dictionary.
        self.Stocks = {}
        ## 期貨商品基本資料Dictionary.
        self.Futures = {}
        ## 選擇權商品基本資料Dictionary.
        self.Options = {}
        
        # Keep "life cycle" of events function
        global gQuoteFunPtr_OnConnected, gQuoteFunPtr_OnDisconnected, gQuoteFunPtr_OnLogonResponse, gQuoteFunPtr_OnContract, gQuoteFunPtr_OnComplete, gQuoteFunPtr_OnOrderBook, gQuoteFunPtr_OnTrade
        # Binding events
        gQuoteFunPtr_OnConnected    = Def_pyQuoteOnConnected(self.OnConnected)
        gQuoteFunPtr_OnDisconnected = Def_pyQuoteOnDisconnected(self.OnDisconnected)
        gQuoteFunPtr_OnLogonResponse= Def_pyQuoteOnLogonResponse(self.OnLogonResponse) 
        gQuoteFunPtr_OnContract     = Def_pyQuoteOnContract( self.__OnContract )    
        gQuoteFunPtr_OnComplete     = Def_pyQuoteOnContractDownloadComplete( self.__OnComplete )   
        gQuoteFunPtr_OnOrderBook    = Def_pyQuoteOnOrderBook(self.__OnOrderBook)
        gQuoteFunPtr_OnTrade        = Def_pyQuoteOnTrade(self.OnTrade)
        # Register events to C/C++
        libSpeedy.pyQuoteAdapter_RegEvents(self.Obj, gQuoteFunPtr_OnConnected, gQuoteFunPtr_OnDisconnected, gQuoteFunPtr_OnLogonResponse, gQuoteFunPtr_OnContract, gQuoteFunPtr_OnComplete, gQuoteFunPtr_OnOrderBook, gQuoteFunPtr_OnTrade)
    
    ## 行情主機是否連線 
    # @param self 物件本身 
    # @return TRUE 表示連線成功,FALSE 斷線. .		
    def IsConnected(self):
        return libSpeedy.pyQuoteAdapter_IsConnected(self.Obj)

    ## 連線登入StarWave行情主機.     
    # @param self	物件本身.
    # @param IP	行情主機IP
    # @param Port	行情主機Port
    # @param ID	StarWave登入帳號.
    # @param DownloadContracts 登入成功後是否自動下載商品基本資料.也可以登入成功後,主動呼叫DownloadContracts().
    # @param Password	StarWave帳號的密碼. 
    def Logon(self, IP, Port,ID,Password,DownloadContracts):        
        libSpeedy.pyQuoteAdapter_Logon(self.Obj, IP.encode(), Port, ID.encode(), Password.encode(), DownloadContracts )
    
    ## 訂閱商品行情 
    # 例如 訂閱台積電行情可以呼叫 ObjQuote.Subscribe( 'TWSE', '2330' )
    # @param Exchange 交易所
    #| 交易所   | 代碼     |
    #| ----:    |  :----   |
    #| 證交所   | 'TWSE'   |
    #| 櫃買中心 | 'OTC'    |
    #| 期交所   | 'TAIFEX' |
    # @param Symbol	 商品代碼
    # @return TRUE 表示訂閱成功,FALSE表示訂閱失敗.超過訂閱數上限.		
    def Subscribe(self, Exchange, Symbol):
        return libSpeedy.pyQuoteAdapter_Subscribe(self.Obj, Exchange.encode(), Symbol.encode())

    ## 用商品基本資料物件訂閱行情 
    # 例如 訂閱台積電行情可以呼叫 ObjQuote.SubscribeContract( ObjQuote.Stocks['2330'] )
    # @param Contract 商品基本資料的物件.    
    # @return TRUE 表示訂閱成功,FALSE表示訂閱失敗.超過訂閱數上限.		
    def SubscribeContract(self, Contract ):
        return libSpeedy.pyQuoteAdapter_Subscribe(self.Obj, Contract.Exchange.encode(), Contract.Symbol.encode())
     
    ## 要求下載商品基本資料
    # 當下載完成時 OnContractDownloadComplete 事件會被呼叫.   
    def DownloadContracts(self):
        return libSpeedy.pyQuoteAdapter_DownloadContracts(self.Obj )

    ## 解構式
    def __del__(self):
        pass
    #------------------------------------------------------------------------
    # -- Events --
    # inheritance spdQuoteAPI & implement
    #------------------------------------------------------------------------
## @cond                                 
    def __OnOrderBook(self, Exchange, Symbol, MsgTime, Msg):
        self.OnOrderBook(Exchange, Symbol, MsgTime, Msg[0])
        pass    

    def __OnContract(self, Ex, Sym, Name,MaturityDate, Category, Info ):        
        NewContract = ContractInfo( Ex, Sym, Name,MaturityDate, Category, Info[0] )
        if Info[0].Market ==  0:    # TAIFEX Taiwan Futures
           self.Futures[ Sym ] =  NewContract
        elif  Info[0].Market ==  1: # TAIFEX Taiwan Options
           self.Options[ Sym ] =  NewContract
        else:                       # TWSE/OTC Taiwan Stocks
           self.Stocks[ Sym ] =  NewContract
        pass

    def __OnComplete(self, Contracts ):
        print( 'Total Contract Count [{0}] '.format(Contracts))                    
        self.OnContractDownloadComplete()
        pass
## @endcond
    ## 連線完成的Event 
    # @param self 物件本身. 
    def OnConnected(self):
        pass

    ## Event 發生斷線 
    # @param self 物件本身. 
    def OnDisconnected(self):
        pass

    ## 登入結果回覆的Event 
    # @param self 物件本身. 
    # @param IsSucceed	是否成功 True:成功 False:失敗 
    # @param ReplyString 登入訊息 
    def OnLogonResponse(self, IsSucceed, ReplyString):
        pass     
    
    ## 通知商品基本資料下載完成的Event ,之後可以用Stocks,Futures,Options這幾個Dictionary取到商品基本資料
    # @param self 物件本身. 
    def OnContractDownloadComplete(self):        
        pass

    ## Event 委託簿更新
    # @param self 物件本身. 
    # @param Exchange 交易所
    #| 交易所   | 代碼     |
    #| ----:    |  :----   |
    #| 證交所   | 'TWSE'   |
    #| 櫃買中心 | 'OTC'    |
    #| 期交所   | 'TAIFEX' |
    # @param Symbol 商品代碼 
    # @param MsgTime 資料時間 格式為 HH:MM:SS.mmm 
    # @param Msg 五檔行情資料 structure為 class spdMsgOrderBook 
    def OnOrderBook(self, Exchange, Symbol, MsgTime, Msg):
        pass

    ## Event 成交信息 
    # @param self 物件本身. 
    # @param Exchange 交易所 
    #| 交易所   | 代碼     |
    #| ----:    |  :----   |
    #| 證交所   | 'TWSE'   |
    #| 櫃買中心 | 'OTC'    |
    #| 期交所   | 'TAIFEX' |
    # @param Symbol	商品代碼 		
    # @param MatchTime	成交時間 格式為 HH:MM:SS.mmm 
    # @param MatchPrice	成交價格
    # @param MatchQty	成交數量
    def OnTrade(self, Exchange, Symbol, MatchTime, MatchPrice, MatchQty):
        pass
#----------------------------------------------------------------------------
