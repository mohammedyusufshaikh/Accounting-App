# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammed Yusuf Shaikh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SalesInvoice(Document):
	def validate(self):
		self.validate_quantity()

	def validate_quantity(self):
		for data in self.item:
			if data.qty <=0:
				frappe.throw("product quantity should be at least 1")