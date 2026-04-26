from modeltranslation.translator import TranslationOptions, register

from .models import Job


@register(Job)
class JobTranslationOptions(TranslationOptions):
    fields = ("title", "country", "city", "industry", "description", "body")
