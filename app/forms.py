from django import forms 
from app.models import *
from localflavor.br.forms import BRCPFField 
from django.db.models.fields import BLANK_CHOICE_DASH

# Create your forms here.

statuspag = BLANK_CHOICE_DASH + [("10","Pagamento Integral"),("11","Pagamento Parcial"),("1","1 mês de atraso"),("2","2 meses de atraso"),("3","3 meses de atraso"),("4","4 meses de atraso"),("5","5 meses de atraso"),("6","6 meses de atraso"),("7","7 meses de atraso"),("8","8 meses de atraso"),("9","9 ou mais meses de atraso")]

class ClienteForm(forms.ModelForm):
    nomec = forms.CharField(label = "Nome Completo")
    cpf = BRCPFField(label = 'CPF')
    mit_bal = forms.IntegerField(label="Limite de crédito") 
    sex = forms.ChoiceField(label = "Gênero",choices=BLANK_CHOICE_DASH + [("1","Masculino"),("2","Feminino")])
    education = forms.ChoiceField(label = "Grau de Instrução",choices=BLANK_CHOICE_DASH + [("3","Ensino Médio Completo"),("2","Superior Completo"),("1","Pós Graduado"),("4","Outros")])
    marriage = forms.ChoiceField(label = "Estado Civil",choices=BLANK_CHOICE_DASH + [("2","Solteiro(a)"),("1","Casado(a)"),("3","Outros")])
    age = forms.IntegerField(label = "Idade")
    pay_6 = forms.ChoiceField(label = "Status de Pagamento 1",choices = statuspag)
    pay_5 = forms.ChoiceField(label = "Status de Pagamento 2",choices = statuspag)
    pay_4 = forms.ChoiceField(label = "Status de Pagamento 3",choices = statuspag)
    pay_3 = forms.ChoiceField(label = "Status de Pagamento 4",choices = statuspag)
    pay_2 = forms.ChoiceField(label = "Status de Pagamento 5",choices = statuspag)
    pay_1 = forms.ChoiceField(label = "Status de Pagamento 6",choices = statuspag)
    bill_amt_6 = forms.IntegerField(label= "Valor da Conta 1")
    bill_amt_5 = forms.IntegerField(label= "Valor da Conta 2") 
    bill_amt_4 = forms.IntegerField(label= "Valor da Conta 3") 
    bill_amt_3 = forms.IntegerField(label= "Valor da Conta 4")
    bill_amt_2 = forms.IntegerField(label= "Valor da Conta 5") 
    bill_amt_1 = forms.IntegerField(label= "Valor da Conta 6")
    pay_amt_6 = forms.IntegerField(label= "Pagamento 1")
    pay_amt_5 = forms.IntegerField(label= "Pagamento 2")
    pay_amt_4 = forms.IntegerField(label= "Pagamento 3")
    pay_amt_3 = forms.IntegerField(label= "Pagamento 4")
    pay_amt_2 = forms.IntegerField(label= "Pagamento 5")
    pay_amt_1 = forms.IntegerField(label= "Pagamento 6")
    payment = forms.ChoiceField(label= "Próximo Pagamento",choices= BLANK_CHOICE_DASH + [("0","Adimplente"),("1","Inadimplente")])
    class Meta:
        model = Cliente
        fields = '__all__'

class ClienteView(ClienteForm):
    pass
    def __init__(self, *args, **kwargs):
        super(ClienteView, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True




    

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.csv', '.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Extensão inválida')



class ClienteFile(forms.Form):
    file = forms.FileField(label="Selecione o arquivo de texto",validators=[validate_file_extension])

