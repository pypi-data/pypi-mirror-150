from logging import getLogger
from typing import Dict, Union, List, Callable, Type

from django.db.models import Model  # FIXME could be a problem during migrations
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from menu import MenuItem as SimpleMenuItem
from turbo.components import BaseComponent

logger = getLogger(__file__)


class MenuItem(SimpleMenuItem):
    """MedUX MenuItem with permission check.

    :param required_permission list|str: You can provide a list or a
        string as required permission for this menu item. If the user
        doesn't have that permission, the menu item will be invisible.
    :param classes: the CSS classes that will be added to the menu item
    :param badge: TurboDjango component that is rendered as text. This
        will be displayed and updated as badge pill.
    :param view_name: the name of the view where this MenuItem should
        be visible, e.g. "namespace:index".
    """

    def __init__(
        self,
        *args,
        required_permissions: list[str] | str | None = None,
        classes: str = None,
        # badge: str | Callable | BroadcastComponent = None,
        badge: Type[BaseComponent] = None,
        disabled: bool | Callable = False,
        view_name="",
        **kwargs,
    ):
        if required_permissions is None:
            required_permissions = []
        elif not type(required_permissions) == list:
            required_permissions = [required_permissions]
        self.required_permissions = required_permissions
        self.classes = classes

        self.badge_component = None
        self.badge = None
        # if a badge component is given, save the class as reference
        # for instantiation later
        if badge:
            if isinstance(badge, type) and issubclass(badge, BaseComponent):
                self.badge_component = badge
            self.badge = badge

        self.view_name = view_name
        self.disabled = disabled
        super().__init__(*args, **kwargs)

    def process(self, request: HttpRequest):
        if self.view_name:
            self.visible = request.resolver_match.view_name == self.view_name
            if not self.visible:
                return
        if self.badge_component:
            if request.user is None:
                raise Exception("Foo!")
            self.badge = self.badge_component(request.user)
        elif callable(self.badge):
            self.badge = self.badge(request)
        if callable(self.disabled):
            self.disabled = self.disabled(request)
        super().process(request)


class MenuSeparator(MenuItem):
    def __init__(self):
        super().__init__(title="", url="#", separator=True)


def create_groups_permissions(
    groups_permissions: Dict[str, Dict[Union[Model, str], List[str]]]
):
    """Creates groups and their permissions defined in given `groups_permissions` automatically.

    :param groups_permissions: a dict, see also `MeduxPluginAppConfig.groups_permissions`

    Based upon the work here: https://newbedev.com/programmatically-create-a-django-group-with-permissions

    """
    from django.apps import apps
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    for group_name in groups_permissions:

        # Get or create group
        # Translators: group name
        group, created = Group.objects.get_or_create(name=_(group_name))
        if created:
            group.save()

        # Loop models in group
        for model in groups_permissions[group_name]:
            # if model_class is written as dotted str, convert it to class
            if type(model) is str:
                model_class = apps.get_model(model)
            else:
                model_class = model

            # Loop permissions in group/model

            for perm_name in groups_permissions[group_name][model]:

                # Generate permission name as Django would generate it
                codename = f"{perm_name}_{model_class._meta.model_name}"

                try:
                    # Find permission object and add to group
                    content_type = ContentType.objects.get(
                        app_label=model_class._meta.app_label,
                        model=model_class._meta.model_name.lower(),
                    )
                    perm = Permission.objects.get(
                        content_type=content_type,
                        codename=codename,
                    )
                    group.permissions.add(perm)
                    logger.info(
                        f"  Adding permission '{codename}' to group '{group.name}'"
                    )
                except Permission.DoesNotExist:
                    logger.critical(f"  ERROR: Permission '{codename}' not found.")
