from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Coder)
admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Submission)
