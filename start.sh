#!/bin/bash

#/usr/lib/python3.6/site-packages/telegram/utils/request.py
#修改Request.__init__函數，去掉证书
#cert_reqs='CERT_REQUIRED',
#ca_certs=certifi.where(),
HTTPS_PROXY="http://192.168.1.26:8087" ./bot.py

