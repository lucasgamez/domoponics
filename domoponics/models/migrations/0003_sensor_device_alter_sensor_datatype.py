# Generated by Django 4.1.7 on 2023-03-27 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_datatype_device_rename_data_type_sensor_datatype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='device',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='models.device'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sensor',
            name='dataType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.datatype'),
        ),
    ]