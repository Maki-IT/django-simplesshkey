# Generated by Django 4.2.5 on 2023-09-09 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simplesshkey', '0006_alter_userkey_fingerprint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkey',
            name='fingerprint',
            field=models.CharField(blank=True, db_index=True, max_length=128, null=True),
        ),
    ]