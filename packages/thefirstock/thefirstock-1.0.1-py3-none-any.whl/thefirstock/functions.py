import ast
import json
import requests

from thefirstock.base import *
from .operations.apiOperations import *

from .Variables.enums import *
from .Variables.fixedParams import *


class ApiRequests(FirstockAPI):
    def firstockLogin(self, uid: str, pwd: str, factor2: str, vc: str, appkey: str):
        """
        :return: The json response
        """
        try:
            encryptedPassword = encodePwd(pwd)

            keyGenerator = generateKey(uid, appkey)
            apiKey = encodePwd(keyGenerator)
            url = LOGIN

            payload = {
                "apkversion": APKVERSION,
                "uid": uid,
                "pwd": encryptedPassword.hexdigest(),
                "factor2": factor2,
                "imei": IMEI,
                "source": SOURCE,
                "vc": vc,
                "appkey": apiKey.hexdigest()
            }
            jsonPayload = json.dumps(payload)

            result = requests.post(url, f'jData={jsonPayload}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            if finalResult["stat"] == "Ok":
                dictionary = {
                    "uid": uid,
                    "factor2": factor2,
                    "vc": vc,
                    "jKey": finalResult["susertoken"],
                    "webSocketLogin": jsonString
                }

                jsonObject = json.dumps(dictionary, indent=4)

                with open("config.json", "w") as outfile:
                    outfile.write(jsonObject)

                return jsonString

            else:
                return jsonString

        except Exception as e:
            print(e)

    def firstockClientDetails(self):
        """
        :return:
        """
        try:
            url = USERDETAILS
            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockLogout(self):
        """
        :return:
        """
        url = LOGOUT

        with open("config.json") as file:
            data = json.load(file)

        uid = data["uid"]
        jKey = data["jKey"]

        payload = {
            "uid": uid
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockPlaceOrder(self, exch, tsym, qty, prc, prd, trantype, prctyp, ret, trgprc):
        """
        :return:
        """
        url = PLACEORDER

        with open("config.json") as file:
            data = json.load(file)

        uid = data["uid"]
        jKey = data["jKey"]

        payload = {
            "uid": uid,
            "actid": uid,
            "exch": exch,
            "tsym": tsym,
            "qty": qty,
            "prc": prc,
            "prd": prd,
            "trantype": trantype,
            "prctyp": prctyp,
            "ret": ret,
            "trgprc": trgprc
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockGetOrderMargin(self, exch, tsym, qty, prc, prd, trantype, prctyp):
        """
        :return:
        """
        try:
            url = ORDERMARGIN

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "actid": uid,
                "exch": exch,
                "tsym": tsym,
                "qty": qty,
                "prc": prc,
                "prd": prd,
                "trantype": trantype,
                "prctyp": prctyp,
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockOrderBook(self):
        """
        :return:
        """
        try:
            url = ORDERBOOK

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockCancelOrder(self, norenordno):
        """
        :return:
        """
        try:
            url = CANCELORDER

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "norenordno": norenordno
            }

            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockModifyOrder(self, qty, norenordno, trgprc, prc):
        """
        :return:
        """
        try:
            url = MODIFYORDER

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "norenordno": norenordno,
                "qty": qty,
                "prc": prc,
                "trgprc": trgprc
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockSingleOrderHistory(self, norenordno):
        """
        :return:
        """
        try:
            url = SINGLEORDERHISTORY

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "norenordno": norenordno,
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockTradeBook(self):
        """
        :return:
        """
        try:
            url = TRADEBOOK

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "actid": uid,
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockPositionBook(self):
        """
        :return:
        """
        try:

            url = POSITIONBOOK

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "actid": uid,
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockConvertProduct(self, exch, tsym, qty, prd, prevprd, trantype, postype):
        """
        :return:
        """
        try:
            url = PRODUCTCONVERSION

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "exch": exch,
                "tsym": tsym,
                "qty": qty,
                "actid": uid,
                "prd": prd,
                "prevprd": prevprd,
                "trantype": trantype,
                "postype": postype
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockHoldings(self):
        """
        :return:
        """
        try:
            url = HOLDINGS

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "actid": uid,
                "prd": "C",
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockLimits(self):
        """
        :return:
        """
        try:

            url = LIMITS

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "actid": uid,
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockGetQuotes(self, exch, token):
        """
        :return:
        """
        try:
            url = GETQUOTES

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "exch": exch,
                "token": token
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockSearchScrips(self, stext):
        """
        :return:
        """
        try:
            url = SEARCHSCRIPS

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "stext": stext
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockGetSecurityInfo(self, exch, token):
        """
        :return:
        """
        try:
            url = GETSECURITYINFO

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "exch": exch,
                "token": token
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockGetIndexList(self, exch):
        """
        :return:
        """
        try:
            url = GETINDEXLIST

            with open("config.json") as file:
                data = json.load(file)

            uid = data["uid"]
            jKey = data["jKey"]

            payload = {
                "uid": uid,
                "exch": exch
            }
            jsonPayload = json.dumps(payload)
            result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
            jsonString = result.content.decode("utf-8")

            finalResult = ast.literal_eval(jsonString)

            return finalResult

        except Exception as e:
            print(e)

    def firstockGetOptionChain(self, tsym, exch, strprc, cnt):
        """
        :return:
        """
        url = GETOPTIONCHAIN

        with open("config.json") as file:
            data = json.load(file)

        uid = data["uid"]
        jKey = data["jKey"]

        payload = {
            "uid": uid,
            "exch": exch,
            "tsym": tsym,
            "strprc": strprc,
            "cnt": cnt
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockSpanCalculator(self, exch, instname, symname, expd, optt, strprc, netqty, buyqty, sellqty):
        """
        :return:
        """
        url = SPANCALCULATOR

        with open("config.json") as file:
            data = json.load(file)

        uid = data["uid"]
        jKey = data["jKey"]

        payload = {
            "actid": uid,
            "exch": exch,
            "instname": instname,
            "symname": symname,
            "expd": expd,
            "optt": optt,
            "strprc": strprc,
            "netqty": netqty,
            "buyqty": buyqty,
            "sellqty": sellqty
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockTimePriceSeries(self, exch, token, et, st):
        """
        :return:
        """
        url = TIMEPRICESERIES

        with open("config.json") as file:
            data = json.load(file)

        uid = data["uid"]
        jKey = data["jKey"]

        payload = {
            "uid": uid,
            "exch": exch,
            "token": token,
            "et": et,
            "st": st
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult
