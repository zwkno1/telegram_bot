#!/bin/bash

#/usr/lib/python3.6/site-packages/telegram/utils/request.py
#修改Request.__init__函數，去掉证书
#cert_reqs='CERT_REQUIRED',
#ca_certs=certifi.where(),

CURRENTDIR=$(pwd)

if [ ! -f "pytrie.so" ] ;  then
	mkdir build 
	cd build 
	cmake ../trie/pylib 
	make 
	cp pytrie.so ${CURRENTDIR} 
	rm -rf ${CURRENTDIR}/build
fi

cd ${CURRENTDIR}

HTTPS_PROXY="http://192.168.1.26:8087" ./bot.py >> bot.log 2>&1 &

