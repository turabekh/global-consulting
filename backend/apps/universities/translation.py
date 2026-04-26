from modeltranslation.translator import TranslationOptions, register

from .models import University


@register(University)
class UniversityTranslationOptions(TranslationOptions):
    fields = ("title", "country", "city", "description", "body", "programs_offered")
