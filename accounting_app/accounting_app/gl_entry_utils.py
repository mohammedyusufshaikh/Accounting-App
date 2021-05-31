import frappe

def insert_gl_entry(self,account,dr,cr):
    gl_entry = frappe.new_doc('GL Entry')
    gl_entry.posting_date = self.posting_date
    gl_entry.account = account
    gl_entry.debit_amount = dr
    gl_entry.credit_amount = cr
    gl_entry.voucher_type = self.doctype
    gl_entry.voucher_no = self.name
    gl_entry.party = self.party
    gl_entry.company = self.company
    gl_entry.insert()

def reverse_gl_entry(self,voucher_no,voucher_type):
    gl_entry = frappe.get_all('GL Entry',filters={
        'voucher_no':voucher_no,
        'voucher_type':voucher_type
    },
    fields=["*"]
    )

    for entry in gl_entry:
        debit = entry.debit_amount
        credit = entry.credit_amount
        entry.debit_amount = credit
        entry.credit_amount = debit
        insert_cancelled_entry(entry)


def insert_cancelled_entry(entry):
    gl_entry = frappe.new_doc('GL Entry')
    gl_entry.update(entry)
    gl_entry.insert()