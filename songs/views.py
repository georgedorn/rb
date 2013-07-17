from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from rb.songs import models
from django.utils import simplejson

def songlist(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    songs = _get_songs(user)
    return render_to_response('songs/songlist.html', {'songlist':songs, 'user':request.user})

def _get_songs(user=None):
    songs = models.Song.objects.all().order_by("name").order_by("band_diff").values()
    if user:
        owned_songs = models.Song.objects.all().filter(owned_by=user).values_list('id', flat=True)
        for song in songs:
            song['owned'] = song['id'] in owned_songs
    return songs

def mark_ownership(request, id, own):
    own = bool(own)
    if request.user.is_authenticated():
        user = request.user
    else:
        return False
    song = models.Song.objects.get(id=int(id))
    if own:
        song.owned_by.add(user)
    else:
        song.owned_by.remove(user)
    if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
        return HttpResponseRedirect(reverse('songlist'))
    else:
        songdata = {'id':song.id, 'owned':int(not own)}
        url = reverse('mark_ownership', kwargs={'id':song.id, 'own':int((not own))})
        data = {'song':songdata, 'url':url}
        return HttpResponse(simplejson.dumps(data),
                                    mimetype='application/json')

    