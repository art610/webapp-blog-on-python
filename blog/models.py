# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from datetime import date

from django import forms
from django.db import models

from django.http import Http404, HttpResponse

from django.utils.dateformat import DateFormat
from django.utils.formats import date_format

import wagtail
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel,MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager

from taggit.models import TaggedItemBase, Tag as TaggitTag

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route

from wagtailmd.utils import MarkdownField, MarkdownPanel

from blog.blocks import TwoColumnBlock

class BlogPage(RoutablePageMixin, Page):
    sidebar_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    description = models.CharField(max_length=255, blank=True,)

    add_page_1 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_1 = models.CharField(max_length=255, blank=True, null=True,)
    add_page_2 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_2 = models.CharField(max_length=255, blank=True, null=True,)
    add_page_3 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_3 = models.CharField(max_length=255, blank=True, null=True,)
    add_page_4 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_4 = models.CharField(max_length=255, blank=True, null=True,)
    add_page_5 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_5 = models.CharField(max_length=255, blank=True, null=True,)
    add_page_6 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_6 = models.CharField(max_length=255, blank=True, null=True,)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        ImageChooserPanel('sidebar_image'),
        FieldPanel('add_page_1'),
        FieldPanel('link_to_page_1'),
        FieldPanel('add_page_2'),
        FieldPanel('link_to_page_2'),
        FieldPanel('add_page_3'),
        FieldPanel('link_to_page_3'),
        FieldPanel('add_page_4'),
        FieldPanel('link_to_page_4'),
        FieldPanel('add_page_5'),
        FieldPanel('link_to_page_5'),
        FieldPanel('add_page_6'),
        FieldPanel('link_to_page_6'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['posts'] = self.posts
        context['blog_page'] = self
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")
        return context

    def get_posts(self):
        return PostPage.objects.descendant_of(self).live().order_by('-date')

    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def post_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.posts = self.get_posts().filter(date__year=year)
        self.search_type = 'date'
        self.search_term = year
        if month:
            self.posts = self.posts.filter(date__month=month)
            df = DateFormat(date(int(year), int(month), 1))
            self.search_term = df.format('F Y')
        if day:
            self.posts = self.posts.filter(date__day=day)
            self.search_term = date_format(date(int(year), int(month), int(day)))
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
        post_page = self.get_posts().filter(slug=slug).first()
        if not post_page:
            raise Http404
        return Page.serve(post_page, request, *args, **kwargs)

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = 'tag'
        self.search_term = tag
        self.posts = self.get_posts().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'category'
        self.search_term = category
        self.posts = self.get_posts().filter(categories__slug=category)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^search/$')
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.posts = self.posts.filter(body__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return Page.serve(self, request, *args, **kwargs)

class PostPage(Page):
    body = MarkdownField()
    date = models.DateTimeField(verbose_name="Post date", default=datetime.datetime.today)
    excerpt = MarkdownField(
        verbose_name='excerpt', blank=True,
    )

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    tags = ClusterTaggableManager(through='blog.BlogPageTag', blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        MarkdownPanel("body"),
        MarkdownPanel("excerpt"),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
    ]

    @property
    def blog_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(PostPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        context['post'] = self
        return context

class LandingPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('two_columns', TwoColumnBlock()),
        ('embedded_video', EmbedBlock(icon="media")),
    ],null=True,blank=True)

    add_page_1 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_1 = models.CharField(max_length=255, blank=True, null=True,)
    add_page_2 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_2 = models.CharField(max_length=255, blank=True, null=True,)
    add_page_3 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_3 = models.CharField(max_length=255, blank=True, null=True,)
    add_page_4 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_4 = models.CharField(max_length=255, blank=True, null=True,)
    add_page_5 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_5 = models.CharField(max_length=255, blank=True, null=True,)
    add_page_6 = models.CharField(max_length=255, blank=True, null=True,)
    link_to_page_6 = models.CharField(max_length=255, blank=True, null=True,)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('add_page_1'),
        FieldPanel('link_to_page_1'),
        FieldPanel('add_page_2'),
        FieldPanel('link_to_page_2'),
        FieldPanel('add_page_3'),
        FieldPanel('link_to_page_3'),
        FieldPanel('add_page_4'),
        FieldPanel('link_to_page_4'),
        FieldPanel('add_page_5'),
        FieldPanel('link_to_page_5'),
        FieldPanel('add_page_6'),
        FieldPanel('link_to_page_6'),
    ]

    @property
    def blog_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(LandingPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        context['landing'] = self
        return context

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('PostPage', related_name='post_tags')

@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True
