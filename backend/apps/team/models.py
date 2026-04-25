from django.db import models
from django.utils.translation import gettext_lazy as _


class TeamMember(models.Model):
    name = models.CharField(_("name"), max_length=120)
    role = models.CharField(_("role"), max_length=120)
    photo = models.ImageField(_("photo"), upload_to="team/", blank=True, null=True)
    bio = models.TextField(_("bio"), blank=True)
    order = models.PositiveIntegerField(_("order"), default=0)
    is_active = models.BooleanField(_("active"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("team member")
        verbose_name_plural = _("team members")
        ordering = ("order", "id")

    def __str__(self):
        return self.name
