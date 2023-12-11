from django.contrib import admin

from synthesis.models import Project, Tag, ProjectTag

admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(ProjectTag)
