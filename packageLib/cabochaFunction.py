#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import CaboCha
from lxml import etree as lxml
from bs4 import BeautifulSoup

"""
	グローバル変数
"""
SRL = {u"SubjectHa":u"", u"SubjectGa":u"", u"ObjectNi":u"", u"ObjectWo":u""}

"""
	sentenceタグにIDを付与
"""
def addSentenceID(xmlStr, idx):
	parseXML = lxml.fromstring(xmlStr)
	parseXML.xpath('//sentence')[0].set('id', str(idx))
	return lxml.tostring(parseXML, encoding="utf-8")

"""
	sentenceタグに文章のタイプを付与
		ト書き(stageDirections)	「」なし
		台詞(speech)　			「」あり
"""
def addSentenceStructureType(xmlStr, sentStr):
	parseXML = lxml.fromstring(xmlStr)
	structType = ""
	if not re.search(u"「*.」" , sentStr) is None:
		structType = u"speech"
	else :
		structType = u"stageDirections"
	parseXML.xpath('//sentence')[0].set('structure', structType)
	return lxml.tostring(parseXML, encoding="utf-8")

"""
	係り受け解析をする
"""
def makePumpkinCake(sentList):
	plist = []
	c = CaboCha.Parser()
	for i, nimono in enumerate(sentList):
		tree = c.parse(nimono.encode('utf-8'))
		xmlData = addSentenceID(tree.toString(CaboCha.FORMAT_XML), i)
		a = addSentenceStructureType(xmlData, nimono)
		plist.append(a)
	return plist

"""
	・助詞[は][が]を判定
"""
def isWaGa(xmlStr):
	flag = False
	tokenList = xmlStr.find_all('tok')
	for tokenItem in tokenList:
		if tokenItem.attrs['feature'].split(',')[0] == u"助詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"係助詞" and \
		  	tokenItem.text == u"は":
			flag = True
		elif tokenItem.attrs['feature'].split(',')[0] == u"助詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"格助詞" and \
			tokenItem.text == u"が":
		  	flag = True
	return flag

"""
	・名詞-一般or名詞-固有名詞の単語が存在するか
"""
def isCharacter(xmlStr):
	flag = False
	tokenList = xmlStr.find_all('tok')
	for tokenItem in tokenList:
		if tokenItem.attrs['feature'].split(',')[0] == u"名詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"一般":
			flag = True
		elif tokenItem.attrs['feature'].split(',')[0] == u"名詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"固有名詞":
		  	flag = True
	return flag	


"""
	・名詞-一般or名詞-固有名詞の単語を取得する
"""
def getCharacter(xmlStr):
	actor = ""
	tokenList = xmlStr.find_all('tok')
	for tokenItem in tokenList:
		if tokenItem.attrs['feature'].split(',')[0] == u"名詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"一般":
			actor = tokenItem.string
		elif tokenItem.attrs['feature'].split(',')[0] == u"名詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"固有名詞":
		  	actor = tokenItem.string
	return actor

"""
	小説内の登場人物
	・助詞[は][が]を判定
	・名詞-一般or名詞-固有名詞の単語が存在するか
"""
def getActor(pumpList):
	actorList = []
	for sentItem in pumpList:
		soup = BeautifulSoup(sentItem)
 		chunkList = soup.find_all('chunk')
 		for chunkItem in chunkList:
			if isWaGa(chunkItem):
				if isCharacter(chunkItem):
					contents = getCharacter(chunkItem)
					if not contents in actorList:
						actorList.append(contents)
	return actorList

"""
	省略された主語・目的語を補う

"""
def supportNoun(pumpkinCake, sentenceList, actorList):
	outputList = []
	for nimono in pumpkinCake:
		parseXML = lxml.fromstring(nimono)
		if parseXML.xpath('//sentence')[0].attrib['structure'] == u"stageDirections":
					pass

	return outputList