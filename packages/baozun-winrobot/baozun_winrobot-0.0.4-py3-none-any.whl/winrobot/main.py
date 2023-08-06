import logging; logging.basicConfig(level=logging.INFO)
import requests;
from requests.cookies import RequestsCookieJar;
from config.tmall import TMALL_DEFAULT_HEADERS;

def get_coupon_info(cookie_list = []):
  url = "https://shell.mkt.taobao.com/coupon/getActivityInfo"
  payload = "{\"id\":\"5907348532\",\"queryDetail\":\"true\",\"couponType\":\"0\"}"
  cookie_jar = RequestsCookieJar()
  for cookie_item in cookie_list:
    cookie_jar.set(cookie_item['name'], cookie_item['value'], domain=cookie_item['domain'])
  response = requests.request("POST", url, headers=TMALL_DEFAULT_HEADERS, data=payload, cookies=cookie_jar)
  return response.text
