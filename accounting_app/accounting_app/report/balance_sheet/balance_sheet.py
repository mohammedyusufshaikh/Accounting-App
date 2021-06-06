# Copyright (c) 2013, Mohammed Yusuf Shaikh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.utils.user_settings import get
from six import reraise
# import frappe

def execute(filters=None):
	columns, data = [], []

	columns =[
		{
			"label": "Account",
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Account",
		},
		
		{
			"label": "Value",
			"fieldname": "value",
			"fieldtype": "int",
		},
	]
	# tmp = get_data(filters)
	# for d in tmp:
	# 	d.update({'value':"0"})
	# data = tmp

	assets = get_data('Asset',filters)
	liabilities = get_data('Liability',filters)
	data.extend(assets)
	data.extend(liabilities)

	if filters.filter_based_on == 'Fiscal Year':
		year = frappe.db.sql(""" SELECT
						start_date, end_date
					FROM
						`tabFiscal Year`
					WHERE
						year=%s""",filters.fiscal_year, as_dict=1)[0]
		date = [year.start_date, year.end_date]
		print("FY",filters.fiscal_year)
		period_key, period_label = "{}".format(filters.fiscal_year.replace(" ", "_").replace("-", "_")), filters.fiscal_year
		print("PK",period_key,period_label)
	elif filters.filter_based_on == 'Date Range':
		period_key, period_label = "Date Range", "Date Range"
		date = [filters.from_date, filters.to_date]
		# print(date)

	return columns, data


def get_data(account_type,filters=None):
	accounts = frappe.db.sql("""
	SELECT name FROM `tabAccount` WHERE company=%s and  account_type=%s 
	ORDER BY lft
	""",values=(filters.company,account_type),as_dict=1)
	numbers = get_account_data()
	return accounts

def get_account_data():
	numbers = frappe.db.sql("""
	SELECT sum(debit_amount) as debit,sum(credit_amount),account
	from `tabGL Entry` left join `tabAccount` 
	on `tabGL Entry`.account=tabAccount.name group by account""",as_dict=1)
	return numbers