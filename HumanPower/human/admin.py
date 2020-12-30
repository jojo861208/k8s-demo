#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.forms.models import BaseInlineFormSet
from django.template import loader, Context
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from human.models import *
from human.forms import *

class SkillAdmin(admin.ModelAdmin):
    list_display = ['name',]
    form = SkillForm

admin.site.register(Skill, SkillAdmin)

class ExpertiseInline(admin.TabularInline):
    model = Expertise
    extra = 0
    form = ExpertiseForm

class HumanAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'email', 'phone']
    form = HumanForm
    inlines = [ExpertiseInline,]
    search_fields = ['name',]



admin.site.register(Human, HumanAdmin)  

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    readonly_fields = ('humanLink', 'changeLink',)
    form = ItemInlineForm

    def changeLink(self, obj):
        if obj.id:
            return mark_safe('<a href="%s">編輯人力</a>' % \
                            reverse('admin:human_item_change',
                            args=(obj.id,)))
        else:
            return "-"

    changeLink.short_description = u"編輯"

    def humanLink(self, obj):
        if obj.id:
            itemHumans = obj.itemHumans
            t = loader.get_template('human/TotalTable.html')
            info = obj.info

            c = {
                'itemHumans': itemHumans,
                'totalHours': info['totalHours'],
                'averageMoney': info['averageMoney'],
                'averageHours': info['averageHours'],
                'totalMoney': obj.total,
            }
            return mark_safe(t.render(c))
        else:
            return "-"

    humanLink.short_description = u"已選定人力"

class CaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'startTime', 'endTime', 'location', 'caseTotal',]
    form = CaseForm
    search_fields = ['name',]
    inlines = [ItemInline,]
    readonly_fields = ('caseTotal',)

    def caseTotal(self, obj):
        if obj.id:
            return "%d 元" % obj.total
        return "-"

    caseTotal.short_description = u"案件總花費"


admin.site.register(Case, CaseAdmin) 

class ItemHumanFormSet(BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super(ItemHumanFormSet, self).get_form_kwargs(index)
        kwargs.update({'item': self.instance})
        return kwargs

class ItemHumanInline(admin.TabularInline):
    model = ItemHuman
    extra = 0
    form = ItemHumanForm
    readonly_fields = ('agree', 'view_moneyRequired', 'total')
    formset = ItemHumanFormSet

    def total(self, obj):
        if obj.id and obj.hours and obj.money:
            return "%d 元" % (obj.hours * obj.money)
        return "-"

    total.short_description = u"合計"

    def view_moneyRequired(self, obj):
        if obj.id:
            return "%d 元" % obj.moneyRequired
        return "-"

    view_moneyRequired.short_description = u"要求時薪"

class ItemAdmin(admin.ModelAdmin):
    list_display = ['case', 'skill',]
    form = ItemForm
    inlines = [ItemHumanInline,]

    fields = ('case', 'skill',)
    readonly_fields = ('case', 'skill',)


    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_post_save_change(self, request, obj):
        
        post_url = reverse('admin:human_case_change', args=(obj.case.id,))
        return HttpResponseRedirect(post_url)


admin.site.register(Item, ItemAdmin)