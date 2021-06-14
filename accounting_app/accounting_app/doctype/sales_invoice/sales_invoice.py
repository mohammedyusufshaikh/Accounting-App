# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammed Yusuf Shaikh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.data import nowdate

class SalesInvoice(Document):
	def validate(self):
		self.validate_quantity()

	def validate_quantity(self):
		for data in self.item:
			if int(data.qty) <= 0:
				frappe.throw("product quantity should be at least 1")

def set_accounts(sales_invoice):
		if not sales_invoice.income_account:
			sales_invoice.income_account = frappe.db.get_value('Company',sales_invoice.company, 'default_income_account')
		if not sales_invoice.debit_to:
			sales_invoice.debit_to = frappe.db.get_value('Company',sales_invoice.company, 'default_receivable_account')

@frappe.whitelist(allow_guest=True)
def create_sales_invoice(item_name,qty):
	item_details = frappe.get_doc("Item",item_name)
	sales_invoice  = frappe.new_doc("Sales Invoice")
	sales_invoice.customer = 'Raj'
	sales_invoice.posting_date = nowdate()
	sales_invoice.payment_due_date = nowdate()
	sales_invoice.total_qty = qty

	sales_invoice.total_amount = item_details.standard_selling_rate
	sales_invoice.company = 'Gada Electronics'
	set_accounts(sales_invoice)
	
	sales_invoice.set("item",[
		{
			"item":item_name,
			"qty":qty,
			"amount":sales_invoice.total_amount
		}	
		])
	


	sales_invoice.insert()
	sales_invoice.save()
	return sales_invoice

@frappe.whitelist(allow_guest=True)
def delete_sales_invoice(invoice_name):
	sales_invoice = frappe.get_doc("Sales Invoice",invoice_name)
	sales_invoice.delete(ignore_permissions=True)
 


@frappe.whitelist(allow_guest=True)
def finalize_sales_invoice(invoice_name):
	sales_invoice = frappe.get_doc("Sales Invoice",invoice_name)
	sales_invoice.submit()

   
