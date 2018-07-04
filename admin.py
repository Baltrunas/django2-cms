from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from django import forms
from django.db import models

from modeltranslation.admin import TranslationAdmin

from .models import Tag, Page, Block, Element, Settings, Redirect, Variable


class TagAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	search_fields = ['name', 'slug']

admin.site.register(Tag, TagAdmin)


class PageAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'url', 'public']
	search_fields = ['title', 'slug', 'url', 'public', 'text']
	list_filter = ['public', 'sites', 'parent']
	list_editable = ['public']
	# save_as = True


	fieldsets = (
		(_('Base'), {
			'fields': ('name', 'image', 'intro', 'text', 'tags'),
		}),
		(_('URL'), {
			'fields': ('sites', 'parent', 'slug',),
		}),
		(_('SEO'), {
			'classes': ('collapse',),
			'fields': ('title', 'header', 'keywords', 'description', 'head_code', 'footer_code'),
		}),
		(_('Settings'), {
			'classes': ('collapse',),
			'fields': ('sorting', 'template', 'per_page'),
		}),
	)

	formfield_overrides = {
		models.CharField: {'widget': forms.TextInput(attrs={'size':'95'})},
		models.TextField: {'widget': forms.Textarea(attrs={'rows':5, 'cols':95})},
	}


admin.site.register(Page, PageAdmin)


class ElementInline(admin.StackedInline):
	model = Element
	verbose_name = _('Element')
	verbose_name_plural = _('Elements')
	extra = 3

class BlockAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'sorting', 'public']
	search_fields = ['name', 'title', 'slug']
	list_filter = ['public', 'group', 'pages']
	list_editable = ['public', 'sorting']
	inlines = [ElementInline]

admin.site.register(Block, BlockAdmin)


class SettingsAdmin(admin.ModelAdmin):
	list_display = ['site', 'language']
	search_fields = ['site', 'language', 'robots_txt', 'sitemap_xml']
	list_filter = ['site', 'language']

admin.site.register(Settings, SettingsAdmin)


class RedirectAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'regex', 'public', 'created_at', 'updated_at']
	search_fields = ['from_domain', 'from_url', 'to_domain', 'to_url']
	list_filter = ['from_domain', 'to_domain', 'public', 'regex']
	list_editable = ['public', 'regex']

admin.site.register(Redirect, RedirectAdmin)


class ValiableForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ValiableForm, self).__init__(*args, **kwargs)
		if 'instance' in kwargs and kwargs['instance']:
			if kwargs['instance'].var_type == 'string':
				self.fields['value'] = forms.CharField(label=_('Value (string or int)'), max_length=128, required=True)
			elif kwargs['instance'].var_type == 'text':
				self.fields['value'] = forms.CharField(label=_('Text'), widget=forms.Textarea, required=False)
		else:
			self.fields['value'] = forms.CharField(label=_('Value (string or int)'), max_length=128, required=False, help_text=_('Safe for edit'))
			self.fields['value'].widget.attrs['readonly'] = True

	class Meta:
		model = Variable
		fields = ['site', 'name', 'key', 'var_type', 'value']


class VariableAdmin(admin.ModelAdmin): 
	list_display = ['name', 'site', 'var_type', 'key', 'get_value']
	search_fields = ['name', 'key', 'value']
	list_filter = ['var_type', 'site', 'key']

	form = ValiableForm

admin.site.register(Variable, VariableAdmin)
