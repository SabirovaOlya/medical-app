from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import Profile, Doctor, Hospital, Pharmacy, Client, DoctorCategory


@receiver(post_save, sender=Profile)
def create_related_model(sender, instance, created, **kwargs):
    if created:
        if instance.role == Profile.Type.DOCTOR:
            default_category, _ = DoctorCategory.objects.get_or_create(name="General")
            Doctor.objects.create(user=instance, category=default_category)
        elif instance.role == Profile.Type.HOSPITAL:
            Hospital.objects.create(user=instance)
        elif instance.role == Profile.Type.PHARMACY:
            Pharmacy.objects.create(user=instance)
        elif instance.role == Profile.Type.CLIENT:
            Client.objects.create(user=instance)

# @receiver(pre_save, sender=User)
# def user_pre_save(sender, instance: User, **kwargs):
#     if instance.pk is None:  # and (not isinstance(instance.balance, int) or instance.balance == 0):
#         # instance.balance = 5000
#
#         send_mail(
#             'Tema',
#             'You signed up successfully',
#             settings.DEFAULT_FROM_EMAIL,
#             [instance.email],
#             fail_silently=False,
#         )
