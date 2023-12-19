# meuapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from lucros.models import Member, Saldo  # Certifique-se de ajustar isso para o caminho correto do seu modelo

@receiver(post_save, sender=Member)
def novo_member_criado(sender, instance, created, **kwargs):
    if created:
        # Subtrair o valor da aposta do saldo da casa
        casa = instance.casa
        valor_aposta = instance.valor
        status = instance.status

        # Certifique-se de lidar com situações em que o Saldo para a casa ainda não existe
        saldo_casa, created = Saldo.objects.get_or_create(casa=casa)

        # Atualizar o saldo subtraindo o valor da aposta
        saldo_casa.valor -= valor_aposta
        saldo_casa.save()

        print(f"Novo Member criado: {instance} com valor de aposta: {valor_aposta}. Saldo atualizado para a casa {casa}: {saldo_casa.valor}")

@receiver(post_save, sender=Member)
def member_atualizado(sender, instance, **kwargs):
    if instance.status == 'ganhou':
        casa_ganhadora = instance.casa
        valor_ganho = instance.valor

        # Certifique-se de lidar com situações em que o Saldo para a casa ganhadora ainda não existe
        saldo_casa_ganhadora, created = Saldo.objects.get_or_create(casa=casa_ganhadora)

        # Atualizar o saldo adicionando o valor ganho
        saldo_casa_ganhadora.valor += valor_ganho
        saldo_casa_ganhadora.save()

        print(f"Aposta ganha: {instance}. Saldo atualizado para a casa {casa_ganhadora}: {saldo_casa_ganhadora.valor}")
