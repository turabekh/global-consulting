from django.db import models
from django.utils.translation import gettext_lazy as _


class Testimonial(models.Model):
    author_name = models.CharField(_("author name"), max_length=120)
    author_city = models.CharField(_("author city"), max_length=120, blank=True)
    author_photo = models.ImageField(
        _("author photo"), upload_to="testimonials/", blank=True, null=True
    )
    body = models.TextField(_("body"), help_text=_("Markdown is supported. Use **text** for bold."))
    order = models.PositiveIntegerField(_("order"), default=0)
    is_active = models.BooleanField(_("active"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("testimonial")
        verbose_name_plural = _("testimonials")
        ordering = ("order", "-created_at")

    def __str__(self):
        return f"{self.author_name} ({self.author_city})" if self.author_city else self.author_name
