from wagtail import blocks


class TrackOrderBlocks(blocks.StructBlock):
    page = blocks.PageChooserBlock(page_type="tracks.AudioTrack", label="Track")
    #order = blocks.IntegerBlock() #not needed StreamField will manage the order using the built in UI

    class Meta:
        icon = "link"
        label = "Track Page"