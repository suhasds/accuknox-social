from apps.commons.constants import *
from django.contrib.auth.models import Permission

def configure_groups_and_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group

    # create groups
    user_group = Group.objects.get_or_create(name=UserGroup.SampleGroup.value)[0]

    # associate permissions to the owners
    all_permissions = Permission.objects.all()
    for permission in all_permissions:
        user_group.permissions.add(permission)
        user_group.save()
