from fabapp.models import User,Exhibition
from django.db.models import Q
from review.models import Review
from review.serializers import ReviewSeializer
from fabapp.serializers import UserDetailSerializer
from django.db.models import F, Sum, FloatField, Avg
from django.utils import timezone

def UserRating():
    print("User Rating schduler Running....")
    rv = User.objects.filter(cron_review=False,is_active=True).first()
    if rv:
        rv.cron_review = True
        rv.save()
        serila = UserDetailSerializer(rv,many=False)
        ID = serila.data['id']
        us = Review.objects.filter(rated_user_id=ID).aggregate(total=Avg(F('rating')))
        rate = User.objects.get(id=ID)
        rate.avg_rating = us['total']
        rate.save()
        print('rating updated')    
    else:
        pass


def CronReset():
    print("Reset schduler start....")
    rv = User.objects.filter(cron_review=True,is_active=True).update(cron_review=False)
    if rv:
        print('Cron Reset')    
    else:
        pass        

def DisableExi():
    print("Exhibition disable schduler running....")
    dis =  Exhibition.objects.filter(end_date__lt=timezone.now()).update(Running_status=False)
    if dis:
        print("Exhibition Disable")
    else:
        pass


