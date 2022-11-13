from .models import *
from random import randint, choice
from datetime import datetime

def generate():
    for i in Task.objects.all():
        i.duration = None
        i.estimated = True
        i.save()

    for i in Task.objects.all().order_by("?")[:500]:
        i.duration = randint(1, 20)
        i.estimated = False
        #if i.quantity == 0:
        #    i.quantity = 1
        i.save()

def generate_dates():
    dates = []
    for m in [11, 12]:
        for d in range(1, 30):
            dates.append(datetime(year=2022, day=d, month=m))

    for i in Task.objects.all():
        i.start = choice(dates)
        i.save()