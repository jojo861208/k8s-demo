# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-03 07:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('human', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemHuman',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.PositiveIntegerField(verbose_name='時數')),
                ('money', models.PositiveIntegerField(verbose_name='時薪')),
            ],
            options={
                'verbose_name': '人力清單',
                'verbose_name_plural': '人力清單',
            },
        ),
        migrations.AlterModelOptions(
            name='case',
            options={'verbose_name': '案件', 'verbose_name_plural': '案件'},
        ),
        migrations.AlterModelOptions(
            name='expertise',
            options={'verbose_name': '專長', 'verbose_name_plural': '專長'},
        ),
        migrations.AlterModelOptions(
            name='human',
            options={'verbose_name': '人力', 'verbose_name_plural': '人力'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': '項目', 'verbose_name_plural': '項目'},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'verbose_name': '技能', 'verbose_name_plural': '技能'},
        ),
        migrations.AlterField(
            model_name='case',
            name='description',
            field=models.TextField(null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='case',
            name='endTime',
            field=models.DateTimeField(null=True, verbose_name='結束時間'),
        ),
        migrations.AlterField(
            model_name='case',
            name='location',
            field=models.CharField(max_length=255, null=True, verbose_name='地點'),
        ),
        migrations.AlterField(
            model_name='case',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='標題'),
        ),
        migrations.AlterField(
            model_name='case',
            name='startTime',
            field=models.DateTimeField(null=True, verbose_name='開始時間'),
        ),
        migrations.AlterField(
            model_name='expertise',
            name='description',
            field=models.TextField(null=True, verbose_name='備註'),
        ),
        migrations.AlterField(
            model_name='expertise',
            name='human',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human.Human', verbose_name='人力'),
        ),
        migrations.AlterField(
            model_name='expertise',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human.Skill', verbose_name='技能'),
        ),
        migrations.AlterField(
            model_name='human',
            name='about',
            field=models.TextField(null=True, verbose_name='簡介'),
        ),
        migrations.AlterField(
            model_name='human',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='human',
            name='gender',
            field=models.IntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性別'),
        ),
        migrations.AlterField(
            model_name='human',
            name='img',
            field=models.ImageField(null=True, upload_to='static/img', verbose_name='照片'),
        ),
        migrations.AlterField(
            model_name='human',
            name='interest',
            field=models.TextField(null=True, verbose_name='興趣'),
        ),
        migrations.AlterField(
            model_name='human',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='human',
            name='phone',
            field=models.CharField(max_length=10, null=True, verbose_name='手機'),
        ),
        migrations.AlterField(
            model_name='item',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human.Case', verbose_name='案件'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(null=True, verbose_name='備註'),
        ),
        migrations.AlterField(
            model_name='item',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human.Skill', verbose_name='技能'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='description',
            field=models.TextField(null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='技能名'),
        ),
        migrations.AlterUniqueTogether(
            name='expertise',
            unique_together=set([('human', 'skill')]),
        ),
        migrations.RemoveField(
            model_name='item',
            name='humans',
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('case', 'skill')]),
        ),
        migrations.AddField(
            model_name='itemhuman',
            name='human',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human.Human', verbose_name='人力'),
        ),
        migrations.AddField(
            model_name='itemhuman',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human.Item', verbose_name='項目'),
        ),
        migrations.AlterUniqueTogether(
            name='itemhuman',
            unique_together=set([('item', 'human')]),
        ),
    ]
