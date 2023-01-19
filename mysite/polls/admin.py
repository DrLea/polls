from django.contrib import admin
from .models import Question, Choice

class InlineChoice(admin.TabularInline):
    model = Choice
    extra = 2
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Main', {'fields': ['question_text']}),
        ('Meta', {'fields': ['pub_date']}),
        ]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'has_options')
    inlines = [InlineChoice]
    search_fields = ['question_text', 'pub_date']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)