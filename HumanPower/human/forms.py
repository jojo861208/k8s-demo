#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from crispy_forms.bootstrap import InlineField, FormActions, StrictButton, Div
from crispy_forms.layout import Layout
from crispy_forms import bootstrap, layout
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticOverlayMapWidget

from human.models import *

# admin.py ---------------------------------------------------------------------
class HumanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HumanForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].required = False
        self.fields['phone'].required = False
        self.fields['about'].required = False
        self.fields['interest'].required = False
        self.fields['img'].required = False
        
        
    class Meta:
        model = Human
        fields = [
            'name',
            'gender',
            'phone', 
            'email', 
            
            'about', 
            'interest', 
            'img',
            'coordinates',
            
        ]
        
        labels = {
            'name': "姓名",
            'img': "照片",
            
            'phone': "電話", 
            'email': "Email", 
            'gender': "性別", 
            
            'about': "簡介", 
            'interest': "興趣", 
        }
       
        widgets = {
            'coordinates': GooglePointFieldWidget,
        }
        

class ExpertiseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExpertiseForm, self).__init__(*args, **kwargs)

        self.fields['description'].required = False

    class Meta:
        model = Expertise
        fields = [
            'human',
            'skill',
            'description',
        ]
        labels = {
            'human': "人力",
            'skill': "技能",       
            'description': "備註", 
        }

BaseExpertiseInlineFormSet = inlineformset_factory(
    Human, Expertise, form=ExpertiseForm, extra=2)

class ExpertiseInlineFormSet(BaseExpertiseInlineFormSet):

    def __init__(self, human, *args, **kwargs):
        super(ExpertiseInlineFormSet, self).__init__(*args, **kwargs)

class SkillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        self.fields['description'].required = False

    class Meta:
        model = Skill
        fields = [
            'name',
            'description',
        ]
        labels = {
            'name': "技能名",  
            'description': "備註", 
        }

class CaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)

        self.fields['description'].required = False

    class Meta:
        model = Case
        fields = [
            'name',
            'startTime',
            'endTime',
            'location',
            'description',
        ]
        labels = {
            'name': "標題", 
            'startTime': "開始時間",
            'endTime': "結束時間",
            'description': "備註", 
        }
        widgets = {
            'location': GooglePointFieldWidget,
        }

class ItemInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemInlineForm, self).__init__(*args, **kwargs)

        self.fields['description'].required = False

    class Meta:
        model = Item
        fields = [
            'skill',
            'description',
        ]
        labels = {
            'skill': "技能",
            'description': "備註",
        }

class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Item
        fields = [
            'case',
            'skill',
        ]
        labels = {
            'case': "案件",
            'skill': "技能",
        }


class ItemHumanForm(forms.ModelForm):
    def __init__(self, item, *args, **kwargs):
        super(ItemHumanForm, self).__init__(*args, **kwargs)
        #self.fields['human'].queryset = Human.objects.filter(expertise__skill=item.skill)
        self.fields['human'].queryset = Human.objects.all()
        self.fields['hours'].required = False
        self.fields['money'].required = False
        
    class Meta:
        model = ItemHuman
        fields = [
            'item',
            'human',
            'hours',
            'money',
            'selected',
        ]
        labels = {
            'item': "項目",
            'human': "人力",
            'hours': "時數",
            'money': "時薪",
        }

# views.py ---------------------------------------------------------------------

        