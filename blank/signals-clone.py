# meuapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from blank.models import Member, Saldo

@receiver(post_save, sender=Member)
def update_saldo_on_member_creation(sender, instance, created, **kwargs):
    if created:
        update_saldo_on_member(instance)

@receiver(post_save, sender=Member)
def update_saldo_on_member_update(sender, instance, **kwargs):
    if instance.status == 'ganhou':
        update_saldo_on_member(instance)

def update_saldo_on_member(member_instance):
    casa = member_instance.casa
    valor = member_instance.valor
    status = member_instance.status

    # Ensure handling situations where the Saldo for the casa does not exist yet
    saldo_casa, created = Saldo.objects.get_or_create(casa=casa)

    if status == 'ganhou':
        saldo_casa.valor += valor
    else:
        saldo_casa.valor -= valor

    saldo_casa.save()

    print(f"{'Novo Member criado' if created else 'Aposta ganha'}: {member_instance} com valor de aposta/ganho: {valor}. Saldo atualizado para a casa {casa}: {saldo_casa.valor}")
