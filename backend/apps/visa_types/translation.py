from modeltranslation.translator import TranslationOptions, register

from .models import VisaType


@register(VisaType)
class VisaTypeTranslationOptions(TranslationOptions):
    fields = ("title", "country", "description", "body", "processing_time")
