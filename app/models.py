from django.db import models
from localflavor.br.models import BRCPFField

# Create your models here.

class Cliente(models.Model):
    nomec = models.CharField(max_length=200)
    cpf = BRCPFField(unique=True)
    mit_bal = models.IntegerField() 
    sex = models.PositiveSmallIntegerField()
    education = models.PositiveSmallIntegerField()
    marriage = models.PositiveSmallIntegerField()
    age = models.PositiveSmallIntegerField()
    pay_1 = models.SmallIntegerField()
    pay_2 = models.SmallIntegerField()
    pay_3 = models.SmallIntegerField()
    pay_4 = models.SmallIntegerField()
    pay_5 = models.SmallIntegerField()
    pay_6 = models.SmallIntegerField()
    bill_amt_1 = models.IntegerField() 
    bill_amt_2 = models.IntegerField() 
    bill_amt_3 = models.IntegerField() 
    bill_amt_4 = models.IntegerField() 
    bill_amt_5 = models.IntegerField() 
    bill_amt_6 = models.IntegerField()
    pay_amt_1 = models.IntegerField()
    pay_amt_2 = models.IntegerField()
    pay_amt_3 = models.IntegerField()
    pay_amt_4 = models.IntegerField()
    pay_amt_5 = models.IntegerField()
    pay_amt_6 = models.IntegerField()
    payment = models.SmallIntegerField()
    class Meta:
        db_table = "cliente"  
