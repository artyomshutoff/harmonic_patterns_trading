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
     FiboType = [0.276, 0.382, 0.447, 0.5, 0.618, 0.707, 0.786, 0.886, 1.0, 1.128, 1.272, 1.414, 1.618, 2.0, 2.236, 2.618, 3.618]
     AntiPatterns = True
     #FiboType = [0.146, 0.236, 0.382, 0.447, 0.5, 0.618, 0.707, 0.786, 0.841, 0.886, 1.0, 1.128, 1.272, 1.414, 1.5, 1.618, 1.732, 1.902, 2.0, 2.236, 2.414, 2.618, 3.14, 3.330 ,3.618, 4.0, 4.236, 5.388, 5.657, 6.854]

     XABCD_patterns = [

     {'pattern': 'ideal gartley', 'minXB': 0.618, 'maxXB': 0.618, 'minAC': 0.618, 'maxAC': 0.786, 'minBD': 1.272, 'maxBD': 1.618, 'minXD': '-', 'maxXD': '-'},
     {'pattern': '618 gartley', 'minXB': 0.618, 'maxXB': 0.618, 'minAC': 0.618, 'maxAC': 0.618, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': '-', 'maxXD': '-'},
     {'pattern': 'ideal butterfly', 'minXB': 0.786, 'maxXB': 0.786, 'minAC': 0.618, 'maxAC': 0.786, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': 1.272, 'maxXD': 1.618},
     {'pattern': '618 butterfly', 'minXB': 0.786, 'maxXB': 0.786, 'minAC': 0.382, 'maxAC': 0.786, 'minBD': 1.618, 'maxBD': 2.618, 'minXD': 1.618, 'maxXD': 1.618},

     {'pattern': 'gartley', 'minXB': 0.618, 'maxXB': 0.618, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.128, 'maxBD': 1.618, 'minXD': 0.786, 'maxXD': 0.786},
     {'pattern': 'butterfly', 'minXB': 0.786, 'maxXB': 0.786, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.618, 'maxBD': 2.236, 'minXD': 1.272, 'maxXD': 1.272},
     {'pattern': 'crab', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 2.618, 'maxBD': 3.618, 'minXD': 1.618, 'maxXD': 1.618},
     {'pattern': 'deep crab', 'minXB': 0.886, 'maxXB': 0.886, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 2.0, 'maxBD': 3.618, 'minXD': 1.618, 'maxXD': 1.618},
     {'pattern': 'bat', 'minXB': 0.382, 'maxXB': 0.5, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.618, 'maxBD': 2.618, 'minXD': 0.886, 'maxXD': 0.886},
     {'pattern': 'alt bat', 'minXB': 0.382, 'maxXB': 0.382, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 2.0, 'maxBD': 3.618, 'minXD': 1.128, 'maxXD': 1.128},
     {'pattern': '5-0', 'minXB': 1.128, 'maxXB': 1.618, 'minAC': 1.618, 'maxAC': 2.236, 'minBD': 0.5, 'maxBD': 0.5, 'minXD': '-', 'maxXD': '-'},
     {'pattern': 'shark', 'minXB': '-', 'maxXB': '-', 'minAC': 1.128, 'maxAC': 1.618, 'minBD': 1.618, 'maxBD': 2.236, 'minXD': 0.886, 'maxXD': 0.886},
     {'pattern': 'shark', 'minXB': '-', 'maxXB': '-', 'minAC': 1.128, 'maxAC': 1.618, 'minBD': 1.618, 'maxBD': 2.236, 'minXD': 1.128, 'maxXD': 1.128},
     {'pattern': 'leonardo', 'minXB': 0.5, 'maxXB': 0.5, 'minAC': 0.382, 'maxAC': 0.886, 'minBD': 1.128, 'maxBD': 2.618, 'minXD': 0.786, 'maxXD': 0.786},
     {'pattern': 'nen star', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 1.414, 'maxAC': 2.14, 'minBD': 1.128, 'maxBD': 2.0, 'minXD': 1.272, 'maxXD': 1.272},
     {'pattern': 'cypher', 'minXB': 0.382, 'maxXB': 0.618, 'minAC': 1.128, 'maxAC': 1.414, 'minBD': 1.272, 'maxBD': 2.0, 'minXD': 0.786, 'maxXD': 0.786},

     {'pattern': '3 drives', 'minXB': 1.272, 'maxXB': 1.272, 'minAC': 0.618, 'maxAC': 0.618, 'minBD': 1.272, 'maxBD': 1.272, 'minXD': '-', 'maxXD': '-'},
     {'pattern': '3 drives', 'minXB': 1.618, 'maxXB': 1.618, 'minAC': 0.786, 'maxAC': 0.786, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': '-', 'maxXD': '-'},

     {'pattern': 'perfect bat', 'minXB': 0.5, 'maxXB': 0.5, 'minAC': 0.5, 'maxAC': 0.618, 'minBD': 2.0, 'maxBD': 2.0, 'minXD': 0.786, 'maxXD': 0.886}
     ]

     if AntiPatterns:

          for i in range(len(XABCD_patterns)):
               XABCD_patterns.append({'pattern': 'A ' + XABCD_patterns[i]['pattern'], 'minXB': 0.5, 'maxXB': 0.5, 'minAC': 0.5, 'maxAC': 0.618, 'minBD': 2.0, 'maxBD': 2.0, 'minXD': 0.786, 'maxXD': 0.886})
               if XABCD_patterns[i]['minBD'] == '-' or XABCD_patterns[i]['maxBD'] == '-':
                    XABCD_patterns[-1]['minXB'] = '-'
                    XABCD_patterns[-1]['maxXB'] = '-'

               else:
                    XABCD_patterns[-1]['minXB'] = round(1 / XABCD_patterns[i]['maxBD'], 3)
                    XABCD_patterns[-1]['maxXB'] = round(1 / XABCD_patterns[i]['minBD'], 3)
                    
               if XABCD_patterns[i]['minXB'] == '-' or XABCD_patterns[i]['maxXB'] == '-':
                    XABCD_patterns[-1]['minBD'] = '-'
                    XABCD_patterns[-1]['maxBD'] = '-'

               else:
                    XABCD_patterns[-1]['minBD'] = round(1 / XABCD_patterns[i]['maxXB'], 3)
                    XABCD_patterns[-1]['maxBD'] = round(1 / XABCD_patterns[i]['minXB'], 3)
                    
               if XABCD_patterns[i]['minAC'] == '-' or XABCD_patterns[i]['maxAC'] == '-':
                    XABCD_patterns[-1]['minAC'] = '-'
                    XABCD_patterns[-1]['maxAC'] = '-'

               else:
                    XABCD_patterns[-1]['minAC'] = round(1 / XABCD_patterns[i]['maxAC'], 3)
                    XABCD_patterns[-1]['maxAC'] = round(1 / XABCD_patterns[i]['minAC'], 3)
                    
               if XABCD_patterns[i]['minXD'] == '-' or XABCD_patterns[i]['maxXD'] == '-':
                    XABCD_patterns[-1]['minXD'] = '-'
                    XABCD_patterns[-1]['maxXD'] = '-'

               else:
                    XABCD_patterns[-1]['minXD'] = round(1 / XABCD_patterns[i]['maxXD'], 3)
                    XABCD_patterns[-1]['maxXD'] = round(1 / XABCD_patterns[i]['minXD'], 3)

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
                              if not (pattern['minXB'] == '-' or pattern['maxXB'] == '-'):
                                   if pattern['minXB'] == pattern['maxXB']:
                                        if pattern['minXB'] * (1 - deviation) <= XB <= pattern['maxXB'] * (1 + deviation):
                                             XBcheck = 1
                                        else:
                                             continue
                                   else:
                                        for i in FiboType:
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
                              else:
                                   XBcheck = 1
                              if not (pattern['minAC'] == '-' or pattern['maxAC'] == '-'):
                                   if pattern['minAC'] == pattern['maxAC']:
                                        if pattern['minAC'] * (1 - deviation) <= AC <= pattern['maxAC'] * (1 + deviation):
                                             ACcheck = 1
                                        else:
                                             continue
                                   else:
                                        for i in FiboType:
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

                              else:
                                   ACcheck = 1
                              if not (pattern['minBD'] == '-' or pattern['maxBD'] == '-'):
                                   if pattern['minBD'] == pattern['maxBD']:
                                        if pattern['minBD'] * (1 - deviationD) <= BD <= pattern['maxBD'] * (1 + deviationD):
                                             BDcheck = 1
                                        else:
                                             continue
                                   else:
                                        for i in FiboType:
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
                              else:
                                   BDcheck = 1
                              if not (pattern['minXD'] == '-' or pattern['maxXD'] == '-'):
                                   if pattern['minXD'] == pattern['maxXD']:
                                        if pattern['minXD'] * (1 - deviationD) <= XD <= pattern['maxXD'] * (1 + deviationD):
                                             XDcheck = 1
                                        else:
                                             continue
                                   else:
                                        for i in FiboType:
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
                              else:
                                   XDcheck = 1
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
                              if not (pattern['minXB'] == '-' or pattern['maxXB'] == '-'):
                                   if pattern['minXB'] == pattern['maxXB']:
                                        if pattern['minXB'] * (1 - deviation) <= XB <= pattern['maxXB'] * (1 + deviation):
                                             XBcheck = 1
                                        else:
                                             continue
                                   else:
                                        for i in FiboType:
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
                              else:
                                   XBcheck = 1
                              if not (pattern['minAC'] == '-' or pattern['maxAC'] == '-'):
                                   if pattern['minAC'] == pattern['maxAC']:
                                        if pattern['minAC'] * (1 - deviation) <= AC <= pattern['maxAC'] * (1 + deviation):
                                             ACcheck = 1
                                        else:
                                             continue
                                   else:
                                        for i in FiboType:
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
                              else:
                                   ACcheck = 1
                              if not (pattern['minBD'] == '-' or pattern['maxBD'] == '-'):
                                   if pattern['minBD'] == pattern['maxBD']:
                                        if pattern['minBD'] * (1 - deviationD) <= BD <= pattern['maxBD'] * (1 + deviationD):
                                             BDcheck = 1
                                        else:
                                             continue
                                   else:
                                        for i in FiboType:
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
                              else:
                                   BDcheck = 1
                              if not (pattern['minXD'] == '-' or pattern['maxXD'] == '-'):
                                   if pattern['minXD'] == pattern['maxXD']:
                                        if pattern['minXD'] * (1 - deviationD) <= XD <= pattern['maxXD'] * (1 + deviationD):
                                             XDcheck = 1
                                        else:
                                             continue
                                   else:
                                        for i in FiboType:
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
                              else:
                                   XDcheck = 1
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

def klines_width_matplotlib(interval:str):

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
     print("Lil_Bat")

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

def main(pair, screening, deviation, deviationD, candle_interval, fetch_time, showPotential, blurryPatterns, hash_lib):

     klines = client.get_historical_klines(pair, candle_interval, fetch_time)
     highs = np.array(klines, dtype=np.float) [:,2]
     lows = np.array(klines, dtype=np.float) [:,3]
     opens = np.array(klines, dtype=np.float) [:,1]
     closes = np.array(klines, dtype=np.float) [:,4]
     dates = np.array([mdates.date2num(datetime.fromtimestamp(i/1000)) for i in np.array(klines, dtype=np.float) [:,6] ])
     xtrmpoints = []

     if len(dates) >= 84:
          while screening <= 25 / 100:
               xtrmpoints.append(zigzag(highs, lows, dates, screening))
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
          #products = products_creator(use_market = ["USDT"])
          products = ['BTCUSDT', 'LTCUSDT', 'ETHUSDT', 'BCHABCUSDT', 'EOSUSDT', 'ETCUSDT', 'XRPUSDT', 'BNBUSDT', 'TRXUSDT']
          while True:
               print('')
               print(datetime.now().strftime("%H:%M:%S") + ' ' + 'Start')
               if len(hash_lib) > 100:
                    hash_lib = hash_lib[-1:-101:-1][::-1]
               for pair in products:
                    for tf in ['1h']:
                         out = main(pair=pair, 
                              screening = 10 / 100,
                              deviation = 10 / 100,
                              deviationD = 10 / 100,
                              candle_interval = tf, 
                              fetch_time = '90 day ago UTC',
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