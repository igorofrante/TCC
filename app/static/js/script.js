$(document).ready(function(){
  $('#button-index').on('click', function() {
    $(this).html('<div class="spinner-border text-light" role="status"></div>');})
});


$(document).ready(function() {
  $('.spinner-border').hide();
  $('table').show();
});

function confirmar(url){
  $.confirm({
      title: 'Confirmar ação',
      content: 'Deseja mesmo executar essa ação?',
      autoClose: 'CANCELAR|5000',
      buttons: {
          SIM:{
              keys: ['enter'],
              btnClass: 'btn-green',
              action: function(){
                  $.ajax({
                      url: url,
                      success: function () {
                          location.reload();
                      }
                    });
              }
          },
          CANCELAR:{
              keys: ['esc'],
              btnClass: 'btn-red any-other-class'
          }
      }
  });
}

function ajaxe() {
    cols = ['mit_bal','sex','education','marriage','age','pay_1','pay_2','pay_3','pay_4','pay_5','pay_6','bill_amt_1','bill_amt_2','bill_amt_3','bill_amt_4','bill_amt_5','bill_amt_6','pay_amt_1','pay_amt_2','pay_amt_3','pay_amt_4','pay_amt_5','pay_amt_6']
    values = []

   for (let index = 0; index < cols.length; index++) {
        values[index] = $("#id_"+cols[index]).val();
   }

   url = "/cliente/ajax"

  
   if (!values.includes('')) {
    $.ajax({
      url: url,
      data: {
        values : JSON.stringify(values)
      },
      success: function (data) {
          $("#id_payment " + "option[value=" +  data + "]").attr("selected", "selected");
        }
      });
   }else{
    alert('Há campos vazios, favor preencher todos os campos antes de utilizar a função estimar!')
   }
}

$(document).ready(function (){ //mascara cpf
  $('#id_cpf').mask('000.000.000-00')
})


