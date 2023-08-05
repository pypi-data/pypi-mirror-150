import requests
import json
import hashlib


def encrypt_string(hashing):
    sha = hashlib.sha256(hashing.encode()).hexdigest()
    return sha


class AliceblueAPI(object):
    # BASE_URL

    base_url = "http://a3.aliceblueonline.com/rest/AliceBlueAPIService/api/"
    api_name = "AliceBlue API - Python Lib "
    version = "1.0.1"

    # Products
    PRODUCT_INTRADAY = "MIS"
    PRODUCT_COVER_ODRER = "CO"
    PRODUCT_CNC = "CNC"
    PRODUCT_BRACKET_ORDER = "BO"
    PRODUCT_NRML = "NRML"

    # Order Type
    REGULAR_ORDER = "REGULAR"
    LIMIT_ORDER = "L"
    STOPLOSS_ORDER = "SL"
    MARKET_ORDER = "MKT"

    # Transaction type
    BUY_ORDER = "BUY"
    SELL_ORDER = "SELL"

    # Positions
    RETENTION_DAY = "DAY" or "NET"

    # Exchanges
    EXCHANGE_NSE = "NSE"
    EXCHANGE_NFO = "NFO"
    EXCHANGE_CDS = "CDS"
    EXCHANGE_BSE = "BSE"
    EXCHANGE_BFO = "BFO"
    EXCHANGE_BCD = "BCD"
    EXCHANGE_MCX = "MCX"

    # Status constants
    STATUS_COMPLETE = "COMPLETE"
    STATUS_REJECTED = "REJECTED"
    STATUS_CANCELLED = "CANCELLED"

    # response = requests.get(base_url);
    # Getscrip URI

    _sub_urls = {

        # Authorization

        "encryption_key": "customer/getAPIEncpkey",
        "getsessiondata": "customer/getUserSID",

        # Market Watch

        "marketwatch_scrips": "marketWatch/fetchMWScrips",
        "addscrips": "marketWatch/addScripToMW",
        "getmarketwatch_list": "marketWatch/fetchMWList",
        "scripdetails": "ScripDetails/getScripQuoteDetails",
        "getdelete_scrips": "marketWatch/deleteMWScrip",

        # OrderManagement

        "squareoffposition": "positionAndHoldings/sqrOofPosition",
        "position_conversion": "positionAndHoldings/positionConvertion",
        "placeorder": "placeOrder/executePlaceOrder",
        "modifyorder": "placeOrder/modifyOrder",
        "marketorder": "placeOrder/executePlaceOrder",
        "exitboorder": "placeOrder/exitBracketOrder",
        "bracketorder": "placeOrder/executePlaceOrder",
        "positiondata": "positionAndHoldings/positionBook",
        "orderbook": "placeOrder/fetchOrderBook",
        "tradebook": "placeOrder/fetchTradeBook",
        "holding": "positionAndHoldings/holdings",
        "orderhistory": "placeOrder/orderHistory",
        "cancelorder": "placeOrder/cancelOrder",

        # Funds

        "fundsrecord": "limits/getRmsLimits",

    }

    # Common Method
    def __init__(self,
                 user_id,
                 api_key,
                 base=None,
                 session_id=None,
                 disable_ssl=False):

        self.user_id = user_id
        self.api_key = api_key
        self.disable_ssl = disable_ssl
        self.session_id = session_id
        self.base = base or self.base_url

    def _get(self, sub_url, data=None):
        """Get method declaration"""
        url = self.base + self._sub_urls[sub_url]
        return self._request(url, "GET", data=data)

    def _post(self, sub_url, data=None):
        """Post method declaration"""
        url = self.base + self._sub_urls[sub_url]
        return self._request(url, "POST", data=data)

    def _dummypost(self, url, data=None):
        """Post method declaration"""
        return self._request(url, "POST", data=data)

    def _user_agent(self):
        return self.api_name + self.version

    """Authorization get to call all requests"""

    def _user_authorization(self):
        if self.session_id:
            return "Bearer " + self.user_id + " " + self.session_id
        else:
            return ""

    """Common request to call POST and GET method"""

    def _request(self, method, req_type, data=None):
        """
        Headers with authorization. For some requests authorization
        is not required. It will be send as empty String
        """
        _headers = {
            "X-SAS-Version": "2.0",
            "User-Agent": self._user_agent(),
            "Authorization": self._user_authorization(),

        }
        if req_type == "POST":
            response = requests.post(method, json=data, headers=_headers, )
            return json.loads(response.text)

        elif req_type == "GET":
            response = requests.get(method, json=data, headers=_headers)
            return json.loads(response.text)

    # Methods to call HTTP Request

    """Userlogin method with userid and userapi_key"""

    def getEncryptionKey(self, data=None):
        data = {'userId': self.user_id}
        response = self._post("encryption_key", data)
        if response['encKey'] is None:
            return response['emsg']
        else:
            data = encrypt_string(self.user_id + self.api_key + response['encKey'])
        data = {'userId': self.user_id, 'userData': data}
        res = self._post("getsessiondata", data)
        if res['stat'] == 'Ok':
            self.session_id = res['sessionID']
        return res

        """GET Market watchlist"""

    def getmarketwatch_list(self):
        marketwatchrespdata = self._get("getmarketwatch_list")
        return marketwatchrespdata

    """GET Tradebook Records"""

    def tradebook(self):
        tradebookresp = self._get("tradebook")
        return tradebookresp

    """GET Holdings Records"""

    def holdingsdata(self):
        holdingresp = self._get("holding")
        return holdingresp

    """GET Orderbook Records"""

    def order_data(self):
        orderresp = self._get("orderbook")
        return orderresp

    def order_history(self, nextorder):
        data = {'nestOrderNumber': nextorder}
        orderhistoryresp = self._post("orderhistory", data)
        return orderhistoryresp

    """Method to call Cancel Orders"""

    def cancel_order(self, exchange,
                     nestordernmbr,
                     tradingsymbol):
        data = {'exch': exchange,
                'nestOrderNumber': nestordernmbr,
                'trading_symbol': tradingsymbol}
        cancelresp = self._post("cancelorder", data)
        return cancelresp

    def marketwatch_scripsdata(self, mwname, ):
        data = {'mwName': mwname, }
        marketwatchresp = self._post("marketwatch_scrips", data)
        return marketwatchresp

    """Method to call Add Scrips"""

    def addscrips(self,
                  mwname,
                  exchange,
                  token):
        data = {'mwName': mwname,
                'exch': exchange,
                'symbol': token, }
        addscripsresp = self._post("addscrips", data)
        return addscripsresp

    """Method to call Delete Scrips"""

    def deletescrips(self,
                     mwname,
                     exchange,
                     token):
        data = {'mwName': mwname,
                'exch': exchange,
                'symbol': token, }
        deletescripsresp = self._post("getdelete_scrips", data)
        return deletescripsresp

    """Method to call Scrip Details"""

    def scrips_details(self,
                       exchange,
                       token):
        data = {'exch': exchange,
                'symbol': token}
        scripsdetailresp = self._post("scripdetails", data)
        return scripsdetailresp

    """Method to call Squareoff Positions"""

    def squareoff_positions(self,
                            exchange,
                            pCode,
                            qty,
                            tokenno,
                            symbol):
        data = {'exchSeg': exchange,
                'pCode': pCode,
                'netQty': qty,
                'tockenNo': tokenno,
                'symbol': symbol}
        squareoffresp = self._post("squareoffposition", data)
        return squareoffresp

    """Method to call  Place Order"""

    def place_order(self,
                    complexty,
                    discqty,
                    exch,
                    pCode,
                    price,
                    prctyp,
                    qty,
                    ret,
                    symbol_id,
                    trading_symbol,
                    transtype,
                    trigPrice):
        data = [{'complexty': complexty,
                 'discqty': discqty,
                 'exch': exch,
                 'pCode': pCode,
                 'price': price,
                 'prctyp': prctyp,
                 'qty': qty,
                 'ret': ret,
                 'symbol_id': symbol_id,
                 'trading_symbol': trading_symbol,
                 'transtype': transtype,
                 'trigPrice': trigPrice}]
        placeorderresp = self._post("placeorder", data)
        return placeorderresp

    """Method to call  Bracket Order"""

    def bracket_order(self,
                      complexty,
                      discqty,
                      exch,
                      pCode,
                      price,
                      prctyp,
                      qty,
                      ret,
                      stopLoss,
                      symbol_id,
                      target,
                      trailing_stop_loss,
                      trading_symbol,
                      transtype,
                      trigPrice):
        data = [{'complexty': complexty,
                 'discqty': discqty,
                 'exch': exch,
                 'pCode': pCode,
                 'price': price,
                 'prctyp': prctyp,
                 'qty': qty,
                 'ret': ret,
                 'target': target,
                 'stopLoss': stopLoss,
                 'trailing_stop_loss': trailing_stop_loss,
                 'symbol_id': symbol_id,
                 'trading_symbol': trading_symbol,
                 'transtype': transtype,
                 'trigPrice': trigPrice}]
        bracketorderresp = self._post("bracketorder", data)
        return bracketorderresp

    """Method to get Funds Data"""

    def fundsdata(self):
        fundsresp = self._get("fundsrecord")
        return fundsresp

    """Method to call Modify Order"""

    def modifyorder(self,
                    discqty,
                    exch,
                    filledQuantity,
                    nestOrderNumber,
                    prctyp,
                    price,
                    qty,
                    trading_symbol,
                    trigPrice,
                    transtype,
                    pCode):
        data = {'discqty': discqty,
                'exch': exch,
                'filledQuantity': filledQuantity,
                'nestOrderNumber': nestOrderNumber,
                'prctyp': prctyp,
                'price': price,
                'qty': qty,
                'trading_symbol': trading_symbol,
                'trigPrice': trigPrice,
                'transtype': transtype,
                'pCode': pCode}
        modifyorderresp = self._post("modifyorder", data)
        return modifyorderresp

    """Method to call Market Order"""

    def marketorder(self,
                    complexty,
                    discqty,
                    exch,
                    pCode,
                    prctyp,
                    price,
                    qty,
                    ret,
                    symbol_id,
                    trading_symbol,
                    transtype,
                    trigPrice):
        data = [{'complexty': complexty,
                 'discqty': discqty,
                 'exch': exch,
                 'pCode': pCode,
                 'prctyp': prctyp,
                 'price': price,
                 'qty': qty,
                 'ret': ret,
                 'symbol_id': symbol_id,
                 'trading_symbol': trading_symbol,
                 'transtype': transtype,
                 'trigPrice': trigPrice}]
        marketorderresp = self._post("marketorder", data)
        return marketorderresp

    """Method to call Exitbook  Order"""

    def exitboorder(self,
                    nestOrderNumber,
                    symbolOrderId,
                    status, ):
        data = {'nestOrderNumber': nestOrderNumber,
                'symbolOrderId': symbolOrderId,
                'status': status, }
        exitboorderresp = self._post("exitboorder", data)
        return exitboorderresp

    """Method to get Position Book"""

    def positionbook(self,
                     ret, ):
        data = {'ret': ret, }
        positionbookresp = self._post("positiondata", data)
        return positionbookresp

    """Method to get Scripsforsearch"""

    def get_scrips(self, symbol, exchange):
        scrip_Url = "http://a3.aliceblueonline.com/rest/AliceBlueAPIService/exchange/getScripForSearch"
        data = {'symbol': symbol, 'exchange': exchange}
        scrip_response = self._dummypost(scrip_Url, data)
        return scrip_response
