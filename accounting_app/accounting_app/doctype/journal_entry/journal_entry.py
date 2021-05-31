# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammed Yusuf Shaikh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting_app.accounting_app.gl_entry_utils import insert_gl_entry,reverse_gl_entry
class JournalEntry(Document):
	def validate(self):
		self.calculate_total_debit_and_credit()

		if self.difference:
			frappe.throw("Difference between total debit and total credit must be zero")

	def on_submit(self):
		for data in self.accounting_entries:
			insert_gl_entry(self,data.account,data.debit,data.credit)
		

	def on_cancel(self):
		reverse_gl_entry(self,self.name,self.doctype)


	def calculate_total_debit_and_credit(self):
		self.total_credit,self.total_debit,self.difference =0,0,0
		for data in self.accounting_entries:
			self.total_debit = self.total_debit + data.debit
			self.total_credit = self.total_credit + data.credit
		
		self.difference = self.total_debit - self.total_credit

		

