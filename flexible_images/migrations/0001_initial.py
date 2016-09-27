# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlexibleImageTestImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('plain_file', models.FileField(null=True, upload_to=b'', blank=True)),
            ],
        ),
    ]
