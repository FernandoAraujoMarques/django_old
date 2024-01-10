from django.db import models
from django.forms import ModelForm

STATUS_CHOISES = (
  ('p','Pendente'),
  ('g','Ganhou'),
  ('pd','Perdeu')
)

class Teste(models.Model):
  data = models.DateField()

  def __str__(self):
    return f"{self.data}"

class Member(models.Model):
  data = models.DateField()
  hora = models.TimeField()
  casa = models.CharField(max_length=255)
  valor = models.DecimalField(max_digits=10, decimal_places=2)
  odd = models.FloatField()
  ganho = models.DecimalField(max_digits=5, decimal_places=2)
  status = models.CharField(max_length=20,choices=[('ganhou', 'Ganhou'), ('perdeu', 'Perdeu'), ('pendente', 'Pendente')])


  def __str__(self):
    return f"{self.casa} {self.data} {self.ganho}"

class Saldo(models.Model):
  casa = models.CharField(max_length=255)
  valor = models.IntegerField()

  def __str__(self):
    return f"{self.casa} {self.valor}"

class Aposta(models.Model):
    # Outros campos do modelo
  ganho = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Teste2(models.Model):
  data = models.DateField()

  def __str__(self):
    return f"{self.data}"