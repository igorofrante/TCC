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

function confirmar2(url){
  $.confirm({
      title: 'Confirmar ação',
      content: 'Deseja mesmo executar essa ação?',
      autoClose: 'CANCELAR|5000',
      buttons: {
          SIM:{
              keys: ['enter'],
              btnClass: 'btn-green',
              action: function(){
                  location.href = url
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
          console.log(data)
          data = data.split(',');
          console.log(data)
          res0 = String(data[0]);
          res1 = String(data[1]);
      
          console.log(data)

          if (res0 == res1){
            $("#id_payment " + "option[value=" +  res0 + "]").attr("selected", "selected");
            $('#estim').html('* Estimado por ambos');
          }else{
            if (res0 == 0){
              nr = "Adimplente"
            }else{
              nr = "Inadimplente"
            }
            if(res1 == 0){
              lr = "Adimplente"
            }else{
              lr = "Inadimplente"
            }
          
            $.confirm({
              title: 'Resultados diferentes',
              content: 'A rede neural estimou como um cliente ' + nr + ' e a regressão logísitica como um cliente ' + lr,
              autoClose: 'RN|20000',
              buttons: {
                  RN:{
                      text: 'Rede Neural',
                      btnClass: 'btn-primary',
                      action: function(res0){
                        $("#id_payment " + "option[value=" +  res0 + "]").attr("selected", "selected");
                        $('#estim').html('* Estimado pela Rede Neural');   
                      }
                  },
                  RL:{
                    text: 'Regressão Logística',
                    btnClass: 'btn-primary',
                    action: function(res1){
                      $("#id_payment " + "option[value=" +  res1 + "]").attr("selected", "selected");
                      $('#estim').html('* Estimado pela Regressão Logística');
                    }
                  }
              }
          });

            
          }

          

          
        }
      });
   }else{
    $.confirm({
      title: 'Campos Vazios',
        content: 'Há campos vazios, favor preencher todos os campos antes de utilizar a função estimar!',
        autoClose: 'tryAgain|10000',
        type: 'red',
        typeAnimated: true,
        buttons: {
          tryAgain: {
              text: 'Tente novamente',
              btnClass: 'btn-red',
              action: function(){
              }
          },
    }
    })
   }
}

$(document).ready(function (){ //mascara cpf
  $('#id_cpf').mask('000.000.000-00')
  $.ajax({
    type: "GET",
    url: "/refresh", 
  })
  if ($(".errorlist").length) {
    var cont;
    if(location.pathname == "/client/form") {
      cont = $('#form > ul > li > ul > li').html();
    }else{
      cont = $('div > form > ul > li > ul > li').html();
    }
    $.confirm({
      title: 'Error',
        content: cont,
        autoClose: 'tryAgain|10000',
        type: 'red',
        typeAnimated: true,
        buttons: {
          tryAgain: {
              text: 'Tente novamente',
              btnClass: 'btn-red',
              action: function(){
              }
          },
      }
    })
    }
})

