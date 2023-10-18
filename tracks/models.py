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

#from .blocks import BodyBlock


# Create your models here.

class TrackIndex(Page):

    def serve(self, request, *args, **kwargs):
        use_template = request.GET.get("use_template")
        print(use_template)

        context = {
            "page" : self,
            "use_template" : use_template
        }

        if use_template == "SPA":
            return render(request, "tracks/components/track-list.html", context)

        return render(request, "tracks/track_index.html", context)

    pass


class AudioTrack(Page):


    # template = "tracks/ajax_track.html"

    track_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    album = models.CharField(max_length=100, null=True, blank=True)
    tags = ClusterTaggableManager(through="tracks.AudioTrackTag", blank=True)

    audio_file = models.ForeignKey(
        "wagtailmedia.Media",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    track_text = RichTextField(blank=True)




    content_panels = Page.content_panels + [
        FieldPanel("track_image"),
        FieldPanel("album"),
        InlinePanel("artists", label="Artists"),
        InlinePanel("audio_categories", label="Genre"),
        MediaChooserPanel("audio_file"),
        FieldPanel("tags"),
        FieldPanel("track_text"),
    ]

    def serve(self, request, *args, **kwargs):
        use_template = request.GET.get("use_template")
        print(use_template)

        context = {
            "page" : self,
            "use_template" : use_template
        }

        if use_template == "SPA":
            return render(request, "tracks/components/track-info.html", context)

        return render(request, "tracks/track.html", context)



@register_snippet
class AudioCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug")
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Audio Category"
        verbose_name_plural = "Audio Categories"


@register_snippet
class AudioArtist(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug")
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Artist"
        verbose_name_plural = "Artists"


@register_snippet
class AudioTag(TaggitTag):
    class Meta:
        proxy = True


#intermediary models

class TrackAudioArtist(models.Model):
    track = ParentalKey(
        "tracks.AudioTrack", on_delete=models.CASCADE, related_name="artists"
    )

    artist = models.ForeignKey(
        "tracks.AudioArtist", on_delete=models.CASCADE, related_name="tracks"
    )

    panels = [
        FieldPanel("artist")
    ]

    class Meta:
        unique_together = ("track", "artist")


class TrackAudioCategory(models.Model):
    track = ParentalKey(
        "tracks.AudioTrack", on_delete=models.CASCADE, related_name="audio_categories"
    )

    track_category = models.ForeignKey(
        "tracks.AudioCategory", on_delete=models.CASCADE, related_name="tracks"
    )

    panels = [
        FieldPanel("track_category")
    ]

    class Meta:
        unique_together = ("track", "track_category")


class AudioTrackTag(TaggedItemBase):
    content_object = ParentalKey("AudioTrack", related_name="audio_tags")