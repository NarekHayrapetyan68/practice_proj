# Generated by Django 4.2.7 on 2023-12-06 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0009_alter_burger_options_alter_pizza_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='burger',
            old_name='burger_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='pizza',
            old_name='pizza_name',
            new_name='name',
        ),
    ]