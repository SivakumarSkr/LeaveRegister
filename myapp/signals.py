from django.db.models.signals import post_save
from django.dispatch import receiver

from myapp.models import UserProfile, AnnualLeaveDetail, current_year


@receiver(post_save, sender=UserProfile)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        AnnualLeaveDetail.objects.create(
            user_profile=instance,
            year=current_year(),
        )
