import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from django.core.exceptions import PermissionDenied
from django.views.defaults import permission_denied

from .models import BlogPage


class BlogAdmin(ModelAdmin):
    model = BlogPage
    menu_label = 'Articles'
    menu_icon = 'doc-full-inverse'
    menu_order = 000
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'owner')
    search_fields = ('title', 'owner')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #only show articles from the current user
        return qs.filter(owner=request.user)
    
modeladmin_register(BlogAdmin)


@hooks.register('before_edit_page')
def before_edit_page(request, page):
    # user_group = request.user.groups.filter(name='Author').exists() # I did not use user_group
    if not (request.user.is_superuser or page.owner == request.user):
        return permission_denied(request, PermissionDenied("You do not have permission to edit this page."))
    
    
@hooks.register('before_delete_page')
def before_delete_page(request, page):
    if not (request.user.is_superuser or page.owner == request.user):
        return permission_denied(request,PermissionDenied("You do not have permission to delete this page."))
    

@hooks.register('before_create_page')
def before_create_page(request, parent_page, page_class):
    if not (request.user.is_superuser or page_class == BlogPage):
        return permission_denied(request, PermissionDenied("You do not have permission to add this page."))


@hooks.register('register_rich_text_features')
def register_caption_feature(features):
    """
    Registering the `caption` feature, which uses the `CAPTION` Draft.js entity type,
    and is stored as HTML with a `<div>` tag.
    """
    feature_name = 'caption'
    type_ = 'CAPTION'
    tag = 'div'

    control = {
        'type': type_,
        'label': 'Caption',
        'description': 'Caption for images',
        'style': {
            'display': 'block',
            'text-align': 'center',
        },
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {
            'element': tag,
            'props': {
                'class': 'caption',
            }
        }}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)

    features.default_features.append(feature_name)