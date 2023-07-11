import matplotlib.pyplot as plt
import numpy as np
from binance.client import Client
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.patches as patches
from matplotlib.colors import to_rgba as c2rgba
import math
import hashlib
import time
import os
import telegram
import json
import os.path

bot = telegram.Bot(token='593263828:AAGZrzPMQoEwGDD2SjVGI1FnZWcE9SRAhXA')

# BINANCE EXCHANGE

apikey = 'pCTr6213prwdxYzgCp61Cc6CXsc9RkbMRmwmvSgreyLxDEPzAs6zUIPdXYF4OPfd' # API KEY
apisecret = 'tVhTxUao7sOZ7owS8Ty9RMEpLrdKIVM7tqEZxGSXEVBU61cQgUtRqNvj1ppEWeFf' # API SECRET
client = Client(apikey,apisecret)

def zigzag(highs, lows, dates, minPercent):

	length = min(len(highs), len(lows), len(dates))

	zigzag = np.zeros(length)

	trend = None

	lastHigh = None

	lastLow = None

	for i in range(length):

		if trend == None:

			if highs[i] >= lows[0] * (1 + minPercent):

				trend = "Bull"

				lastHigh = i

				zigzag[0] = -1

			if lows[i] <= highs[0] * (1 - minPercent):

				trend = "Bear"

				lastLow = i

				zigzag[0] = 1

		if trend == "Bull":

			if lows[i] <= highs[lastHigh] * (1 - minPercent) and highs[i] < highs[lastHigh]:

				trend = "Bear"

				zigzag[lastHigh] = 1

				lastLow = i

			if highs[i] > highs[lastHigh]:

				lastHigh = i

		if trend == "Bear":

			if highs[i] >= lows[lastLow] * (1 + minPercent) and lows[i] > lows[lastLow]:

				trend = "Bull"

				zigzag[lastLow] = -1

				lastHigh = i

			if lows[i] < lows[lastLow]:

				lastLow = i

	lastTrend = 0

	lastTrendIndex = 0

	for i in range(len(zigzag) - 1, -1, -1):

		if zigzag[i] != 0:

			lastTrend = zigzag[i]

			lastTrendIndex = i

			break

	determinant = 0

	highDeterminant = highs[lastTrendIndex]

	lowDeterminant = lows[lastTrendIndex]

	for i in range(lastTrendIndex+1, length):

		if lastTrend == 1:

			if lows[i] < lowDeterminant:

				lowDeterminant = lows[i]

				determinant = i

		if lastTrend == -1:

			if highs[i] > highDeterminant:

				highDeterminant = highs[i]

				determinant = i

	if lastTrend == 1:

		zigzag[determinant] = -1

	if lastTrend == -1:

		zigzag[determinant] = 1

	out = []

	for i in range(length):

		if zigzag[i] == 1:

			out.append([dates[i], highs[i]])

		if zigzag[i] == -1:

			out.append([dates[i], lows[i]])

	return np.array(out)

def products_creator(use_market = ['BTC', 'ETH', 'USDT']):

	products = client.get_products()

	if len(use_market) == 0:

		use_market = ['BTC', 'ETH', 'USDT']

	products = [products['data'][i]['symbol'] for i in range(len(products['data'])) if products['data'][i]['status'] == 'TRADING']

	products = [i for i in products if (i[::-1][:4:][::-1] == "TUSD" if "TUSD" in use_market else False) or 
			(i[::-1][:3:][::-1] == "PAX" if "PAX" in use_market else False) or
			(i[::-1][:4:][::-1] == "USDC" if "USDC" in use_market else False) or
			(i[::-1][:4:][::-1] == "USDS" if "USDS" in use_market else False) or
			(i[::-1][:3:][::-1] == "BNB" if "BNB" in use_market else False) or
			(i[::-1][:3:][::-1] == "XRP" if "XRP" in use_market else False) or
			(i[::-1][:3:][::-1] == "BTC" if "BTC" in use_market else False) or
			(i[::-1][:3:][::-1] == "ETH" if "ETH" in use_market else False) or
			(i[::-1][:4:][::-1] == "USDT" if "USDT" in use_market else False)]

	return products

def e2_str_norm(number):

	if not 'e' in str(number):

		return str(number)

	else:

		main = '0.'

		for i in range(len(str(number)[::-1])):

			if str(number)[::-1][i] == '-':

				i = i

				break

		zero_amount = int(str(number)[-i:]) - 1

		for i in range(zero_amount):

			main += '0'

		for i in range(len(str(number)[::-1])):

			if str(number)[i] == 'e':

				i = i

				break

		for i in range(i):

			if str(number)[i] != '.':

				main += str(number)[i]

		return main

def format_value(val, step_size_str):

	def step_size_to_precision(ss):
		return ss.find('1') - 1

	precision = step_size_to_precision(step_size_str)
	if precision > 0:
		return float("{:0.0{}f}".format(val, precision))
	return math.floor(int(val))

def harmonic_pattern_finding(xtrmpoints, deviation, deviationD, pair, close, showPotential, blurryPatterns):

	patterns = {}

	used = np.array([])

	info = client.get_symbol_info(pair)

	ticksize = info['filters'][0]['tickSize']

	pesavento_numbers = [0.146, 0.236, 0.382, 0.447, 0.5, 0.618, 0.707, 0.786, 0.841, 0.886, 1.0, 1.128, 1.272, 1.414, 1.5, 1.618, 1.732, 1.902, 2.0, 2.236, 2.414, 2.618, 3.14, 3.618, 4.0]

	XABCD_patterns = [{'pattern': 'new cypher', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 1.414, 'maxAC': 2.14, 'minBD': 1.128, 'maxBD': 2.0, 'minXD': 0.786, 'maxXD': 0.786},
	{'pattern': 'anti new cypher', 'minXB': 0.5, 'maxXB': 0.886, 'minAC': 0.467, 'maxAC': 0.707, 'minBD': 1.618, 'maxBD': 2.618, 'minXD': 1.272, 'maxXD': 1.272},
	{'pattern': 'ideal gartley', 'minXB': 0.618, 'maxXB': 0.618, 'minAC': 0.618, 'maxAC': 0.618, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': 0.786, 'maxXD': 0.786},
	{'pattern': 'ideal gartley', 'minXB': 0.618, 'maxXB': 0.618, 'minAC': 0.618, 'maxAC': 0.618, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': 0.786, 'maxXD': 0.786},
	{'pattern': 'gartley', 'minXB': 0.618, 'maxXB': 0.618, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.272, 'maxBD': 1.618, 'minXD': 0.786, 'maxXD': 0.786},
	{'pattern': 'max gartley', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.128, 'maxBD': 2.236, 'minXD': 0.618, 'maxXD': 0.786},
	{'pattern': 'anti gartley', 'minXB': 0.618, 'maxXB': 0.786, 'minAC': 1.128, 'maxAC': 2.618, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': 1.272, 'maxXD': 1.272},
	{'pattern': 'leonardo', 'minXB': 0.5, 'maxXB': 0.5, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.128, 'maxBD': 2.618, 'minXD': 0.786, 'maxXD': 0.786},
	{'pattern': 'anti leonardo', 'minXB': 0.382, 'maxXB': 0.886, 'minAC': 1.128, 'maxAC': 2.618, 'minBD': 2.0, 'maxBD': 2.0, 'minXD': 1.272, 'maxXD': 1.272},
	{'pattern': 'ideal bat', 'minXB': 0.5, 'maxXB': 0.5, 'minAC': 0.5, 'maxAC': 0.618, 'minBD': 2.0, 'maxBD': 2.0, 'minXD': 0.886, 'maxXD': 0.886},
	{'pattern': 'bat', 'minXB': 0.382, 'maxXB': 0.5, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.618, 'maxBD': 2.618, 'minXD': 0.886, 'maxXD': 0.886},
	{'pattern': 'alt bat', 'minXB': 0.382, 'maxXB': 0.382, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 2.0, 'maxBD': 3.618, 'minXD': 1.128, 'maxXD': 1.128},
	{'pattern': 'anti bat', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 1.128, 'maxAC': 2.618, 'minBD': 2.0, 'maxBD': 2.618, 'minXD': 1.128, 'maxXD': 1.128},
	{'pattern': 'max bat', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.272, 'maxBD': 2.618, 'minXD': 0.886, 'maxXD': 0.886},
	{'pattern': 'anti alt bat', 'minXB': 0.236, 'maxXB': 0.5, 'minAC': 1.128, 'maxAC': 2.618, 'minBD': 2.618, 'maxBD': 2.618, 'minXD': 0.886, 'maxXD': 0.886},
	{'pattern': 'ideal crab', 'minXB': 0.618, 'maxXB': 0.618, 'minAC': 0.5, 'maxAC': 0.618, 'minBD': 3.14, 'maxBD': 3.14, 'minXD': 1.618, 'maxXD': 1.618},
	{'pattern': 'crab', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 2.24, 'maxBD': 3.618, 'minXD': 1.618, 'maxXD': 1.618},
	{'pattern': 'ideal deep crab', 'minXB': 0.886, 'maxXB': 0.886, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 2.24, 'maxBD': 3.618, 'minXD': 1.618, 'maxXD': 1.618},
	{'pattern': 'anti crab', 'minXB': 0.236, 'maxXB': 0.447, 'minAC': 1.128, 'maxAC': 2.618, 'minBD': 1.128, 'maxBD': 2.618, 'minXD': 0.618, 'maxXD': 0.618},
	{'pattern': 'focke wulf', 'minXB': 1.128, 'maxXB': 1.618, 'minAC': 0.5, 'maxAC': 0.786, 'minBD': 1.128, 'maxBD': 1.618, 'minXD': 0.146, 'maxXD': 4},
	{'pattern': 'anti deep crab', 'minXB': 0.236, 'maxXB': 0.382, 'minAC': 1.128, 'maxAC': 2.618, 'minBD': 1.128, 'maxBD': 1.128, 'minXD': 0.618, 'maxXD': 0.618},
	{'pattern': 'ideal butterfly', 'minXB': 0.786, 'maxXB': 0.786, 'minAC': 0.5, 'maxAC': 0.886, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': 1.27, 'maxXD': 1.27},
	{'pattern': 'butterfly', 'minXB': 0.786, 'maxXB': 0.786, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.618, 'maxBD': 2.618, 'minXD': 1.272, 'maxXD': 1.618},
	{'pattern': '113 butterfly', 'minXB': 0.786, 'maxXB': 1.0, 'minAC': 0.618, 'maxAC': 1.0, 'minBD': 1.128, 'maxBD': 1.618, 'minXD': 1.128, 'maxXD': 1.128},
	{'pattern': 'anti butterfly', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 1.128, 'maxAC': 2.618, 'minBD': 1.272, 'maxBD': 1.272, 'minXD': 0.618, 'maxXD': 0.786},
	{'pattern': 'max butterfly', 'minXB': 0.618, 'maxXB': 0.886, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.272, 'maxBD': 2.618, 'minXD': 1.272, 'maxXD': 1.618},
	{'pattern': 'bg 100', 'minXB': 0.707, 'maxXB': 0.707, 'minAC': 1.0, 'maxAC': 1.0, 'minBD': 1.414, 'maxBD': 1.414, 'minXD': 1.0, 'maxXD': 1.0},
	{'pattern': 'navarro 200', 'minXB': 0.382, 'maxXB': 0.786, 'minAC': 0.886, 'maxAC': 1.128, 'minBD': 0.886, 'maxBD': 3.618, 'minXD': 0.886, 'maxXD': 1.128},
	{'pattern': 'shark', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 1.128, 'maxAC': 1.618, 'minBD': 1.618, 'maxBD': 2.236, 'minXD': 0.886, 'maxXD': 1.128},
	{'pattern': 'alt shark', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 1.128, 'maxAC': 1.618, 'minBD': 1.618, 'maxBD': 2.236, 'minXD': 1.128, 'maxXD': 1.128},
	{'pattern': 'anti alt shark', 'minXB': 0.446, 'maxXB': 0.618, 'minAC': 0.618, 'maxAC': 0.886, 'minBD': 1.618, 'maxBD': 2.618, 'minXD': 0.886, 'maxXD': 0.886},
	{'pattern': 'anti shark', 'minXB': 0.446, 'maxXB': 0.618, 'minAC': 0.618, 'maxAC': 0.886, 'minBD': 1.618, 'maxBD': 2.618, 'minXD': 0.886, 'maxXD': 1.128},
	{'pattern': 'partizan', 'minXB': 0.128, 'maxXB': 3.618, 'minAC': 0.382, 'maxAC': 0.382, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': 0.618, 'maxXD': 3.618},
	{'pattern': 'stasi 486_618', 'minXB': 0.886, 'maxXB': 0.886, 'minAC': 0.5, 'maxAC': 0.5, 'minBD': 1.272, 'maxBD': 1.272, 'minXD': 1.0, 'maxXD': 1.0},
	{'pattern': '5-0', 'minXB': 1.128, 'maxXB': 1.618, 'minAC': 1.618, 'maxAC': 2.236, 'minBD': 0.5, 'maxBD': 0.5, 'minXD': 0.146, 'maxXD': 4.0},
	{'pattern': 'anti 5-0', 'minXB': 2.0, 'maxXB': 2.0, 'minAC': 0.447, 'maxAC': 0.618, 'minBD': 0.618, 'maxBD': 0.886, 'minXD': 0.146, 'maxXD': 4.0},
	{'pattern': '3 drives', 'minXB': 1.272, 'maxXB': 1.618, 'minAC': 0.618, 'maxAC': 0.786, 'minBD': 1.272, 'maxBD': 1.618, 'minXD': 1.618, 'maxXD': 2.618},
	{'pattern': 'anti 3 drives', 'minXB': 0.618, 'maxXB': 0.786, 'minAC': 1.272, 'maxAC': 1.618, 'minBD': 0.618, 'maxBD': 0.786, 'minXD': 0.13, 'maxXD': 0.886},
	{'pattern': 'black swan', 'minXB': 1.382, 'maxXB': 2.618, 'minAC': 0.236, 'maxAC': 0.5, 'minBD': 1.128, 'maxBD': 2.0, 'minXD': 1.128, 'maxXD': 2.618},
	{'pattern': 'white swan', 'minXB': 0.382, 'maxXB': 0.724, 'minAC': 2.0, 'maxAC': 4.237, 'minBD': 0.5, 'maxBD': 0.886, 'minXD': 0.382, 'maxXD': 0.886},
	{'pattern': 'ez partizan 2', 'minXB': 0.618, 'maxXB': 0.618, 'minAC': 0.382, 'maxAC': 0.382, 'minBD': 1.414, 'maxBD': 1.414, 'minXD': 0.707, 'maxXD': 0.707},
	{'pattern': '121 classic', 'minXB': 0.618, 'maxXB': 0.786, 'minAC': 0.146, 'maxAC': 4.0, 'minBD': 0.5, 'maxBD': 0.618, 'minXD': 0.146, 'maxXD': 4.0},
	{'pattern': 'nen star', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 1.414, 'maxAC': 2.14, 'minBD': 1.128, 'maxBD': 2.0, 'minXD': 1.272, 'maxXD': 1.272},
	{'pattern': 'anti nen star', 'minXB': 0.5, 'maxXB': 0.886, 'minAC': 0.467, 'maxAC': 0.707, 'minBD': 1.618, 'maxBD': 2.618, 'minXD': 0.786, 'maxXD': 0.786},
	{'pattern': 'anti drc 707', 'minXB': 0.618, 'maxXB': 0.618, 'minAC': 0.786, 'maxAC': 0.786, 'minBD': 1.414, 'maxBD': 1.414, 'minXD': 0.786, 'maxXD': 0.786},
	{'pattern': 'wolf tail', 'minXB': 0.786, 'maxXB': 0.886, 'minAC': 0.618, 'maxAC': 0.618, 'minBD': 2.618, 'maxBD': 4.4, 'minXD': 2.3, 'maxXD': 2.5},
	{'pattern': 'snorm', 'minXB': 0.9, 'maxXB': 1.1, 'minAC': 0.9, 'maxAC': 1.1, 'minBD': 0.9, 'maxBD': 1.1, 'minXD': 0.618, 'maxXD': 1.618},
	{'pattern': 'col poruchik', 'minXB': 0.128, 'maxXB': 3.618, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.0, 'maxBD': 1.0, 'minXD': 0.618, 'maxXD': 3.618},
	{'pattern': 'quasimodo', 'minXB': 1.618, 'maxXB': 1.618, 'minAC': 1.128, 'maxAC': 1.128, 'minBD': 0.618, 'maxBD': 0.618, 'minXD': 0.146, 'maxXD': 4.0},
	{'pattern': 'ww3 dr', 'minXB': 1.128, 'maxXB': 1.128, 'minAC': 0.786, 'maxAC': 0.786, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': 1.618, 'maxXD': 1.618},
	{'pattern': '121 ff', 'minXB': 0.5, 'maxXB': 0.618, 'minAC': 1.618, 'maxAC': 2.0, 'minBD': 0.5, 'maxBD': 0.786, 'minXD': 0.236, 'maxXD': 0.886},
	{'pattern': 'henry', 'minXB': 0.128, 'maxXB': 2.0, 'minAC': 0.44, 'maxAC': 0.618, 'minBD': 0.618, 'maxBD': 0.886, 'minXD': 0.618, 'maxXD': 1.618},
	{'pattern': 'next quasimodo', 'minXB': 0.382, 'maxXB': 0.382, 'minAC': 1.272, 'maxAC': 1.272, 'minBD': 1.128, 'maxBD': 1.128, 'minXD': 0.5, 'maxXD': 0.5},
	{'pattern': 'david vm1', 'minXB': 0.128, 'maxXB': 1.618, 'minAC': 0.382, 'maxAC': 0.382, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': 0.618, 'maxXD': 3.618},
	{'pattern': 'david vm2', 'minXB': 1.618, 'maxXB': 3.618, 'minAC': 0.382, 'maxAC': 0.382, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': 0.618, 'maxXD': 7.618},
	{'pattern': '121', 'minXB': 0.5, 'maxXB': 0.786, 'minAC': 1.128, 'maxAC': 3.618, 'minBD': 0.382, 'maxBD': 0.786, 'minXD': 0.382, 'maxXD': 0.786},
	{'pattern': 'anti 121', 'minXB': 1.272, 'maxXB': 2.0, 'minAC': 0.5, 'maxAC': 0.786, 'minBD': 1.272, 'maxBD': 2.0, 'minXD': 1.272, 'maxXD': 2.618},
	{'pattern': 'cypher', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 1.13, 'maxAC': 1.414, 'minBD': 1.272, 'maxBD': 2.0, 'minXD': 0.786, 'maxXD': 0.786},
	{'pattern': 'anti cypher', 'minXB': 0.5, 'maxXB': 0.786, 'minAC': 0.707, 'maxAC': 0.886, 'minBD': 1.618, 'maxBD': 2.618, 'minXD': 1.272, 'maxXD': 1.272},
	{'pattern': 'brick', 'minXB': 0.236, 'maxXB': 3.618, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.13, 'maxBD': 2.618, 'minXD': 0.382, 'maxXD': 0.618},
	{'pattern': 'golden crypto', 'minXB': 0.786, 'maxXB': 0.886, 'minAC': 0.707, 'maxAC': 1.0, 'minBD': 0.841, 'maxBD': 1.128, 'minXD': 0.841, 'maxXD': 1.732}]

	for xy in xtrmpoints:

		if len(xy) >= 5:

			xy = xy[::-1][:5:][::-1]

			X = xy[0]

			A = xy[1]

			B = xy[2]

			C = xy[3]

			D = xy[4]

			XA = A[1] - X[1]

			AB = A[1] - B[1]

			BC = C[1] - B[1]

			CD = C[1] - D[1]

			AD = A[1] - D[1]

			if not all(i in used for i in np.array([X,A,B,C,D])[:, 0]):

				if XA > 0 and AB > 0 and BC > 0 and CD > 0:

					XB = AB / XA

					AC = BC / AB

					BD = CD / BC

					XD = AD / XA

					for pattern in XABCD_patterns:

						XBcheck = 0

						ACcheck = 0

						BDcheck = 0

						XDcheck = 0

						if pattern['minXB'] == pattern['maxXB']:

							if pattern['minXB'] * (1 - deviation) <= XB <= pattern['maxXB'] * (1 + deviation):

								XBcheck = 1

							else:

								continue

						else:

							for i in pesavento_numbers:

								if i > pattern['maxXB']:

									break

								if pattern['minXB'] < i < pattern['maxXB']:

									if i * (1 - deviation) <= XB <= i * (1 + deviation):

										XBcheck = 1

										break

							if XBcheck != 1:

								if pattern['minXB'] * (1 - deviation) <= XB <= pattern['minXB'] * (1 + deviation):

									XBcheck = 1

								if pattern['maxXB'] * (1 - deviation) <= XB <= pattern['maxXB'] * (1 + deviation):

									XBcheck = 1

							if XBcheck != 1:

								continue

						if pattern['minAC'] == pattern['maxAC']:

							if pattern['minAC'] * (1 - deviation) <= AC <= pattern['maxAC'] * (1 + deviation):

								ACcheck = 1

							else:

								continue

						else:

							for i in pesavento_numbers:

								if i > pattern['maxAC']:

									break

								if pattern['minAC'] < i < pattern['maxAC']:

									if i * (1 - deviation) <= AC <= i * (1 + deviation):

										ACcheck = 1

										break

							if ACcheck != 1:

								if pattern['minAC'] * (1 - deviation) <= AC <= pattern['minAC'] * (1 + deviation):

									ACcheck = 1

								if pattern['maxAC'] * (1 - deviation) <= AC <= pattern['maxAC'] * (1 + deviation):

									ACcheck = 1

							if ACcheck != 1:

								continue

						if pattern['minBD'] == pattern['maxBD']:

							if pattern['minBD'] * (1 - deviationD) <= BD <= pattern['maxBD'] * (1 + deviationD):

								BDcheck = 1

							else:

								continue

						else:

							for i in pesavento_numbers:

								if i > pattern['maxBD']:

									break

								if pattern['minBD'] < i < pattern['maxBD']:

									if i * (1 - deviationD) <= BD <= i * (1 + deviationD):

										BDcheck = 1

										break

							if BDcheck != 1:

								if pattern['minBD'] * (1 - deviationD) <= BD <= pattern['minBD'] * (1 + deviationD):

									BDcheck = 1

								if pattern['maxBD'] * (1 - deviationD) <= BD <= pattern['maxBD'] * (1 + deviationD):

									BDcheck = 1

							if BDcheck != 1:

								continue

						if pattern['minXD'] == pattern['maxXD']:

							if pattern['minXD'] * (1 - deviationD) <= XD <= pattern['maxXD'] * (1 + deviationD):

								XDcheck = 1

							else:

								continue

						else:

							for i in pesavento_numbers:

								if i > pattern['maxXD']:

									break

								if pattern['minXD'] < i < pattern['maxXD']:

									if i * (1 - deviationD) <= XD <= i * (1 + deviationD):

										XDcheck = 1

										break

							if XDcheck != 1:

								if pattern['minXD'] * (1 - deviationD) <= XD <= pattern['minXD'] * (1 + deviationD):

									XDcheck = 1

								if pattern['maxXD'] * (1 - deviationD) <= XD <= pattern['maxXD'] * (1 + deviationD):

									XDcheck = 1

							if XDcheck != 1:

								continue

						if all([XBcheck, ACcheck, BDcheck, XDcheck]):

							used = np.append(used, np.array([ X, A, B, C, D]) [:, 0])

							patterns[len(patterns)] = {'pattern':'bullish' + ' ' + pattern['pattern'], 'X':X,'A':A, 'B':B, 'C':C, 'D':D}

							continue

			XA = X[1] - A[1]

			AB = B[1] - A[1]

			BC = B[1] - C[1]

			CD = D[1] - C[1]

			AD = D[1] - A[1]

			if not all(i in used for i in np.array([X,A,B,C,D])[:, 0]):

				if XA > 0 and AB > 0 and BC > 0 and CD > 0:

					XB = AB / XA

					AC = BC / AB

					BD = CD / BC

					XD = AD / XA

					for pattern in XABCD_patterns:

						XBcheck = 0

						ACcheck = 0

						BDcheck = 0

						XDcheck = 0

						if pattern['minXB'] == pattern['maxXB']:

							if pattern['minXB'] * (1 - deviation) <= XB <= pattern['maxXB'] * (1 + deviation):

								XBcheck = 1

							else:

								continue

						else:

							for i in pesavento_numbers:

								if i > pattern['maxXB']:

									break

								if pattern['minXB'] < i < pattern['maxXB']:

									if i * (1 - deviation) <= XB <= i * (1 + deviation):

										XBcheck = 1

										break

							if XBcheck != 1:

								if pattern['minXB'] * (1 - deviation) <= XB <= pattern['minXB'] * (1 + deviation):

									XBcheck = 1

								if pattern['maxXB'] * (1 - deviation) <= XB <= pattern['maxXB'] * (1 + deviation):

									XBcheck = 1

							if XBcheck != 1:

								continue

						if pattern['minAC'] == pattern['maxAC']:

							if pattern['minAC'] * (1 - deviation) <= AC <= pattern['maxAC'] * (1 + deviation):

								ACcheck = 1

							else:

								continue

						else:

							for i in pesavento_numbers:

								if i > pattern['maxAC']:

									break

								if pattern['minAC'] < i < pattern['maxAC']:

									if i * (1 - deviation) <= AC <= i * (1 + deviation):

										ACcheck = 1

										break

							if ACcheck != 1:

								if pattern['minAC'] * (1 - deviation) <= AC <= pattern['minAC'] * (1 + deviation):

									ACcheck = 1

								if pattern['maxAC'] * (1 - deviation) <= AC <= pattern['maxAC'] * (1 + deviation):

									ACcheck = 1

							if ACcheck != 1:

								continue

						if pattern['minBD'] == pattern['maxBD']:

							if pattern['minBD'] * (1 - deviationD) <= BD <= pattern['maxBD'] * (1 + deviationD):

								BDcheck = 1

							else:

								continue

						else:

							for i in pesavento_numbers:

								if i > pattern['maxBD']:

									break

								if pattern['minBD'] < i < pattern['maxBD']:

									if i * (1 - deviationD) <= BD <= i * (1 + deviationD):

										BDcheck = 1

										break

							if BDcheck != 1:

								if pattern['minBD'] * (1 - deviationD) <= BD <= pattern['minBD'] * (1 + deviationD):

									BDcheck = 1

								if pattern['maxBD'] * (1 - deviationD) <= BD <= pattern['maxBD'] * (1 + deviationD):

									BDcheck = 1

							if BDcheck != 1:

								continue

						if pattern['minXD'] == pattern['maxXD']:

							if pattern['minXD'] * (1 - deviationD) <= XD <= pattern['maxXD'] * (1 + deviationD):

								XDcheck = 1

							else:

								continue

						else:

							for i in pesavento_numbers:

								if i > pattern['maxXD']:

									break

								if pattern['minXD'] < i < pattern['maxXD']:

									if i * (1 - deviationD) <= XD <= i * (1 + deviationD):

										XDcheck = 1

										break

							if XDcheck != 1:

								if pattern['minXD'] * (1 - deviationD) <= XD <= pattern['minXD'] * (1 + deviationD):

									XDcheck = 1

								if pattern['maxXD'] * (1 - deviationD) <= XD <= pattern['maxXD'] * (1 + deviationD):

									XDcheck = 1

							if XDcheck != 1:

								continue

						if all([XBcheck, ACcheck, BDcheck, XDcheck]):

							used = np.append(used, np.array([ X, A, B, C, D]) [:, 0])

							patterns[len(patterns)] = {'pattern':'bearish' + ' ' + pattern['pattern'], 'X':X,'A':A, 'B':B, 'C':C, 'D':D}

							continue

	return patterns

def plot_pattern(i, patterns):

	plt.plot(np.array([patterns[i]['X'], patterns[i]['A'], patterns[i]['B'], patterns[i]['C'], patterns[i]['D']]) [:, 0], np.array([patterns[i]['X'], patterns[i]['A'], patterns[i]['B'], patterns[i]['C'], patterns[i]['D']]) [:, 1], '#CA2F91', alpha=1)

	plt.plot(np.array([patterns[i]['X'], patterns[i]['B'], patterns[i]['D']]) [:, 0], np.array([patterns[i]['X'], patterns[i]['B'], patterns[i]['D']]) [:, 1], '#CA2F91', alpha=1)

	plt.scatter(np.array([patterns[i]['X'], patterns[i]['A'], patterns[i]['B'], patterns[i]['C'], patterns[i]['D']]) [:, 0], np.array([patterns[i]['X'], patterns[i]['A'], patterns[i]['B'], patterns[i]['C'], patterns[i]['D']]) [:, 1], color='#CA2F91', s = 1)

	plt.gca().add_patch( plt.Polygon([ [patterns[i]['X'][0],patterns[i]['X'][1]], [patterns[i]['A'][0],patterns[i]['A'][1]], [patterns[i]['B'][0],patterns[i]['B'][1]] ], color='#CA2F91', alpha=0.125, linewidth=0.75) )

	plt.gca().add_patch( plt.Polygon([ [patterns[i]['B'][0],patterns[i]['B'][1]], [patterns[i]['C'][0],patterns[i]['C'][1]], [patterns[i]['D'][0],patterns[i]['D'][1]] ], color='#CA2F91', alpha=0.125, linewidth=0.75) )

	#relevance_zone = patches.Rectangle((patterns[i]['relevance'][0],patterns[i]['relevance'][1]), patterns[i]['relevance'][2], patterns[i]['relevance'][3], linewidth=0.5,edgecolor=c2rgba('#CA2F91', 1),facecolor=c2rgba('#CA2F91', 0.125))

	#plt.gca().add_patch(relevance_zone)

def nan_clean(array):

	return [i for i in array if str(i) != 'nan']

def get_klines(pair='BTCUSDT', interval='1DAY', fetch_time='7 day ago UTC'):

	#'1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'

	if interval == '1m':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_1MINUTE, fetch_time)

	if interval == '3m':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_3MINUTE, fetch_time)

	if interval == '5m':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_5MINUTE, fetch_time)

	if interval == '15m':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_15MINUTE, fetch_time)

	if interval == '30m':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_30MINUTE, fetch_time)

	if interval == '1h':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_1HOUR, fetch_time)

	if interval == '2h':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_2HOUR, fetch_time)

	if interval == '4h':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_4HOUR, fetch_time)

	if interval == '6h':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_6HOUR, fetch_time)

	if interval == '8h':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_8HOUR, fetch_time)

	if interval == '12h':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_12HOUR, fetch_time)

	if interval == '1d':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, fetch_time)

	if interval == '3d':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_3DAY, fetch_time)

	if interval == '1w':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_1WEEK, fetch_time)

	if interval == '1M':

		return  client.get_historical_klines(pair, Client.KLINE_INTERVAL_1MONTH, fetch_time)

def klines_width_matplotlib(interval:str):

	#'1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'

	if interval == '1m':

		return  0.5/(24/ (1 / 60))

	if interval == '3m':

		return  0.5/(24/ (3 / 60) )

	if interval == '5m':

		return  0.5/(24/ (5 / 60) )

	if interval == '15m':

		return  0.5/(24/ (15 / 60) )

	if interval == '30m':

		return  0.5/(24/ (30 / 60))

	if interval == '1h':

		return  0.5/(24/1)

	if interval == '2h':

		return  0.5/(24/2)

	if interval == '4h':

		return  0.5/(24/4)

	if interval == '6h':

		return  0.5/(24/6)

	if interval == '8h':

		return  0.5/(24/8)

	if interval == '12h':

		return  0.5/(24/12)

	if interval == '1d':

		return  0.5/(24/24)

	if interval == '3d':

		return  0.5/(24/72)

	if interval == '1w':

		return  0.5/(24/168)

	if interval == '1M':

		return  0.5/(24/720)

def check_connection():

	status = client.get_system_status()

	return not status['status']

def hello():

	print("")
	print("")
	print("")

	print("Binacci")
	print("tradingview.com/u/shutoff")
	print("t.me/shtff")

	print("")
	print("")
	print("")

def plot_chart(pair, candle_interval, dates, opens, highs, lows, closes, i, patterns, hash_):

	global bot

	print('')

	print(datetime.now().strftime("%H:%M:%S") + ' ' + 'Found pattern:', pair + ' ' + candle_interval + ' ' + patterns[i]['pattern'])

	plt.ioff()

	plt.style.use('default')

	fig = plt.figure(num='Binacci: ' + pair + '_' + candle_interval + '_' + patterns[i]['pattern']  + '_' + hash_, figsize=(1920 / 100,1080 / 100), facecolor='#FFFFFF', edgecolor='#FFFFFF')

	fig.patch.set_facecolor(color='#1A1D26')

	ax1 = fig.add_subplot(111)

	ax1.grid(color='#2C3238', linestyle='-', linewidth=1, alpha=0.15)

	ax1.set_facecolor(color='#FFFFFF')

	ax1.set_title(pair + ' - ' + candle_interval + ' - ' + patterns[i]['pattern'], color='#CA2F91', fontsize=22)

	candlestick_ohlc(ax1, zip(dates, opens, highs, lows, closes), width=klines_width_matplotlib(candle_interval), alpha=1, colorup='#53B987', colordown='#EB4D5C')

	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

	ax1.set_xlim(patterns[i]['X'][0], patterns[i]['D'][0])

	ax1.set_xlim(plt.xlim()[0] - (plt.xlim()[1] - plt.xlim()[0]) * 0.05, plt.xlim()[1] + (plt.xlim()[1] - plt.xlim()[0]) * 0.05)

	ax1.set_ylim(min(patterns[i]['X'][1], patterns[i]['A'][1], patterns[i]['B'][1], patterns[i]['C'][1], patterns[i]['D'][1]), max(patterns[i]['X'][1], patterns[i]['A'][1], patterns[i]['B'][1], patterns[i]['C'][1], patterns[i]['D'][1]))

	ax1.set_ylim(plt.ylim()[0] - (plt.ylim()[1] - plt.ylim()[0]) * 0.05, plt.ylim()[1] + (plt.ylim()[1] - plt.ylim()[0]) * 0.05)

	plot_pattern(i, patterns)

	x_text = plt.xlim()[1]

	info = client.get_symbol_info(pair)

	ticksize = info['filters'][0]['tickSize']

	#plt.text(x_text, patterns[i]['relevance'][1], s= e2_str_norm(patterns[i]['relevance'][1]), horizontalalignment='right', verticalalignment='top', color='#CA2F91', alpha=1, fontsize=22) # entry down

	#plt.text(x_text, format_value(patterns[i]['relevance'][1] + patterns[i]['relevance'][3], ticksize), s= e2_str_norm(format_value(patterns[i]['relevance'][1] + patterns[i]['relevance'][3], ticksize)), horizontalalignment='right', verticalalignment='bottom', color='#CA2F91', alpha=1, fontsize=22) # entry up

	ax1.text(0.1 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0], 0.45 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0],'tradingview.com/u/shutoff', color='#212532',alpha=0.25, size=70)

	ax1.text(0.6 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0], 0.3 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0],'@shtff', color='#212532',alpha=0.25, size=70)

	ax1.text(0.15 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0], 0.55 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0],pair + ' ' + candle_interval, color='#212532',alpha=0.25, size=70)

	save = 'img/' + pair + '_' + datetime.now().strftime("%d-%m-%Y") + '_' + candle_interval + '_' + patterns[i]['pattern']  + '_' + hash_

	fig.savefig(save, facecolor='#FFFFFF', edgecolor='#FFFFFF')

	bot.send_photo(chat_id='-1001297962599', photo=open(save + '.png', 'rb'), caption= "#" + pair + " " + "#" + candle_interval + " " + "#" + patterns[i]['pattern'].replace(' ', '_'))

	os.remove(save + '.png')

	plt.close(fig)

def main(pair='BTCUSDT', screening = 1 / 100, deviation = 0.5 / 100, deviationD=1.25 / 100,candle_interval = '4h', fetch_time = '14 day ago UTC', showPotential = False, blurryPatterns = False, hash_lib= []):

	klines = get_klines(pair, candle_interval, fetch_time)

	highs = np.array(klines, dtype=np.float) [:,2] # high

	lows = np.array(klines, dtype=np.float) [:,3] # low

	opens = np.array(klines, dtype=np.float) [:,1] # open

	closes = np.array(klines, dtype=np.float) [:,4] # close

	dates = np.array([mdates.date2num(datetime.fromtimestamp(i/1000)) for i in np.array(klines, dtype=np.float) [:,6] ]) # close time

	xtrmpoints = []

	if len(dates) >= 84:

		while screening <= 25 / 100:

			xtrmpoints.append(zigzag(highs, lows, dates, screening)) # find extreme points

			screening += 1.25 / 100

		patterns = harmonic_pattern_finding(xtrmpoints, deviation, deviationD, pair, closes[-1], showPotential, blurryPatterns)

		if len(patterns) > 0:

			for i in range(len(patterns)):

				hash2 = pair + '_' + patterns[i]['pattern'] + '_' + str(patterns[i]['X'][1]) + str(patterns[i]['A'][1]) + str(patterns[i]['B'][1]) + str(patterns[i]['C'][1])

				hash_ = hashlib.md5(hash2.encode()).hexdigest()

				before382 = 0

				level382 = patterns[i]['D'][1] + (patterns[i]['C'][1] - patterns[i]['D'][1]) * 0.146 if patterns[i]['pattern'][:7] == 'bullish' else patterns[i]['D'][1] - (patterns[i]['D'][1] - patterns[i]['C'][1]) * 0.146

				if patterns[i]['pattern'][:7] == 'bullish':

					if closes[-1] < level382:

						before382 = 1

				else:

					if closes[-1] > level382:

						before382 = 1

				if not hash_ in hash_lib and dates[0] != patterns[i]['X'][0] and before382:

					plot_chart(pair, candle_interval, dates, opens, highs, lows, closes, i, patterns, hash_)

					return hash_

				else:

					return "None"

if __name__ == '__main__':

	hello()

	if check_connection():

		print('Connection: ok')

		if os.path.isfile("hashLib.txt") and len(open("hashLib.txt", "r").read()) != 0:

			hash_lib = json.load(open("hashLib.txt", "r"))

		else:

			hash_lib = []

		products = products_creator(use_market = ["USDT", "BTC"])

		#products = ['BTCUSDT', 'LTCUSDT', 'ETHUSDT', 'BCHABCUSDT', 'EOSUSDT', 'ETCUSDT', 'XRPUSDT']

		while True:

			print('')

			print(datetime.now().strftime("%H:%M:%S") + ' ' + 'Start')

			if len(hash_lib) > 100:

				hash_lib = hash_lib[-1:-101:-1][::-1]

			for pair in products:

				for tf in ['1h']:

					out = main(pair=pair, 
						screening = 10 / 100, # zigzag
						deviation = 5 / 100, # B, C deviation
						deviationD = 5 / 100, # D deviation
						candle_interval = tf,  #'1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'
						fetch_time = '30 day ago UTC',
						showPotential = False,
						blurryPatterns = False,
						hash_lib = hash_lib)

					if out != "None":

						hash_lib.append(out)

			hash_lib = [i for i in hash_lib if i != None]

			json.dump(hash_lib, open("hashLib.txt", "w"))

			print('')

			print(datetime.now().strftime("%H:%M:%S") + ' ' + 'Finish')

			time.sleep(900)

	else:

		print("Connection: error")