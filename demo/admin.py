from django.contrib import admin
from django.db import models

from markdown_editor.widgets import AdminMarkdownWidget
from demo.models import MyModel


class TestAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownWidget()},
    }


admin.site.register(MyModel, TestAdmin)
