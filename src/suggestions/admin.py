from django.contrib import admin

# Register your models here.
from django.contrib import admin
from suggestions.models import Suggestion

# Register your models here.
class SuggestionAdmin(admin.ModelAdmin):
    model = Suggestion
    list_display = ["content_object", "user", "value"]
    search_fields = ["user__username"]
    raw_id_fields = ["user"]
    readonly_fields = ["content_object"]
    
    
admin.site.register(Suggestion, SuggestionAdmin)