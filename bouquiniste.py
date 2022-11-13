#!/usr/bin/python3

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s", datefmt='%d/%m/%Y %H:%M:%S')

from core import engine

import re
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta


def help(retcode: int) :
	print(f"usage : {sys.argv[0]} [<n_months>m][<n_weeks>w][<n_days>d]")
	sys.exit(retcode)


def main() :

	args = sys.argv[1:]
	if len(args) == 0 :
		help(1)
	
	if args[0] in ['-h', '--help'] :
		help(0)
	
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
	main()
