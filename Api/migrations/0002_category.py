# Generated by Django 4.0.5 on 2022-06-22 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('userid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.user')),
            ],
        ),
    ]
