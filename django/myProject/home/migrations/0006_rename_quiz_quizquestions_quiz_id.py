# Generated by Django 5.0.2 on 2024-03-17 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_rename_question_id_quizchoices_question_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizquestions',
            old_name='quiz',
            new_name='quiz_id',
        ),
    ]
