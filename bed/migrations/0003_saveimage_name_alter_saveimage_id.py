# Generated by Django 4.2 on 2023-04-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bed', '0002_remove_saveimage_name_alter_saveimage_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='saveimage',
            name='name',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='saveimage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
