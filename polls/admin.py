from django.contrib import admin

from .models import Choice, Question


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """The following assignment determines the display order of the fields
    at the admin page. However, we'll organize the admin page by fieldsets.
    fields = ['pub_date', 'question_text']
    """
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)
