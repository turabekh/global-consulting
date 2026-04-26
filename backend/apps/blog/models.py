import re

from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BlogPost(models.Model):
    class Category(models.TextChoices):
        GENERAL = "general", _("General")
        TOURISM = "tourism", _("Tourism")
        STUDY = "study", _("Study")
        WORK = "work", _("Work")
        VISA = "visa", _("Visa")

    title = models.CharField(_("title"), max_length=200)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=False)
    category = models.CharField(
        _("category"),
        max_length=16,
        choices=Category.choices,
        default=Category.GENERAL,
        db_index=True,
    )
    excerpt = models.TextField(
        _("excerpt"),
        max_length=300,
        blank=True,
        help_text=_("Short summary shown in cards. Plain text only."),
    )
    body = models.TextField(_("body"), help_text=_("Markdown is supported."))
    cover_image = models.ImageField(_("cover image"), upload_to="blog/")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    is_published = models.BooleanField(_("published"), default=False, db_index=True)
    published_at = models.DateTimeField(_("published at"), null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("blog post")
        verbose_name_plural = _("blog posts")
        ordering = ("-published_at", "-created_at")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def read_time_minutes(self) -> int:
        words = len(re.findall(r"\w+", self.body))
        return max(1, round(words / 200))
