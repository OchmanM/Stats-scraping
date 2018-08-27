# Generated by Django 2.0.2 on 2018-08-08 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deaths',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('date', models.DateTimeField()),
                ('level', models.PositiveSmallIntegerField()),
                ('pvp', models.BooleanField()),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='OnlineDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('login', models.DateTimeField()),
                ('logout', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('logout', 'login'),
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guild', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=7)),
                ('level', models.PositiveSmallIntegerField()),
                ('vocation', models.CharField(choices=[('No Vocation', 'No Vocation'), ('Knight', 'Knight'), ('Paladin', 'Paladin'), ('Druid', 'Druid'), ('Sorcerer', 'Sorcerer'), ('Elite Knight', 'Elite Knight'), ('Royal Paladin', 'Royal Paladin'), ('Elder Druid', 'Elder Druid'), ('Master Sorcerer', 'Master Sorcerer')], max_length=50)),
                ('house', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('ONLINE', 'ONLINE'), ('OFFLINE', 'OFFLINE')], max_length=10)),
                ('lastlogin', models.DateTimeField()),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='onlinedetails',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.Player'),
        ),
        migrations.AddField(
            model_name='deaths',
            name='killed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='killed', to='stats.Player'),
        ),
        migrations.AddField(
            model_name='deaths',
            name='killer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='killer', to='stats.Player'),
        ),
    ]