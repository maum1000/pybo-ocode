from django.contrib import admin
from pybo.models import Question

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']  # 검색 기능 추가
    
admin.site.register(Question, QuestionAdmin)  # Question 모델을 QuestionAdmin 클래스와 함께 등록
    
