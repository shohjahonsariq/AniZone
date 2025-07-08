from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(user_logged_in)
def populate_profile(sender, request, user, **kwargs):
    print("✅ Google login ishladi")
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        data = social_account.extra_data
        picture_url = data.get('picture')
        first_name = data.get('given_name')
        last_name = data.get('family_name')

        # Ism va familiyani yangilash
        user.first_name = first_name or user.first_name
        user.last_name = last_name or user.last_name
        user.save()

        # Profil rasmi
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if picture_url:
            profile.profile_image = picture_url
            profile.save()
            print("💾 Profil rasmi saqlandi")

    except SocialAccount.DoesNotExist:
        print("⚠️ Google account topilmadi")
