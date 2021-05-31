# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammed Yusuf Shaikh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import re
import frappe
# from frappe.model.document import Document
from frappe.utils.nestedset import NestedSet
class Company(NestedSet):
	
	def on_update(self):
		result = frappe.db.exists({
			'doctype':'Account',
			'company':self.name,
		})

		if result:
			print("account already exists")


		if not result:
			self.set_default_field()

		
	def set_default_field(self):
		frappe.db.set(self,'default_cash_account','Cash')
		frappe.db.set(self, 'default_payable_account', 'Debtors')
		frappe.db.set(self, 'default_receivable_account', 'Creditors')
		frappe.db.set(self, 'default_cost_of_goods_sold_account', 'Cost of Goods Sold')
		frappe.db.set(self, 'default_income_account', 'Sales')
		frappe.db.set(self,'default_inventory_account','Stock In Hand')
		frappe.db.set(self, 'stock_received_but_not_billed', 'Stock Received But Not Billed')

	