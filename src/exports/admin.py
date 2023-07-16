from django.contrib import admin

from exports.models import Export

# Register your models here.
class ExportAdmin(admin.ModelAdmin):
    list_display=['type', 'timestamp', 'latest']
    list_filter =['latest','type', 'timestamp']

admin.site.register(Export, ExportAdmin)