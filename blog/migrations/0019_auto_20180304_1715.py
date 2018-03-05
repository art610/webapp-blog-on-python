# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-04 14:15
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20180304_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='add_page_1',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='add_page_2',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='add_page_3',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='add_page_4',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='add_page_5',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='add_page_6',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='link_to_page_1',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='link_to_page_2',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='link_to_page_3',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='link_to_page_4',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='link_to_page_5',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='link_to_page_6',
        ),
        migrations.AddField(
            model_name='blogpage',
            name='nav_links',
            field=wagtail.wagtailcore.fields.StreamField((('nav_link_title', wagtail.wagtailcore.blocks.CharBlock()), ('nav_link_url', wagtail.wagtailcore.blocks.CharBlock())), blank=True, null=True),
        ),
    ]