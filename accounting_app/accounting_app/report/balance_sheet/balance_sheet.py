# Copyright (c) 2013, Mohammed Yusuf Shaikh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.utils.user_settings import get
from six import reraise
# import frappe

def execute(filters=None):
	columns, data = [], []

	if filters.filter_based_on == 'Fiscal Year':
		year = frappe.db.sql(""" SELECT
						start_date, end_date
					FROM
						`tabFiscal Year`
					WHERE
						year=%s""",filters.fiscal_year, as_dict=1)[0]
		date = [year.start_date, year.end_date]
		period_key, period_label = "{}".format(filters.fiscal_year.replace(" ", "_").replace("-", "_")), filters.fiscal_year
	elif filters.filter_based_on == 'Date Range':
		period_key, period_label = "Date Range", "Date Range"
		date = [filters.from_date, filters.to_date]

	asset = get_data(date, filters.company, 'Asset', 'Debit', period_key)
	liability = get_data(date, filters.company, 'Liability', 'Credit', period_key)
	# equity = get_data(date, filters.company, 'Equity', 'Credit', period_key)

	data = []
	data.extend(asset or [])
	data.extend(liability or [])

	for d in data:
		print(d)
	columns =[
		{
			"fieldname": "account",
			"label": "Account",
			"fieldtype": "Link",
			"options": "Account",
		},
		
		{
			
			"fieldname": period_key,
			"label": period_label,
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150
		},
	]
	return columns, data


def get_data(date,company,account_type,dr_cr,period_key):
	accounts = get_accounts(company,account_type)
	data = []
	if accounts:
		cnt = 0
		for info in accounts:
			if info.parent_account==None or info.parent_account==data[-1]['account']:
				append(data,cnt,info,period_key)
				cnt+=1
			else:
				for d in data:
					if d['account'] == info.parent_account:
						cnt = d['indent'] + 1
						break
				append(data,cnt,info,period_key)
				cnt+=1
	temp = []
	for info in data:
		balance  = get_account_balance(info['account'],date)
		if balance:
			info[period_key] = abs(balance)
			temp.append(info)

	
	for t in temp:
		for d in data:
			if d["account"] == t["parent_account"]:
				if d[period_key] == 0:
					d[period_key] = t[period_key]
					temp.append(d)
				else:
					d[period_key] += t[period_key]
	data = [d for d in data if d[period_key] != 0]
	if data:
		data.append({
			"account": "Total " + account_type + " (" + dr_cr + ")",
			period_key: data[0][period_key]
		})
		data.append({})
	return data

def get_accounts(company,account_type):
	return frappe.db.sql("""
	SELECT name, parent_account, lft,account_type,sub_account_type, is_group 
	FROM tabAccount 
	WHERE company=%s and account_type=%s 
	ORDER BY lft""",(company,account_type),as_dict=1)

def append(data,cnt,info,period_key):
	print("INFO",info.name)
	data.append({
		"account":info.name,
		"account_type":info.account_type,
		"parent_account":info.parent_account,
		"indent":cnt,
		"has_value":info.is_group,
		period_key:0
	})


def get_account_balance(account, date):
	return frappe.db.sql(""" SELECT 
					sum(debit_amount) - sum(credit_amount) 
				FROM 
					`tabGL Entry` 
				WHERE 
					account=%s and posting_date>=%s and posting_date<=%s""",
				(account, date[0], date[1]))[0][0]

