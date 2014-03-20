#!/usr/bin/env python

import sys
import re
import csv
from bs4 import BeautifulSoup

def row_to_dict(row):
    date_str = row.find(id = re.compile(r'transactionView\.output\.transactionDate\d+')).get_text()
    date = " ".join(date_str.split()[0:3])

    ref_str = row.find(id = re.compile(r'transactionView\.output\.reference\d+')).get_text()
    ref = " ".join(ref_str.split())

    desc_str = row.find(id = re.compile(r'transactionView\.output\.transactionDescription\d+')).get_text()
    desc = " ".join(desc_str.split())

    maybe_money_in = row.find(id = re.compile(r'transactionView\.output\.moneyIn\d+'))
    if (maybe_money_in and re.search("\d+\.\d\d", maybe_money_in.get_text())):
        delta = '+' + maybe_money_in.get_text().strip()
    else:
        money_out = row.find(id = re.compile(r'transactionView\.output\.moneyOut\d+'))
        delta = '-' + money_out.get_text().strip()
    
    balance_str = row.find(id = re.compile(r'transactionView\.output\.total\d+')).get_text()
    balance = " ".join(balance_str.split())
     

    return {'date':date, 'ref':ref, 'desc':desc, 'delta':delta, 'balance':balance}

html = sys.stdin.read()
soup = BeautifulSoup(html)
transactions = soup.find_all('div', 'transactionJournalRow')
dicts = [row_to_dict(r) for r in transactions]
output = [d for d in dicts if not re.search('R', d['ref'])]

with open('out.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'reference', 'description', 'amount', 'balance'])
    for r in output:
        writer.writerow([r['date'], r['ref'], r['desc'], r['delta'], r['balance']])

