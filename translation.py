from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions


from .models import Tag
from .models import Page
from .models import Block
from .models import Element
from .models import Media


class TagTranslationOptions(TranslationOptions):
	fields = ['name']

translator.register(Tag, TagTranslationOptions)


class PageTranslationOptions(TranslationOptions):
	fields = ['title', 'header', 'keywords', 'description', 'intro', 'text']

translator.register(Page, PageTranslationOptions)


class BlockTranslationOptions(TranslationOptions):
	fields = ['title', 'description', 'text', 'url']

translator.register(Block, BlockTranslationOptions)


class ElementTranslationOptions(TranslationOptions):
	fields = ['title', 'description', 'text']

translator.register(Element, ElementTranslationOptions)


class MediaTranslationOptions(TranslationOptions):
	fields = ['name', 'description', 'doc']

translator.register(Media, MediaTranslationOptions)


from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.db import models
from django import forms



class MediaInline(admin.StackedInline):
	model = Media
	verbose_name = _('Media')
	verbose_name_plural = _('Media')
	extra = 1


class PageAdmin(TranslationAdmin):
	list_display = ['__str__', 'url', 'public']
	search_fields = ['title', 'slug', 'url', 'public', 'text']
	list_filter = ['public', 'sites', 'parent']
	list_editable = ['public']
	inlines = [MediaInline]
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

	class Media:
		js = (
			'modeltranslation/js/force_jquery.js',
			'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
			'modeltranslation/js/tabbed_translation_fields.js',
		)
		css = {
			'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
		}

admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)
