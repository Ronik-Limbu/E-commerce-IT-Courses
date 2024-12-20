from django.contrib import admin
from .models import Course
from .models import Certificate
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=['id','name','image','price','desc','About_course']




class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'issued_to')
    search_fields = ('certificate_number', 'issued_to')

admin.site.register(Certificate, CertificateAdmin)