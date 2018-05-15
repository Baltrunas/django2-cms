from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions


from .models import Tag
from .models import Page
from .models import Block
from .models import SubBlock


class TagTranslationOptions(TranslationOptions):
	fields = ['name']

translator.register(Tag, TagTranslationOptions)


class PageTranslationOptions(TranslationOptions):
	fields = ['title', 'header', 'keywords', 'description', 'intro', 'text']

translator.register(Page, PageTranslationOptions)


class BlockTranslationOptions(TranslationOptions):
	fields = ['title', 'description', 'text']

translator.register(Block, BlockTranslationOptions)


class SubBlockTranslationOptions(TranslationOptions):
	fields = ['title', 'description', 'text']

translator.register(SubBlock, SubBlockTranslationOptions)
