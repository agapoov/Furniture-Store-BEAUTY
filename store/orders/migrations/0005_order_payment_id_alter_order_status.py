# Generated by Django 4.0 on 2024-10-01 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ID платежа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'В обработке'), ('paid', 'Оплачено'), ('shipped', 'Отправлено'), ('completed', 'Завершено'), ('canceled', 'Отменено')], default='processing', max_length=50, verbose_name='Статус заказа'),
        ),
    ]
