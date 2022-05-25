# Generated by Django 3.2.10 on 2022-05-23 12:45

from django.db import migrations, models
import django.db.models.deletion
import problem.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('score', models.DecimalField(decimal_places=3, default=0, max_digits=100)),
                ('rank', models.IntegerField(default=-1)),
                ('problems_tried', models.IntegerField(default=0, null=True)),
                ('problems_ac', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('link', models.URLField()),
                ('statement', models.TextField()),
                ('num_submission', models.IntegerField()),
                ('num_ac', models.IntegerField(default=0)),
                ('num_wa', models.IntegerField(default=0)),
                ('num_re', models.IntegerField(default=0)),
                ('num_tle', models.IntegerField(default=0)),
                ('num_ce', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('time_limit', models.IntegerField(default=1)),
                ('source', models.CharField(max_length=200)),
                ('num_tests', models.IntegerField(default=1)),
                ('author', models.CharField(default='admin', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_file', models.FileField(upload_to=problem.models.in_upload_path)),
                ('output_file', models.FileField(upload_to=problem.models.out_upload_path)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.problem')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NT', 'Not tested'), ('CE', 'Compile Error'), ('TL', 'Time Limit Exceed'), ('RE', 'Runtime Error'), ('AC', 'Accepted')], default='NT', max_length=2)),
                ('lang', models.CharField(choices=[('C', 'GNU C'), ('CPP', 'GNU C++')], default='C', max_length=4)),
                ('code', models.TextField(default='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('private', models.BooleanField(default=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.problem')),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.coder')),
            ],
        ),
    ]
