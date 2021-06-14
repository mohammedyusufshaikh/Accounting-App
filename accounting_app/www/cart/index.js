frappe.ready(function(){
    let counter = 0;

    $("#pos").on("click",function(event){
        counter++;
       $("#val").val(counter);
    })

    $("#neg").on("click",function(event){
        counter--;
       $("#val").val(counter);
    })

    $(".delete-btn").on('click',function(event){
        $(event.currentTarget).prop('disabled',true);
        let invoice_data = $(event.currentTarget).data('invoice-no')
        console.log(invoice_data)
        if(frappe.session.user === 'Guest'){
            window.location.href ="/login"
        }

        else{
           frappe.call({
               method :'accounting_app.accounting_app.doctype.sales_invoice.sales_invoice.delete_sales_invoice',
               args:{
                invoice_name:invoice_data,
               },
               callback : (r)=>{
                $(".delete-btn").prop('disabled',false)
                frappe.msgprint({
                    title:'Success',
                     indicator:'green',
                     message:'Item Deleted Successfully'
                })
                }
               })
            }

    })

    $(".buynow-btn").on('click',function(event){
        $(event.currentTarget).prop('disabled',true);
        let invoice_data = $(event.currentTarget).data('invoice-no')
        console.log(invoice_data)
        if(frappe.session.user === 'Guest'){
            window.location.href ="/login"
        }

        else{
           frappe.call({
               method :'accounting_app.accounting_app.doctype.sales_invoice.sales_invoice.finalize_sales_invoice',
               args:{
                invoice_name:invoice_data,
               },
               callback : (r)=>{
                $(".buynow-btn").prop('disabled',false)
                frappe.msgprint({
                    title:'Success',
                     indicator:'green',
                     message:'Transaction Successfull Thanks for Shopping'
                })
                }
               })
            }

    })
})