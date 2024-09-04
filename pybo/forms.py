from django import forms
from pybo.models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content'] # subject와 content 필드만 사용
        labels = {
            'subject': '제목',
            'content': '내용',
        } # subject와 content 필드의 레이블을 '제목'과 '내용'으로 지정
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # } # subject 필드는 TextInput 위젯을 사용하고 content 필드는 Textarea 위젯을 사용
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }
        # widgets = {
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        # } # content 필드는 Textarea 위젯을 사용