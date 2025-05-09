from django.contrib import admin
from .models import Celebrity, Media, MembershipTier, Fan

admin.site.register(Celebrity)
admin.site.register(Media)
admin.site.register(MembershipTier)
admin.site.register(Fan)
