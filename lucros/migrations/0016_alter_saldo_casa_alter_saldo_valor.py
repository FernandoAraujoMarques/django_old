# Generated by Django 5.0 on 2023-12-19 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lucros', '0015_alter_saldo_casa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saldo',
            name='casa',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='saldo',
            name='valor',
            field=models.IntegerField(),
        ),
    ]