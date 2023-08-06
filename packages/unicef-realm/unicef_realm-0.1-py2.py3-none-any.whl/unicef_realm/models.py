from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext as _

from django_countries.fields import CountryField

app_label = 'unicef_realm'


class TimeStampedModel:
    last_modify_date = models.DateTimeField(editable=False, blank=True, auto_now_add=True,
                                            auto_now=True)


class Region(models.Model, TimeStampedModel):
    code = models.CharField(_('code'), max_length=10, unique=True)
    name = models.CharField(_('name'), max_length=50, unique=True)

    class Meta:
        app_label = 'unicef_realm'

    def __str__(self):
        return f"{self.name}"


class BusinessArea(models.Model, TimeStampedModel):
    code = models.CharField(_('code'), max_length=10, unique=True)
    name = models.CharField(_('name'), max_length=50, unique=True)
    long_name = models.CharField(_('long name'), max_length=150)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    country = CountryField()

    class Meta:
        app_label = 'unicef_realm'
        verbose_name = _('Business Area')
        verbose_name_plural = _('Business Areas')

    def __str__(self):
        return f"{self.name}"


class UserRoleManager(models.Manager):

    def by_permissions(self, perms_name):
        if not isinstance(perms_name, (set, list)):
            perms_name = perms_name,
        for perm_name in perms_name:
            app_label, codename = perm_name.split('.')
            self = self.filter(group__permissions__codename=codename,
                               group__permissions__content_type__app_label=app_label)
        return self

    def get_permissions_by_target(self, user, target):
        return self.filter(user=user, target=target).values_list(
            'group__permissions__content_type__app_label',
            'group__permissions__codename')


class UserRole(models.Model, TimeStampedModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='roles', on_delete=models.deletion.CASCADE)
    group = models.ForeignKey(Group, related_name='roles', on_delete=models.deletion.CASCADE)
    target = models.ForeignKey(settings.REALM_TARGET_MODEL, related_name='roles', on_delete=models.deletion.CASCADE)
    objects = UserRoleManager()

    class Meta:
        app_label = 'unicef_realm'
        ordering = ['group', 'target']
        verbose_name = _('User Role')
        verbose_name_plural = _('User Roles')
        unique_together = (('user', 'group', 'target'),)

    def __str__(self):
        return f'{self.user} | {self.group} | {self.target}'
