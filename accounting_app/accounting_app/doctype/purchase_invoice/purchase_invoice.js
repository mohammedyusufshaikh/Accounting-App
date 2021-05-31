// Copyright (c) 2021, Mohammed Yusuf Shaikh and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {

	timeline_refresh: function(frm) {
		frm.add_custom_button('Make Payment', () => {
			let payment_entry = frappe.model.get_new_doc('Payment Entry');
			payment_entry.posting_date = frm.doc.posting_date
			payment_entry.payment_type = 'Pay'
			payment_entry.party_type = 'Supplier'
			payment_entry.party = frm.doc.supplier
			payment_entry.company = frm.doc.company
			payment_entry.account_paid_from  = frm.doc.credit_to
			payment_entry.account_paid_to = frm.doc.expense_account
			payment_entry.paid_amount  = frm.doc.total_amount
			frappe.set_route('Form','Payment Entry',payment_entry.name);
		}, 'Actions');
	}
	,
	onload:function(frm){
		frm.set_query('supplier',()=>{
			return {
				filters:{
					party_type:'Supplier'
				}
			}
		})

	}
	,
	company:function(frm){
		let cur_company = frm.doc.company
		frappe.db.get_doc('Company',cur_company).then(doc=>{
			frm.set_value('credit_to',doc.default_payable_account);
			frm.set_value('expense_account',doc.stock_received_but_not_billed);
		})
	}

});


frappe.ui.form.on('Purchase_Invoice_Item', {
	form_render(frm,cdt,cdn){		
		var d = locals[cdt][cdn];
		frappe.model.set_value(d.doctype,d.name,"amount",d.qty*d.rate);
		var total_amount = 0;
		var total_qty = 0;
		frm.doc.item.forEach(function(d){
			total_amount += d.amount;
			total_qty += d.qty;
		});
		frm.set_value('total_amount',total_amount);
		frm.set_value('total_qty',total_qty);

	}
});
