from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions


from .models import Tag
from .models import Page
from .models import Block
from .models import Element


class TagTranslationOptions(TranslationOptions):
	fields = ['name']

translator.register(Tag, TagTranslationOptions)


class PageTranslationOptions(TranslationOptions):
	fields = ['title', 'header', 'keywords', 'description', 'intro', 'text']

translator.register(Page, PageTranslationOptions)


class BlockTranslationOptions(TranslationOptions):
	fields = ['title', 'description', 'text']

translator.register(Block, BlockTranslationOptions)


class ElementTranslationOptions(TranslationOptions):
	fields = ['title', 'description', 'text']

translator.register(Element, ElementTranslationOptions)
