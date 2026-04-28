#from django.contrib import admin

# Register your models here.
from django.contrib import admin 
from .models import Student, Question, Response

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'payment_status']
    #list_display = ['student',]
   # list_filter = ['payment_status']         #filter aa jayega -> easy management

class ResponseAdmin(admin.ModelAdmin):
    list_display = ['student','question','selected_option','answer_text','marks']

admin.site.register(Student,StudentAdmin)

#from .models import Question    #ye Question model ko admin panel mei dikhane ke liye hai
admin.site.register(Question)   #ye Question model ko admin panel mei dikhane ke liye hai

#admin.site.register(Student)

#from .models import Response

#admin.site.register(Response)
admin.site.register(Response,ResponseAdmin)