#!/usr/bin/python3

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s", datefmt='%d/%m/%Y %H:%M:%S')

from core import engine

import re
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta


def help(retcode: int) :
	location = sys.argv[0]
	print(f"usage : {location} [<n_months>m][<n_weeks>w][<n_days>d]")
	print(f"        {location} follow <source_id> <series_url>")
	print(f"        {location} init")
	sys.exit(retcode)


def main(args) :

	if len(args) == 0 :
		help(1)
	
	if args[0] in ['-h', '--help'] :
		help(0)
	
	if args[0] == 'init' :
		engine.init()
		return
	
	if args[0] == 'follow' :
		if len(args) < 3 :
			help(1)
		source_id = args[1]
		url = args[2]
		engine.followSeries(source_id, url)
		return
	
	m = re.fullmatch(r'([0-9]+m)?([0-9]+w)?([0-9]+d)?', string=args[0])
	if m is None :
		print(f"Bad argument format : `{args[0]}`")
		sys.exit(1)
	nums = [
		0 if n is None else int(n[:-1])
		for n in m.groups()
	]

	begin = datetime.now().date()
	end = begin + relativedelta(months=nums[0], weeks=nums[1], days=nums[2])

	engine.run(begin, end)


if __name__ == '__main__' :
	main(sys.argv[1:])
