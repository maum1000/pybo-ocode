from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer

########################################################################################################
"""
로그아웃 상태에서는 request.user가 AnonymousUser 객체이므로 에러가 발생할 수 있음 

-> 로그인 상태에서만 질문을 등록할 수 있도록 수정
"""
@login_required(login_url='common:login')
def answer_create(request, question_id):
    ''' pybo 답변등록 '''
    #
    question = get_object_or_404(Question, pk=question_id)
    #
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        #
        if form.is_valid():
            answer = form.save(commit=False)  # commit=False는 데이터베이스에 저장하지 않고 모델 객체만 반환
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # 
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id)) # answer_{}(앵커)로 이동
            #
        #
    else:
        form = AnswerForm()
        #
    #
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
    #
#

########################################################################################################

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """ pybo 답변 수정 """
    #
    answer = get_object_or_404(Answer, pk=answer_id)
    #
    if request.user != answer.author:
        messages.error(request, 

        '수정권한이 없습니다'

        )
        #
        return redirect('pybo:detail', question_id=answer.question.id)
        #
    #
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        #
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
            #
        #
    #
    else:
        form = AnswerForm(instance=answer)
        #
    #
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)
    #
#

########################################################################################################

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """ pybo 답변 삭제 """
    #
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, 

        '삭제권한이 없습니다'

        )
        #
    #
    else:
        answer.delete()
        #
    #
    return redirect('pybo:detail', question_id=answer.question.id)
    #
#

########################################################################################################

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    """ pybo 답변 추천 """
    #
    answer = get_object_or_404(Answer, pk=answer_id)
    #
    if request.user == answer.author:
        messages.error(request, 
        
        '본인이 작성한 글은 추천할수 없습니다'
        
        )
        #
    #
    else:
        answer.voter.add(request.user)
        #
    #
    return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    #
#

########################################################################################################