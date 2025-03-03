# Generated by Django 5.1.6 on 2025-02-24 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_message_media_alter_message_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='media',
        ),
        migrations.CreateModel(
            name='MessageMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='chat_media/')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_files', to='messaging.message')),
            ],
        ),
    ]
