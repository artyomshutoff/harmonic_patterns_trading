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
{'pattern': '3 drives', 'minXB': 1.618, 'maxXB': 1.618, 'minAC': 0.786, 'maxAC': 0.786, 'minBD': 1.618, 'maxBD': 1.618, 'minXD': '-', 'maxXD': '-'}

]

for i in range(len(XABCD_patterns)):
	XABCD_patterns.append({'pattern': 'A ' + XABCD_patterns[i]['pattern'], 'minXB': 0.5, 'maxXB': 0.5, 'minAC': 0.5, 'maxAC': 0.618, 'minBD': 2.0, 'maxBD': 2.0, 'minXD': 0.786, 'maxXD': 0.886})
	if XABCD_patterns[i]['minBD'] == '-' or XABCD_patterns[i]['maxBD'] == '-':
		XABCD_patterns[-1]['minXB'] = '-'
		XABCD_patterns[-1]['maxXB'] = '-'
	else:
		XABCD_patterns[-1]['minXB'] = 1 / XABCD_patterns[i]['maxBD'] // 0.001 / 1000
		XABCD_patterns[-1]['maxXB'] = 1 / XABCD_patterns[i]['minBD'] // 0.001 / 1000
	if XABCD_patterns[i]['minXB'] == '-' or XABCD_patterns[i]['maxXB'] == '-':
		XABCD_patterns[-1]['minBD'] = '-'
		XABCD_patterns[-1]['maxBD'] = '-'
	else:
		XABCD_patterns[-1]['minBD'] = 1 / XABCD_patterns[i]['maxXB'] // 0.001 / 1000
		XABCD_patterns[-1]['maxBD'] = 1 / XABCD_patterns[i]['minXB'] // 0.001 / 1000
	if XABCD_patterns[i]['minAC'] == '-' or XABCD_patterns[i]['maxAC'] == '-':
		XABCD_patterns[-1]['minAC'] = '-'
		XABCD_patterns[-1]['maxAC'] = '-'
	else:
		XABCD_patterns[-1]['minAC'] = 1 / XABCD_patterns[i]['maxAC'] // 0.001 / 1000
		XABCD_patterns[-1]['maxAC'] = 1 / XABCD_patterns[i]['minAC'] // 0.001 / 1000
	if XABCD_patterns[i]['minXD'] == '-' or XABCD_patterns[i]['maxXD'] == '-':
		XABCD_patterns[-1]['minXD'] = '-'
		XABCD_patterns[-1]['maxXD'] = '-'
	else:
		XABCD_patterns[-1]['minXD'] = 1 / XABCD_patterns[i]['maxXD'] // 0.001 / 1000
		XABCD_patterns[-1]['maxXD'] = 1 / XABCD_patterns[i]['minXD'] // 0.001 / 1000
