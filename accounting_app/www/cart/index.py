import frappe

def get_context(context):
	si = frappe.db.sql(""" SELECT
					name
				FROM
					`tabSales Invoice`
				WHERE
					customer='Raj' and docstatus=0
				ORDER BY 
					modified desc""", as_dict=1)
	
	si_item = frappe.db.sql("""SELECT * 
							FROM `tabSales_Invoice_Item`
							WHERE parent=%s;
							""",si[0].name, as_dict=1)
	
	item_name = si_item[0].item

	item_d = frappe.db.sql("""SELECT * 
							FROM `tabItem`
							WHERE item_name=%s
							;
							""",item_name, as_dict=1)
	if si:
		context.cart = frappe.get_doc('Sales Invoice',si[0].name)
		context.items = si_item
		context.detail = item_d
	return context
