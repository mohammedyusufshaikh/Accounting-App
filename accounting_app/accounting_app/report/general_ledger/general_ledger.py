# Copyright (c) 2013, Mohammed Yusuf Shaikh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from datetime import date
import frappe

def execute(filters=None):
	columns, data = [], []
	columns =[
		{
			"label": "GL Entry",
			"fieldname": "gl_entry",
			"fieldtype": "Link",
			"options": "GL Entry",
		},
		{
			"label":"Posting Date",
			"fieldname":"posting_date",
			"fieldtype":"Date",

		},
		{
			"label":"Account",
			"fieldname":"account",
			"fieldtype":"Link",
			"options":"Account"
		},
		{
			"label":"Debit",
			"fieldname":"debit_amount",
			"fieldtype":"Data"
		},
		{
			"label":"Credit",
			"fieldname":"credit_amount",
			"fieldtype":"Data"
		},
		{
			"label":"Voucher No",
			"fieldname":"voucher_no",
			"fieldtype":"Data"
		},
		{
			"label":"Voucher Type",
			"fieldname":"voucher_type",
			"fieldtype":"Data"
		},
		{
			"label":"Party",
			"fieldname":"party",
			"fieldtype":"Link",
			"options":"Party"
		}
		]
	
	tmp = get_data(filters)
	data  = calc(tmp)
	return columns, data


def get_data(filters):
	gl_entries = frappe.db.sql(""" SELECT
						name as gl_entry,posting_date,account,debit_amount,credit_amount,voucher_no,voucher_type,party
					FROM
						`tabGL Entry` gl
					
					WHERE
						{conditions}
					
					""".format(conditions=get_conditions(filters)),filters,as_dict=1)

	return gl_entries

def get_conditions(filters):
	conditions = []
	if filters.get('company'):
		conditions.append('company=%(company)s')
	
	if filters.get('account'):
		conditions.append('account=%(account)s')

	if filters.get('party'):
		conditions.append('party=%(party)s')

	conditions.append("posting_date>=%(from_date)s")
	conditions.append("posting_date<=%(to_date)s")


	
	return "{}".format(" and ".join(conditions))

def calc(gl_entries):
	opening  = construct_dict('Opening')
	total = construct_dict('Total')
	closing = construct_dict('Closing(Openning + Total)')

	total_credit,total_debit =0,0
	for entry in gl_entries:
		
		total_debit = total_debit + int(entry.debit_amount)
		total_credit =total_credit + int(entry.credit_amount)
	total.update({
		'debit_amount':total_debit,
		'credit_amount':total_credit
		})
	closing.update({
		'debit_amount':total_debit,
		'credit_amount':total_credit
		})

	gl_entries.append(total)
	gl_entries.append(closing)
	gl_entries.insert(0,opening)

	return gl_entries




def construct_dict(text):
	return dict(
		account = text,
		debit_amount = 0,
		credit_amount = 0
	)