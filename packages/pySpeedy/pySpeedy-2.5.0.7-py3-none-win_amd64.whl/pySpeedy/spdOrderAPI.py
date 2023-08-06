# -*- coding: cp950 -*-
##
# 類別 : spdOrderAPI
# 作者 : Allen Lee, Simon Chang
# 功能 : spdOrderAPI連接Speedy Order Server.提供對台灣交易所TWSE/OTC/TAIFEX交易的支援.

## @cond DEV
#----------------------------------------------------------------------------
import ctypes, platform, os
#----------------------------------------------------------------------------
if platform.system() == 'Windows':
    print('----- spdOrderAPI detect : Windows platform -----')
    print('Load['+os.path.dirname(__file__) + '\pySpeedyAPI_64.dll'+']')
    libSpeedy = ctypes.cdll.LoadLibrary( os.path.dirname(__file__) +  '\pySpeedyAPI_64.dll')
elif platform.system() == 'Linux':
    print('----- spdOrderAPI detect : Linux platform -----')
    print('Load['+os.path.dirname(__file__) + '\pySpeedyAPI_64.so'+']')
    libSpeedy = ctypes.cdll.LoadLibrary(os.path.dirname(__file__) + '\pySpeedyAPI_64.so')
#----------------------------------------------------------------------------
#
# prepare for class spdOrderAPI define
#
#----------------------------------------------------------------------------
def spdOrderDummyFun():
    pass
#----------------------------------------------------------------------------
# Declare the callback type
## \hiderefby
Def_pyOrderOnConnected        = ctypes.CFUNCTYPE(None)
## \hiderefby
Def_pyOrderOnDisconnected     = ctypes.CFUNCTYPE(None)
## \hiderefby
Def_pyOrderOnLogonResponse    = ctypes.CFUNCTYPE(None, ctypes.c_bool, ctypes.c_wchar_p)
## \hiderefby
Def_pyOrderOnReplyNewOrder    = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_double, ctypes.c_wchar_p
                                                     , ctypes.c_long, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p)
## \hiderefby
Def_pyOrderOnReplyCancelOrder = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_double, ctypes.c_wchar_p, ctypes.c_wchar_p)
## \hiderefby
Def_pyOrderOnReplyReplaceOrder = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_double, ctypes.c_wchar_p
                                                     , ctypes.c_long, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p)
## \hiderefby
Def_pyOnRejectOrder           = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p )
## \hiderefby
Def_pyOnFill                  = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_long, ctypes.c_double, ctypes.c_long, ctypes.c_wchar_p)
# Keep "life cycle" of events function pointer to prevent "access violation"
gOrderFunPtr_OnConnected        = spdOrderDummyFun
gOrderFunPtr_OnDisconnected     = spdOrderDummyFun
gOrderFunPtr_OnLogonResponse    = spdOrderDummyFun
gOrderFunPtr_OnReplyNewOrder    = spdOrderDummyFun
gOrderFunPtr_OnReplyCancelOrder = spdOrderDummyFun
gOrderFunPtr_OnReplyReplaceOrder = spdOrderDummyFun
gOrderFunPtr_OnRejectOrder      = spdOrderDummyFun
gOrderFunPtr_OnFill             = spdOrderDummyFun

## @endcond
#----------------------------------------------------------------------------
#
# class spdOrderAPI
#
#----------------------------------------------------------------------------
class spdOrderAPI():
    #------------------------------------------------------------------------
    # Functions
    #------------------------------------------------------------------------
    # 建構式中會宣告C對應在Python中的函數原形.
    # 並宣告對應C的callback function.並註冊給C的模組. 
    # @param self 物件本身 
    def __init__(self):
        # Functions definition
        # Constructor
        libSpeedy.pyOrderAdapter_New.argtypes = []
        libSpeedy.pyOrderAdapter_New.restype = ctypes.c_void_p
        # Delete
        libSpeedy.pyOrderAdapter_Delete.argtypes = [ctypes.c_void_p]
        libSpeedy.pyOrderAdapter_Delete.restype = None
        # IsConnected()
        libSpeedy.pyOrderAdapter_IsConnected.argtypes = [ctypes.c_void_p]
        libSpeedy.pyOrderAdapter_IsConnected.restype = ctypes.c_bool
        # Connect()
        libSpeedy.pyOrderAdapter_Connect.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        libSpeedy.pyOrderAdapter_Connect.restype = None
        # Logon()
        libSpeedy.pyOrderAdapter_Logon.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_Logon.restype = None
        # LogonProxy()
        libSpeedy.pyOrderAdapter_LogonProxy.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_LogonProxy.restype = None
        # SetAccount()
        libSpeedy.pyOrderAdapter_SetAccount.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_SetAccount.restype = None
        # Disconnect()
        libSpeedy.pyOrderAdapter_Disconnect.argtypes = [ctypes.c_void_p]
        libSpeedy.pyOrderAdapter_Disconnect.restype = None
        # SendNewOrder()
        libSpeedy.pyOrderAdapter_SendNewOrder.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double,
                                                          ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_SendNewOrder.restype = ctypes.c_int
        # SendCancelOrder()
        libSpeedy.pyOrderAdapter_SendCancelOrder.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                                                             ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_SendCancelOrder.restype = ctypes.c_int
        # SendReplaceOrder()
        libSpeedy.pyOrderAdapter_SendReplaceOrder.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p,
                                                           ctypes.c_double, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
        libSpeedy.pyOrderAdapter_SendReplaceOrder.restype = ctypes.c_int
        # RegEvents()
        libSpeedy.pyOrderAdapter_RegEvents.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                                                       ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        libSpeedy.pyOrderAdapter_RegEvents.restype = None

        libdir = os.path.dirname(__file__) 
        CurDir = os.path.abspath(os.getcwd())
        
        # Create pyOrderAdapter object
        os.chdir( libdir )        
        self.Obj = libSpeedy.pyOrderAdapter_New()
        os.chdir( CurDir )
        print("Package install directory: {0}".format(libdir))
        print("Current working directory: {0}".format(CurDir))

        # Keep "life cycle" of events function
        global gOrderFunPtr_OnConnected, gOrderFunPtr_OnDisconnected, gOrderFunPtr_OnLogonResponse, gOrderFunPtr_OnReplyNewOrder
        global gOrderFunPtr_OnReplyCancelOrder, gOrderFunPtr_OnReplyReplaceOrder, gOrderFunPtr_OnRejectOrder, gOrderFunPtr_OnFill
        # Binding events
        gOrderFunPtr_OnConnected         = Def_pyOrderOnConnected(self.OnConnected)
        gOrderFunPtr_OnDisconnected      = Def_pyOrderOnDisconnected(self.OnDisconnected)
        gOrderFunPtr_OnLogonResponse     = Def_pyOrderOnLogonResponse(self.OnLogonResponse)
        gOrderFunPtr_OnReplyNewOrder     = Def_pyOrderOnReplyNewOrder(self.OnReplyNewOrder)
        gOrderFunPtr_OnReplyCancelOrder  = Def_pyOrderOnReplyCancelOrder(self.OnReplyCancelOrder)
        gOrderFunPtr_OnReplyReplaceOrder = Def_pyOrderOnReplyReplaceOrder(self.OnReplyReplaceOrder)
        gOrderFunPtr_OnRejectOrder       = Def_pyOnRejectOrder(self.OnRejectOrder)
        gOrderFunPtr_OnFill              = Def_pyOnFill(self.OnFill)
        # Register events to C/C++
        libSpeedy.pyOrderAdapter_RegEvents(self.Obj, gOrderFunPtr_OnConnected, gOrderFunPtr_OnDisconnected, gOrderFunPtr_OnLogonResponse, gOrderFunPtr_OnReplyNewOrder,
                                           gOrderFunPtr_OnReplyCancelOrder, gOrderFunPtr_OnReplyReplaceOrder, gOrderFunPtr_OnRejectOrder, gOrderFunPtr_OnFill)
    
    ##連線至Speedy下單主機
    # @param self	物件本身
    # @param IP	下單主機IP
    # @param Port	下單主機Port
    # @param TimeoutSec	設定連線逾時秒數 
    def Connect(self, IP, Port, TimeoutSec):
        libSpeedy.pyOrderAdapter_Connect(self.Obj, IP.encode(), Port, TimeoutSec)
        
    ## 下單主機是否連線 
    # @param self 物件本身 
    # @return TRUE 表示連線成功,FALSE 斷線.		                                         
    def IsConnected(self):
        return libSpeedy.pyOrderAdapter_IsConnected(self.Obj)
        
    ## 登入Speedy下單主機. 
    # @param self 物件本身 .
    # @param ID	Speedy登入帳號.
    # @param Password	Speedy帳號的密碼.
    # @param Account	交易帳號.
    def Logon(self, ID, Password, Account):
        libSpeedy.pyOrderAdapter_Logon(self.Obj, ID.encode(), Password.encode(), Account.encode())
    
    ## 登入Speedy Proxy下單主機 
    # @param self 物件本身 		
    # @param ID	主機帳號 
    # @param Password 主機帳號的密碼
    # @param Account交易帳號       
    #
    def LogonProxy(self, ID, Password, Account):
        libSpeedy.pyOrderAdapter_LogonProxy(self.Obj, ID.encode(), Password.encode(), Account.encode())
    
    ## 設定交易帳號 
    # @param self 物件本身 	
    # @param Exchange	交易所  ※需為大寫字母 
    #| 交易所   | 代碼     |
    #| ----:    |  :----   |
    #| 證交所   | 'TWSE'   |
    #| 櫃買中心 | 'OTC'    |
    #| 期交所   | 'TAIFEX' |
    # @param BrokerID	券商或期商代號
    # @param Account	交易帳號
    #
    def SetAccount(self, Exchange, BrokerID, Account):
        libSpeedy.pyOrderAdapter_SetAccount(self.Obj, Exchange.encode(), BrokerID.encode(), Account.encode())
        
    ## 與下單主機斷線 
    # @param self 物件本身 	
    def Disconnect(self):
        libSpeedy.pyOrderAdapter_Disconnect(self.Obj)
        
    ## 傳送新單指令    
    # @param self 物件本身.
    # @param Market	市場別  ※需為小寫字母.
    #| 市場別   | 代碼   |
    #| ----:    |  :---- |
    #| 集中市場 | 'tse'  |
    #| 櫃買市場 | 'otc'  |
    #| 期貨市場 | 'fut'  |
    #| 選擇權   | 'opt'  |
    # @param UDD 使用者運用的字串, 在以下Event 發生時會帶回, OnReplyNewOrder, OnRejectOrder, OnFill, 長度:128以內.
    # @param Symbol 商品代碼
    # @param Price 價格
    # @param Side 買賣別, ‘B’:Buy, ‘S’:Sell, ※需為大寫字母.
    # @param OrderQty 委託數量
    # @param OrderType 委託方式. ※需為大寫字母.
    #| 代碼 | 說明   |
    #| ----:|  :---- |
    #| 'L'  | Limit order, 限價單.  |
    #| 'M'  | Market order, 市價單.  |
    #| 'P'  | Market with protection, 一定範圍市價單,僅期交所支援. |
    # @param TimeInForce 委託條件 ‘R’:ROD, ‘I’:IOC, ‘F’:FOK, ※需為大寫字母.
    # @param TWSEOrdType TWSE/OTC Order type. 
    #| 代碼 | 說明   |
    #| ----:|  :---- |
    #| '0'  | regular trading Via Securities Finance.  |
    #| '1'  | Purchase on Margin.  |
    #| '2'  | Short Sell. Via Securities Firms conduct Margin Lending.  |
    #| '3'  | Purchase on Margin.  |
    #| '4'  | Short Sell.  |
    #| '5'  | SBL Short Sell type 5  |
    #| '6'  | SBL Short Sell type 5  |
    # @return NID 當日唯一的ID,收到新單回報時請透過NID對應回原單, 若NID回0表示帶入欄位有誤 
    #
    def SendNewOrder(self, Market, UDD, Symbol, Price, Side, OrderQty, OrderType, TimeInForce, TWSEOrdType ):
        return libSpeedy.pyOrderAdapter_SendNewOrder(self.Obj, Market.encode(), UDD.encode(), Symbol.encode(), Price,
                                                     Side.encode(), OrderQty, OrderType.encode(), TimeInForce.encode(), TWSEOrdType.encode())
    ## 送出刪單指令 
    # @param self	物件本身.
    # @param Market	市場別  ※需為小寫字母.
    #| 市場別   | 代碼   |
    #| ----:    |  :---- |
    #| 集中市場 | 'tse'  |
    #| 櫃買市場 | 'otc'  |
    #| 期貨市場 | 'fut'  |
    #| 選擇權   | 'opt'  |
    # @param UDD	使用者運用的字串, 在以下Event 發生時會帶回, OnReplyNewOrder, OnRejectOrder, OnFill, 長度:128以內.
    # @param Symbol	商品代碼
    # @param Price	價格
    # @param Side	買賣別, ‘B’:Buy, ‘S’:Sell, ※需為大寫字母.
    # @param OrderID	交易所端單號 
    # @return NID 當日唯一的ID,收到刪單回報時請透過NID對應回原委託單, 若NID回0表示帶入欄位有誤.
    #
    def SendCancelOrder(self, Market, UDD, Symbol, Price, Side, OrderID):
        return libSpeedy.pyOrderAdapter_SendCancelOrder(self.Obj, Market.encode(), UDD.encode(), Symbol.encode(), Price, Side.encode(), OrderID.encode())

    ## 送出改單指令 
    # @param self	物件本身.
    # @param Market	市場別  ※需為小寫字母.
    #| 市場別   | 代碼   |
    #| ----:    |  :---- |
    #| 集中市場 | 'tse'  |
    #| 櫃買市場 | 'otc'  |
    #| 期貨市場 | 'fut'  |
    #| 選擇權   | 'opt'  |
    # @param UDD	使用者運用的字串, 在以下Event 發生時會帶回, OnReplyNewOrder, OnRejectOrder, OnFill, 長度:128以內.
    # @param Symbol	商品代碼
    # @param OrderID	改單的交易所端單號
    # @param Side	買賣別, ‘B’:Buy, ‘S’:Sell, ※需為大寫字母.
    # @param Price	價格 欲改價的價錢(減量時填0)
    # @param OrderQty	委託數量 欲減的量(改價時填0)
    # @param OrderType	委託方式, ※需為大寫字母.
    #| 代碼 | 說明   |
    #| ----:|  :---- |
    #| 'L'  | Limit order, 限價單.  |
    #| 'M'  | Market order, 市價單.  |
    #| 'P'  | Market with protection, 一定範圍市價單,僅期交所支援. |
    # @param TimeInForce	委託條件 ‘R’:ROD, ‘I’:IOC, ‘F’:FOK, ※需為大寫字母.
    # @return NID 當日唯一的ID,收到改單回報時請透過NID對應回原委託單, 若NID回0表示帶入欄位有誤.
    #
    def SendReplaceOrder(self, Market, UDD, Symbol, OrderID, Side, Price, OrderQty, OrderType, TimeInForce):
        return libSpeedy.pyOrderAdapter_SendReplaceOrder(self.Obj, Market.encode(), UDD.encode(), Symbol.encode(), OrderID.encode(), Side.encode(), Price,
                                                      OrderQty, OrderType.encode(), TimeInForce.encode())        
    #------------------------------------------------------------------------
    # Events
    # inheritance spdOrderAPI & implement
    #------------------------------------------------------------------------
    ## 連線成功的 Event
    # @param self 物件本身.
    def OnConnected(self):
        pass

    ## 發生斷線的 Event
    # @param self 物件本身.
    def OnDisconnected(self):
        pass

    ## 登入結果回覆的 Event 
    # @param self  物件本身.
    # @param IsSucceed	是否成功.  True:成功 False:失敗 
    # @param ReplyString Server回復的登入訊息 
    def OnLogonResponse(self, IsSucceed, ReplyString):
        pass

    ## Event 新單回報     
    # @param self	物件本身.
    # @param NID	網路單號
    # @param UDD	SendNewOrder所帶之User Define Data
    # @param Symbol	商品代碼
    # @param Price	價格
    # @param Side	買賣別‘B’:Buy ‘S’:Sell
    # @param OrderQty	委託數量
    # @param OrderType	委託方式
    #| 代碼 | 說明   |
    #| ----:|  :---- |
    #| 'L'  | Limit order, 限價單.  |
    #| 'M'  | Market order, 市價單.  |
    #| 'P'  | Market with protection, 一定範圍市價單,僅期交所支援. |
    # @param TimeInForce	委託條件‘R’:ROD,‘I’:IOC,‘F’:FOK
    # @param OrderID	交易所端單號 
    def OnReplyNewOrder(self, NID, UDD, Symbol, Price, Side, OrderQty, OrderType, TimeInForce, OrderID):
        pass

    ## Event 刪單回報
    # @param self	物件本身.
    # @param NID	網路單號
    # @param UDD	SendCancelOrder所帶之User Define Data
    # @param Symbol	商品代碼
    # @param Price	價格
    # @param Side	買賣別‘B’:Buy ‘S’:Sell
    # @param OrderID	交易所端單號 
    def OnReplyCancelOrder(self, NID, UDD, Symbol, Price, Side, OrderID):
        pass

    ## Event 改單回報 
    # @param self	物件本身.
    # @param NID	網路單號
    # @param UDD	SendNewOrder所帶之User Define Data
    # @param Symbol	商品代碼
    # @param Price	改價後的價錢(改量時為0)
    # @param Side	買賣別‘B’:Buy ‘S’:Sell
    # @param OrderQty	改量後的量(改價時為0)
    # @param OrderType	委託方式
    #| 代碼 | 說明   |
    #| ----:|  :---- |
    #| 'L'  | Limit order, 限價單.  |
    #| 'M'  | Market order, 市價單.  |
    #| 'P'  | Market with protection, 一定範圍市價單,僅期交所支援. |
    # @param TimeInForce	委託條件‘R’:ROD,‘I’:IOC,‘F’:FOK
    # @param OrderID	交易所端單號 
    def OnReplyReplaceOrder(self, NID, UDD, Symbol, Price, Side, OrderQty, OrderType, TimeInForce, OrderID):
        pass

    ## Event  委託失敗回報 
    # @param self	物件本身.
    # @param NID	網路單號
    # @param UDD	SendNewOrder 或 SendCancelOrder 或 SendReplaceOrder 所帶之User Define Data.
    # @param ActionFrom	委託失敗類別 'N':Reject New Order,‘C’:Reject Cancel Order,‘R’: Reject Replace Order
    # @param ErrCode	錯誤代號
    # @param ErrMsg	錯誤訊息 
    def OnRejectOrder(self, NID, UDD, ActionFrom, ErrCode, ErrMsg):
        pass

    ## Event 成交回報
    # @param self	物件本身.
    # @param NID	網路單號
    # @param UDD	SendNewOrder所帶之User Define Data
    # @param OrderID	交易所端單號
    # @param ReportSequence	回報序號
    # @param FillPrice	成交價錢
    # @param FillQty	成交量
    # @param FillTime	成交時間 證交所:HHMMSSmm, 期交所:HHMMSSmmm 
    def OnFill(self, NID, UDD, OrderID, ReportSequence, FillPrice, FillQty, FillTime):
        pass
#----------------------------------------------------------------------------

