import frappe

def get_context(context):
    context.items = frappe.db.get_list('Item',
                        fields=['item_name','item_code','brand',
                        'standard_selling_rate','item_image','route']
                        ,ignore_permissions=True)