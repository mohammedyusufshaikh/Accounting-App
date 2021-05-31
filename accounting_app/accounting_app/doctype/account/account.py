# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammed Yusuf Shaikh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import re
from frappe.utils.nestedset import NestedSet

class Account(NestedSet):
	def validate(self):
		self.add_abbr_to_account()

	def add_abbr_to_account(self):
		doc = frappe.get_doc('Company',self.company)
		abbrevation = doc.abbr
		pattern = '-' + abbrevation
		if re.search(pattern,self.name):
			pass
		else:
			self.name = self.name + pattern