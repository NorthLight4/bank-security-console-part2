from datacenter.models import Passcard, Visit, format_duration
from django.shortcuts import render
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard__owner_name=passcard.owner_name)
    this_passcard_visits = []

    for visit in visits:
        duration = visit.get_duration()
        this_passcard_visit = {
            'entered_at': visit.entered_at,
            'duration': format_duration(duration),
            'is_strange': visit.is_long
        }
        this_passcard_visits.append(this_passcard_visit)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
