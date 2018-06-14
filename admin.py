from django.contrib import admin

from .models import PostcodeMapping


class PostcodeMappingAdmin(admin.ModelAdmin):
    search_fields = ('postcode',)


admin.site.register(PostcodeMapping, PostcodeMappingAdmin)
