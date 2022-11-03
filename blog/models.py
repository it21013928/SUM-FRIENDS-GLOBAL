from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtailmetadata.models import MetadataPageMixin
# from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from taggit.models import Tag


class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("blog.BlogPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
    	# Use a SnippetChooserPanel because blog.BlogAuthor is registered as a snippet
        SnippetChooserPanel("author"),
    ]


@register_snippet
class BlogAuthor(models.Model):
    """Blog author for snippets."""

    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=500)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                # Use an ImageChooserPanel because wagtailimages.Image (image property) 
                # is a ForeignKey to an Image
                ImageChooserPanel("image"),
                FieldPanel("bio"),
            ],
            heading="Name, Image and Bio",
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links"
        )
    ]

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:  # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"


class BlogIndexPage(MetadataPageMixin, Page):
    max_count = 1
    intro = RichTextField(blank=True)

    subpage_types = [
        'blog.BlogPage',  # appname.ModelName
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        # Get all posts
        blogpages = self.get_children().live().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        paginator = Paginator(blogpages, 2)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            blogpages = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            blogpages = paginator.page(paginator.num_pages)
        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        tags = Tag.objects.all()
        context['blogpages'] = blogpages
        context['tags'] = tags
        context["categories"] = BlogCategory.objects.all()
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(MetadataPageMixin, Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    # def main_image(self):
    #     gallery_item = self.gallery_images.first()
    #     if gallery_item:
    #         return gallery_item.image
    #     else:
    #         return None
    # This function was used for fetch only first image from gallery images related to the post.

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=1)
            ],
            heading="Author(s)"
        ),
        FieldPanel('intro'),
        FieldPanel('body'),
        ImageChooserPanel('banner_image'),
        # InlinePanel('gallery_images', label="Gallery images"),
    ] 

    subpage_types = []


class BlogTagIndexPage(MetadataPageMixin, Page):
    max_count = 1
    subpage_types = []
    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        tags = Tag.objects.all()

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        context['tags'] = tags
        return context


# class BlogPageGalleryImage(Orderable):
#     page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
#     image = models.ForeignKey(
#         'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
#     )
#     caption = models.CharField(blank=True, max_length=250)

#     panels = [
#         ImageChooserPanel('image'),
#         FieldPanel('caption'),
#     ]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
    )
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "blog category"
        verbose_name_plural = 'blog categories'
        ordering = ["name"]


class BlogCategoryIndexPage(MetadataPageMixin, Page):
    max_count = 1
    subpage_types = []
    def get_context(self, request):

        # Filter by category
        category = request.GET.get('category')

        if(category==''):
            context = super().get_context(request)
            context["categories"] = BlogCategory.objects.all()[:3]
            return context

        blogpages = BlogPage.objects.filter(categories__name=category)

        # Update template context
        context = super().get_context(request)
        context["categories"] = BlogCategory.objects.all()
        context['blogpages'] = blogpages
        return context