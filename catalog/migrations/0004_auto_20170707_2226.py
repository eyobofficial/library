# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 19:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_return_book', 'Can return borrowed book'),), 'verbose_name': 'Book Copy', 'verbose_name_plural': 'Book Copies'},
        ),
    ]
