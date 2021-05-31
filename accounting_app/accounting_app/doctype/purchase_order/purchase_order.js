// Copyright (c) 2021, Mohammed Yusuf Shaikh and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Order', {
	// refresh: function(frm) {

	// }

	onload:function(frm){
		frm.set_query('supplier',()=>{
			return {
				filters:{
					party_type:'Supplier'
				}
			}
		});
	
	}
	,
	before_save:function(frm){
		
	}
});


frappe.ui.form.on('Purchase_Order_Item', {

	form_render:function(frm,cdt,cdn){		
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
