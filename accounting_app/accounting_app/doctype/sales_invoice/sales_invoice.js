// Copyright (c) 2021, Mohammed Yusuf Shaikh and contributors
// For license information, please see license.txt
frappe.ui.form.on('Sales Invoice', {

	timeline_refresh: function(frm) {
		frm.add_custom_button('Make Payment', () => {
			let payment_entry = frappe.model.get_new_doc('Payment Entry');
			payment_entry.posting_date = frm.doc.posting_date
			payment_entry.payment_type = 'Receive'
			payment_entry.party_type = 'Customer'
			payment_entry.party = frm.doc.customer
			payment_entry.company = frm.doc.company
			payment_entry.account_paid_from  = frm.doc.debit_to
			payment_entry.account_paid_to = frm.doc.income_account
			payment_entry.paid_amount  = frm.doc.total_amount
			frappe.set_route('Form','Payment Entry',payment_entry.name);
		}, 'Actions');
	}

	,
	onload:function(frm){
		frm.set_query('customer',()=>{
			return {
				filters:{
					party_type:'Customer'
				}
			}
		})

		frm.set_query('debit_to',()=>{
			return {
				filters:{
					is_group:0,
					company:frm.doc.company
				}
			}
		})

		frm.set_query('income_to',()=>{
			return {
				filters:{
					is_group:0,
					company:frm.doc.company
				}
			}
		})
	}
	,
	company:function(frm){
		let cur_company = frm.doc.company
		// console.log(frappe.db.get_doc('Company',cur_company))
		frappe.db.get_doc('Company',cur_company).then(doc=>{
			frm.set_value('debit_to',doc.default_receivable_account);
			frm.set_value('income_account',doc.default_income_account);
		})
	}

});



frappe.ui.form.on('Sales_Invoice_Item', {
	qty: function(frm,cdt,cdn){
		calculate_total(frm, cdt, cdn);
	},
	rate: function(frm, cdt, cdn){
		calculate_total(frm, cdt, cdn);
	},

	item: function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		if(child.item){
			frappe.db.get_doc('Item', child.item)
			.then( doc =>{
				frappe.model.set_value(cdt, cdn, 'qty', 1.00)
				frappe.model.set_value(cdt, cdn, 'rate', doc.standard_selling_rate)
			})
		}
	}
	
	// form_render(frm,cdt,cdn){		
	// 	// let row = frappe.get_doc(cdt,cdn);
	// 	// row['amount'] = row['qty'] * row['rate'];
	// 	// console.log(row);
	// 	// frappe.model.set_value(cdt,cdn,'amount',row['amount']+"");
	// 	// console.log(total);
	// 	var d = locals[cdt][cdn];
	// 	frappe.model.set_value(d.doctype,d.name,"amount",d.qty*d.rate);
	// 	var total_amount = 0;
	// 	var total_qty = 0;
	// 	frm.doc.item.forEach(function(d){
	// 		total_amount += d.amount;
	// 		total_qty += d.qty;
	// 	});
	// 	frm.set_value('total_amount',total_amount);
	// 	frm.set_value('total_qty',total_qty);
	// }
});


var calculate_total = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "amount", child.qty * child.rate);
}

frappe.ui.form.on("Sales Invoice Item", "qty", function(frm, cdt, cdn) {
	var sales_item_details = frm.doc.items;
	var total = 0
	for(var i in sales_item_details) {
		total = total + sales_item_details[i].qty
	}
	frm.set_value("total_qty", total_qty)
});


frappe.ui.form.on("Sales Invoice Item", "amount", function(frm, cdt, cdn) {
	var sales_item_details = frm.doc.items;
	var total = 0
	for(var i in sales_item_details) {
		total = total + sales_item_details[i].amount
	}
	frm.set_value("total_amount", total_amount)
});