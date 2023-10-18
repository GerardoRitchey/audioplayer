from django import forms
from django.db import models
from django.shortcuts import render
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import StreamField, RichTextField
from wagtailmedia.edit_handlers import MediaChooserPanel

from .blocks import TrackOrderBlocks
from tracks.models import AudioTrack  # Import your Track model here

# Create your models here.

class PlaylistIndex(Page):


    def serve(self, request, *args, **kwargs):
        use_template = request.GET.get("use_template")
        print(use_template)

        context = {
            "page" : self,
            "use_template" : use_template
        }

        if use_template == "SPA":
            return render(request, "playlists/components/playlist-list.html", context)

        return render(request, "playlists/playlist_index.html", context)


class PlaylistPage(Page):

   # template = "playlists/playlist.html"

    body = StreamField([
        ('page_order', TrackOrderBlocks()),
    ],
    use_json_field=True, null=True, blank=True)

    body.verbose_name = "Playlist Tracks"

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    inline_panels = [
        InlinePanel('body'),
    ]

    # def sorted_pages(self):
    #     return sorted(self.body, key=lambda block: block.value['order'])


    def serve(self, request, *args, **kwargs):
        use_template = request.GET.get("use_template")
        print(use_template)

        context = {
            "page" : self,
            "use_template" : use_template
        }

        if use_template == "SPA":
            return render(request, "playlists/components/playlist-tracks.html", context)

        return render(request, "playlists/playlist.html", context)

    class Meta:
        verbose_name = "Playlist Page"