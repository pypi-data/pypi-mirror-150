from thefirstock.execution import *

from enum import Enum
from typing import List, Optional
from datetime import date, datetime

from thefirstock.pyClient import Client
from thefirstock.pyClient.utils.encoders import date_encoder
from thefirstock.pyClient.utils.encoders import password_hash_encoder
from pydantic import BaseModel, IPvAnyAddress, EmailStr, SecretStr, root_validator
from thefirstock.pyClient.utils.decoders import build_loader, timestamp_decoder, datetime_decoder

API_URL = r'https://norenapi.thefirstock.com/NorenWClientTP/'
SOCKET_URL = r'wss://norenapi.thefirstock.com/NorenWSTP/'

try:
    client = Client(api_url=API_URL, socket_url=SOCKET_URL)
except Exception as e:
    print(e)


class ResponseStatus(str, Enum):
    OK = 'Ok'
    NOT_OK = 'Not_Ok'


class LoginRequestModel(BaseModel):
    apkversion: Optional[str] = "1.0.0"

    uid: str

    pwd: Optional[SecretStr]

    dpin: Optional[SecretStr]

    factor2: str

    vc: str

    appkey: str

    imei: Optional[str] = "12345"

    addldivinf: Optional[str]

    ipaddr: Optional[IPvAnyAddress]

    source: Optional[str] = "API"

    @root_validator(allow_reuse=True)
    def validate(cls, values: dict):
        pwd_is_present = values.get('pwd') is not None
        dpin_is_present = values.get('dpin') is not None
        valid = pwd_is_present or dpin_is_present
        if not valid:
            raise ValueError('Either pwd or dpin should be present')
        return values

    class Config:
        json_encoders = {
            date: date_encoder(),
            SecretStr: password_hash_encoder()
        }


class LoginResponseModel(BaseModel):
    stat: ResponseStatus = ResponseStatus.OK

    susertoken: Optional[str]

    lastaccesstime: Optional[datetime]

    request_time: Optional[datetime]

    spasswordreset: Optional[str]

    exarr: Optional[List[str]]

    uname: Optional[str]

    actid: Optional[str]

    email: Optional[EmailStr]

    brkname: Optional[str]

    emsg: Optional[str]

    class Config:
        json_loads = build_loader({
            "lastaccesstime": timestamp_decoder(),
            "request_time": datetime_decoder()
        })


def webSocketLogin():
    with open("config.json") as file:
        data = json.load(file)

    result = data["webSocketLogin"]
    credentials = LoginResponseModel.parse_raw(result)
    client.login(credentials)

    return client


def firstock_login(uid, pwd, factor2, vc, appkey):
    try:
        login = FirstockLogin(
            uid=uid,
            pwd=pwd,
            factor2=factor2,
            vc=vc,
            appkey=appkey,
        )

        result = login.firstockLogin()

        return result

    except Exception as e:
        print(e)


def firstock_userDetails():
    try:

        clientDetails = FirstockClientDetails().firstockClientDetails()
        return clientDetails

    except Exception as e:
        print(e)


def firstock_logout():
    try:

        logout = FirstockLogout().firstockLogout()
        return logout

    except Exception as e:
        print(e)


def firstock_placeOrder(exch, tsym, qty, prc, prd, trantype, prctyp, ret, trgprc):
    try:
        placeOrder = FirstockPlaceOrder(
            exch=exch,
            tsym=tsym,
            qty=qty,
            prc=prc,
            prd=prd,
            trantype=trantype,
            prctyp=prctyp,
            ret=ret,
            trgprc=trgprc
        ).firstockPlaceOrder()

        return placeOrder
    except Exception as e:
        print(e)


def firstock_orderMargin(exch, tsym, qty, prc, prd, trantype, prctyp):
    try:
        orderMargin = FirstockGetOrderMargin(
            exch=exch,
            tsym=tsym,
            qty=qty,
            prc=prc,
            prd=prd,
            trantype=trantype,
            prctyp=prctyp,
        ).firstockGetOrderMargin()

        return orderMargin

    except Exception as e:
        print(e)


def firstock_orderBook():
    try:
        orderBook = FirstockOrderBook().firstockOrderBook()

        return orderBook

    except Exception as e:
        print(e)


def firstock_cancelOrder(norenordno):
    try:
        cancelOrder = FirstockCancelOrder(
            norenordno=norenordno
        ).firstockCancelOrder()

        return cancelOrder

    except Exception as e:
        print(e)


def firstock_ModifyOrder(qty, norenordno, trgprc, prc):
    try:

        modifyOrder = FirstockModifyOrder(
            qty=qty,
            norenordno=norenordno,
            trgprc=trgprc,
            prc=prc
        ).firstockModifyOrder()

        return modifyOrder

    except Exception as e:
        print(e)


def firstock_SingleOrderHistory(norenordno):
    try:
        singleOrderHistory = FirstockSingleOrderHistory(
            norenordno=norenordno
        ).firstockSingleOrderHistory()

        return singleOrderHistory

    except Exception as e:
        print(e)


def firstock_TradeBook():
    try:

        tradeBook = FirstockTradeBook().firstockTradeBook()

        return tradeBook

    except Exception as e:
        print(e)


def firstock_PositionBook():
    try:

        positionBook = FirstockPositionBook().firstockPositionBook()

        return positionBook

    except Exception as e:
        print(e)


def firstock_ConvertProduct(exch, tsym, qty, prd, prevprd, trantype, postype):
    try:

        convertProduct = FirstockConvertProduct(
            exch=exch,
            tsym=tsym,
            qty=qty,
            prd=prd,
            prevprd=prevprd,
            trantype=trantype,
            postype=postype
        ).firstockConvertProduct()

        return convertProduct

    except Exception as e:
        print(e)


def firstock_Holding():
    try:

        holding = FirstockHoldings().firstockHoldings()

        return holding

    except Exception as e:
        print(e)


def firstock_Limits():
    try:

        limits = FirstockLimits().firstockLimits()

        return limits

    except Exception as e:
        print(e)


def firstock_GetQuotes(exch, token):
    try:
        getQuotes = FirstockGetQuotes(
            exch=exch,
            token=token
        ).firstockGetQuotes()

        return getQuotes

    except Exception as e:
        print(e)


def firstock_SearchScrips(stext):
    try:

        searchScrips = FirstockSearchScrips(
            stext=stext
        ).firstockSearchScrips()

        return searchScrips

    except Exception as e:
        print(e)


def firstock_SecurityInfo(exch, token):
    try:

        securityInfo = FirstockGetSecurityInfo(
            exch=exch,
            token=token
        ).firstockGetSecurityInfo()

        return securityInfo

    except Exception as e:
        print(e)


def firstock_IndexList(exch):
    try:

        indexList = FirstockGetIndexList(
            exch=exch
        ).firstockGetIndexList()

        return indexList

    except Exception as e:
        print(e)


def firstock_OptionChain(tsym, exch, strprc, cnt):
    try:

        optionChain = FirstockGetOptionChain(
            tsym=tsym,
            exch=exch,
            strprc=strprc,
            cnt=cnt
        ).firstockGetOptionChain()

        return optionChain

    except Exception as e:
        print(e)


def firstock_SpanCalculator(exch, instname, symname, expd, optt, strprc, netqty, buyqty, sellqty):
    try:

        spanCalculator = FirstockSpanCalculator(
            exch=exch,
            instname=instname,
            symname=symname,
            expd=expd,
            optt=optt,
            strprc=strprc,
            netqty=netqty,
            buyqty=buyqty,
            sellqty=sellqty
        ).firstockSpanCalculator()

        return spanCalculator

    except Exception as e:
        print(e)


def firstock_TimePriceSeries(exch, token, et, st):
    try:

        timePrice = FirstockTimePriceSeries(
            exch=exch,
            token=token,
            et=et,
            st=st
        ).firstockTimePriceSeries()

        return timePrice

    except Exception as e:
        print(e)
