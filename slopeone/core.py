from django.db.models import Count
from django.contrib.auth.models import User

from slopeone.models import Rating, Calculation

def update():
    """
    Calculate the difference and frequency.

    The prediction algorithm is Slope One:
    http://www.daniel-lemire.com/fr/documents/publications/lemiremaclachlan_sdm05.pdf
    """
    # delete all calculations before making new ones
    for calc in Calculation.objects.all():
        calc.delete()

    user_ratings = Rating.objects.all().values('user').annotate(
        user_count=Count('user'))
    for user_rating in user_ratings:
        ratings = Rating.objects.all().filter(user=user_rating['user'])
        for rating in ratings:
            for rating2 in ratings:
                try:
                    calc = Calculation.objects.get(
                        item1_object_id=rating.item.id,
                        item2_object_id=rating2.item.id)
                except Calculation.DoesNotExist:
                    calc = Calculation()
                    calc.item1 = rating.item
                    calc.item2 = rating2.item
                calc.freq += 1
                calc.diff += rating.rating - rating2.rating
                calc.save()

    # divide the difference by frequency
    item1_calcs = Calculation.objects.all().values('item1_object_id').annotate(
        item1_count=Count('item1_object_id'))
    for item1_calc in item1_calcs:
        ratings = Calculation.objects.filter(
            item1_object_id=item1_calc['item1_object_id'])
        for item2 in ratings:
            item2.diff /= item2.freq
            item2.save()

def recommend(user):
    """
    Returns a list of pairs with the object id and the predicted rating
    of each object.
    """
    preds, freqs = {}, {}

    # get all ratings and calculations for current user
    user_ratings = user.rating_set.all()
    #user_ratings = Rating.objects.all().values('user').annotate(user_count=Count('user'))
    for user_rating in user_ratings:
        item1_groups = Calculation.objects.all().values('item1_object_id').\
                annotate(item1_count=Count('item1_object_id'))
        for item1_group in item1_groups:
            diffratings = Calculation.objects.filter(
                item1_object_id=item1_group['item1_object_id'])
            try:
                freq = Calculation.objects.get(
                    item1_object_id=item1_group['item1_object_id'],
                    item2_object_id=user_rating.object_id).freq
            except Calculation.DoesNotExist:
                continue
            preds.setdefault(item1_group['item1_object_id'], 0.0)
            freqs.setdefault(item1_group['item1_object_id'], 0)
            diffr = Calculation.objects.get(
                item1_object_id=item1_group['item1_object_id'],
                item2_object_id=user_rating.object_id).diff
            preds[item1_group['item1_object_id']] += \
                    freq * (diffr + user_rating.rating)
            freqs[item1_group['item1_object_id']] += freq
    adict = dict([(item, value / freqs[item])
                 for item, value in preds.iteritems()])
    return sorted(adict.iteritems(), key=lambda (k,v): (v,k), reverse=True)
