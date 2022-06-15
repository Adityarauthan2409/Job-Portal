# Generated by Django 3.0.6 on 2022-05-28 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_auto_20220527_0822'),
    ]

    operations = [
        migrations.CreateModel(
            name='apply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(null=True, upload_to='')),
                ('applydate', models.DateField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Recruiter')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.StudentUser')),
            ],
        ),
    ]
