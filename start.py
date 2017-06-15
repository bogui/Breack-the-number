# /usr/bin/env python

from sys import version_info

if version_info[0] < 3:
	import extract_nums as v2
	e2 = v2.ExtractNums
	e2.cookie(e2.target())
else:
	import extract_nums_v3 as v3
	e3 = v3.ExtractNumsV3()
	if e3.wait('Initializing'):
		target = e3.target()
		cookie = e3.cookie(target)
