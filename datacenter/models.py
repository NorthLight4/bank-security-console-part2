from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        now = localtime().replace(microsecond=0)
        start_time = localtime(self.entered_at)
        end_time = localtime(self.leaved_at) if self.leaved_at else now
        duration = end_time - start_time
        return duration

    def is_long(self, minutes=60):
        duration = self.get_duration()
        total_sec = duration.total_seconds()
        seconds_in_minute = 60
        if total_sec // seconds_in_minute > minutes:
            return True
        return False


def format_duration(duration):
    total_sec = int(duration.total_seconds())
    seconds_in_hour = 3600
    seconds_in_minute = 60

    total_hours = total_sec // seconds_in_hour
    total_minutes = (total_sec % seconds_in_hour) // seconds_in_minute
    formatted_duration = f'{total_hours}ч : {total_minutes}мин'
    return formatted_duration
