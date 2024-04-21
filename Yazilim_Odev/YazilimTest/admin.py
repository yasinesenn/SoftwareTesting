from django.contrib import admin

from YazilimTest.models import GitHubDepo, JavaClass

# Register your models here.
admin.site.register(JavaClass)
admin.site.register(GitHubDepo)