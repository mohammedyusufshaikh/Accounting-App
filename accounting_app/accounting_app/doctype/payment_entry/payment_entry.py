# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammed Yusuf Shaikh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
# import frappe
from frappe.model.document import Document
from accounting_app.accounting_app.gl_entry_utils import insert_gl_entry,reverse_gl_entry

class PaymentEntry(Document):
	def validate(self):
		self.check_paid_amount()
	

	def on_submit(self):
		self.gl_entry()

	def on_cancel(self):
		reverse_gl_entry(self,self.name,self.doctype)

	def check_paid_amount(self):
		if self.paid_amount == '0':
			frappe.throw("paid amount should be greater than zero")


	def gl_entry(self):
		insert_gl_entry(self,self.account_paid_from,self.paid_amount,0)
		insert_gl_entry(self,self.account_paid_to,0,self.paid_amount)
		