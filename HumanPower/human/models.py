#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum, Avg
from django.contrib.gis.db import models as gisModels
from django.contrib.auth import get_user_model

# Create your models here.
GENDER_CHOICES = (
    (0, '男'),
    (1, '女'),
)


class Human(models.Model):
    name = models.CharField(verbose_name=u"姓名", max_length=255, db_index=True)
    email = models.EmailField(verbose_name=u"Email", null=True)
    phone = models.CharField(verbose_name=u"手機", max_length=10, null=True)
    gender = models.IntegerField(verbose_name=u"性別", choices=GENDER_CHOICES, default=0)
    about = models.TextField(verbose_name=u"簡介", null=True)
    interest = models.TextField(verbose_name=u"興趣", null=True)
    img = models.ImageField(verbose_name=u"照片", upload_to='static/img', null=True)
    coordinates = gisModels.PointField(verbose_name=u"希望工作地點", null=True)

    user = models.ForeignKey(
        get_user_model(),
        null=True,
    )
    
    class Meta:
        verbose_name = u"人力"
        verbose_name_plural = u"人力"

    def __str__(self):
        return self.name

    @property
    def getGender(self):
        if self.gender == 0:
            return '男'
        else:
            return '女'

class Skill(models.Model):
    name = models.CharField(verbose_name=u"技能名", max_length=255, db_index=True, unique=True)
    description = models.TextField(verbose_name=u"描述", null=True)

    class Meta:
        verbose_name = u"技能"
        verbose_name_plural = u"技能"
    
    def __str__(self):
        return self.name

class Expertise(models.Model):
    human = models.ForeignKey(
        Human,
        on_delete=models.CASCADE,
        verbose_name=u"人力", 
    )
    skill =  models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name=u"技能", 
    )
    description = models.TextField(verbose_name=u"備註", null=True)

    def __str__(self):
        return self.skill.name

    class Meta:
        verbose_name = u"專長"
        verbose_name_plural = u"專長"
        unique_together = ("human", "skill")

class Case(models.Model):
    name = models.CharField(verbose_name=u"標題", max_length=255, db_index=True)
    startTime = models.DateTimeField(verbose_name=u"開始時間", null=True)
    endTime = models.DateTimeField(verbose_name=u"結束時間", null=True)
    location = gisModels.PointField(verbose_name=u"工作地點", null=True)
    description = models.TextField(verbose_name=u"描述", null=True)

    @property
    def total(self):
        itemHumans = ItemHuman.objects.filter(item__case=self)

        totalMoney = 0
        for ih in itemHumans:
            totalMoney += ih.total

        return totalMoney

    @property
    def items(self):
        return Item.objects.filter(case=self)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"案件"
        verbose_name_plural = u"案件"

class Item(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        verbose_name=u"案件",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name=u"技能", 
    )
    
    description = models.TextField(verbose_name=u"備註", null=True)

    def __str__(self):
        return self.skill.name

    @property
    def itemHumans(self):
        return ItemHuman.objects.filter(item=self, agree=True, selected=True)

    @property
    def total(self):
        itemHumans = self.itemHumans

        totalMoney = 0
        for ih in itemHumans:
            totalMoney += ih.total

        return totalMoney


    @property
    def info(self):
        itemHumans = self.itemHumans
        itemHumanCount = itemHumans.count()
        totalHours = itemHumans.aggregate(Sum('hours'))["hours__sum"]
        averageHours = itemHumans.aggregate(Avg('hours'))["hours__avg"]
        averageMoney = itemHumans.aggregate(Avg('money'))["money__avg"]
        
        info = {
            'totalHours': totalHours if totalHours else 0,
            'averageMoney': averageMoney if averageMoney else 0,
            'averageHours': averageHours if averageHours else 0,
        }
        return info

    class Meta:
        verbose_name = u"項目"
        verbose_name_plural = u"項目"
        unique_together = ("case", "skill")

class ItemHuman(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name=u"項目", 
    )
    human = models.ForeignKey(
        Human,
        on_delete=models.CASCADE,
        verbose_name=u"人力", 
    )

    moneyRequired = models.PositiveIntegerField(verbose_name="要求時薪")
    hours = models.PositiveIntegerField(verbose_name="時數", null=True)
    money = models.PositiveIntegerField(verbose_name="時薪", null=True)

    agree = models.BooleanField(verbose_name="同意", default=False)
    selected = models.BooleanField(verbose_name="選定", default=False)
    
    @property
    def total(self):
        if self.hours and self.money and self.agree and self.selected:
            return self.hours * self.money
        else:
            return 0

    @property
    def total2(self):
        if self.hours and self.money:
            return self.hours * self.money
        else:
            return 0

    @property
    def allagree(self):
        if self.agree and self.selected:
            return True
        else:
            return False

    def __str__(self):
        return self.human.name

    class Meta:
        verbose_name = u"人力清單"
        verbose_name_plural = u"人力清單"
        unique_together = ("item", "human")

