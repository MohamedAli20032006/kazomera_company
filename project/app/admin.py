from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Publication)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Interaction)
admin.site.register(Project)
admin.site.register(Contribution)
admin.site.register(Investment)

