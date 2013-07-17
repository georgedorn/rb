from django.contrib import admin
from django.contrib.auth.models import User


from django.db import models
from django.db.models import signals

song_sources = [('RB1','Rock band 1'),
                ('RB2','Rock band 2'),
                ('DLC', 'Download'),
                ('RBU', 'Unplugged')]

class Song(models.Model):
    name = models.CharField(max_length=255)
    band = models.CharField(max_length=255)
    year = models.IntegerField(null=True)
    band_diff = models.IntegerField()
    guitar_diff = models.IntegerField(null=True)
    bass_diff = models.IntegerField(null=True)
    vocals_diff = models.IntegerField(null=True)
    drums_diff = models.IntegerField(null=True)
    source = models.CharField(max_length=5,
                              choices=song_sources
                              )
    release = models.DateField(null=True)
    owned_by = models.ManyToManyField(User)
    
    def __unicode__(self):
        str = "Song: %s\nBand: %s\nYear: %s\n"
        str += "Band: %s\tGuitar: %s\tBass: %s\tVox: %s\tDrums: %s\n"
        str += "Source: %s\nReleased: %s"
        return str % (self.name, self.band, self.year,
                      self.band_diff, self.guitar_diff, self.bass_diff,
                      self.vocals_diff, self.drums_diff, self.source,
                      self.release)
        
class SongAdmin(admin.ModelAdmin):
    pass
admin.site.register(Song, SongAdmin)

