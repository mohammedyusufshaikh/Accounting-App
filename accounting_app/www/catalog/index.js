frappe.ready(function(){
    $(".cart-btn").on('click',function(event){
        $(event.currentTarget).prop('disabled',true);
        let item = $(event.currentTarget).data('item-name')
        if(frappe.session.user === 'Guest'){
            window.location.href ="/login"
        }

        else{
           frappe.call({
               method :'accounting_app.accounting_app.doctype.sales_invoice.sales_invoice.create_sales_invoice',
               args:{
                item_name : item,
                qty:1
               },
               callback : (r)=>{
                $(".cart-btn").prop('disabled',false)
                frappe.msgprint({
                    title:'Success',
                     indicator:'green',
                     message:'Item successfully added to you cart'
                })
                }
               })
             
            }
    })
})