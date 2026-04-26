from modeltranslation.translator import TranslationOptions, register

from .models import TourPackage


@register(TourPackage)
class TourPackageTranslationOptions(TranslationOptions):
    fields = ("title", "destination", "description", "body")
