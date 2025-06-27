from django.shortcuts import render
from datacenter.models import Visit, format_duration


def storage_information_view(request):
    non_closed_visits = []

    for visit in Visit.objects.filter(leaved_at__isnull=True):
        duration = visit.get_duration()
        formatted_duration = format_duration(duration)
        visit_details = {
            'who_entered': visit.passcard.owner_name,
            'entered_at': visit.entered_at,
            'duration': formatted_duration,
        }
        non_closed_visits.append(visit_details)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
