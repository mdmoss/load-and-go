#!/usr/bin/env python

import sys
import re
import csv
from bs4 import BeautifulSoup

def row_to_dict(row):
    date_tag = row.find(id = re.compile(r'transactionView\.output\.transactionDate\d+'))
    date = " ".join(date_tag.get_text().split()[0:3])

    ref_tag = row.find(id = re.compile(r'transactionView\.output\.reference\d+'))
    ref = " ".join(ref_tag.get_text().split())

    desc_tag = row.find(id = re.compile(r'transactionView\.output\.transactionDescription\d+'))
    desc = " ".join(desc_tag.get_text().split())

    maybe_money_in = row.find(id = re.compile(r'transactionView\.output\.moneyIn\d+'))
    if (maybe_money_in and re.search("\d+\.\d\d", maybe_money_in.get_text())):
        amount = '+' + maybe_money_in.get_text().strip()
    else:
        money_out = row.find(id = re.compile(r'transactionView\.output\.moneyOut\d+'))
        amount = '-' + money_out.get_text().strip()
    
    balance_tag = row.find(id = re.compile(r'transactionView\.output\.total\d+'))
    balance = " ".join(balance_tag.get_text().split())

    return {'date':date, 'ref':ref, 'desc':desc, 'amount':amount, 'balance':balance}

html = sys.stdin.read()
soup = BeautifulSoup(html)
transactions = soup.find_all('div', 'transactionJournalRow')
dicts = [row_to_dict(r) for r in transactions]
output = [d for d in dicts if not re.search('R', d['ref'])]

with open('out.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'reference', 'description', 'amount', 'balance'])
    for r in output:
        writer.writerow([r['date'], r['ref'], r['desc'], r['amount'], r['balance']])

