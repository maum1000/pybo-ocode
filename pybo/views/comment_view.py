from django.contrib import messages  # 메시지 처리에 사용
from django.contrib.auth.decorators import login_required  # 로그인 필수 조건을 추가하는 데코레이터
from django.shortcuts import render, get_object_or_404, redirect  # 뷰 처리, 객체 조회, 리다이렉트 기능
from django.utils import timezone  # 시간 처리를 위한 유틸리티

from ..forms import CommentForm  # 댓글 작성 폼
from ..models import Question, Answer, Comment  # 모델 정의 (질문, 답변, 댓글)

# 질문에 대한 댓글 작성 뷰 (로그인 필요)
@login_required(login_url='common:login')  # 로그인이 되어있지 않으면 로그인 페이지로 이동
def comment_create_question(request, question_id):

    # 질문 객체 조회 (존재하지 않으면 404 에러 발생)
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":  # POST 요청 시 (댓글 작성 요청)
        form = CommentForm(request.POST)
        if form.is_valid():  # 폼 데이터가 유효할 때
            comment = form.save(commit=False)  # DB에 바로 저장하지 않고 일단 폼에서 객체 생성
            comment.author = request.user  # 댓글 작성자를 현재 로그인한 사용자로 설정
            comment.create_date = timezone.now()  # 댓글 작성 시간을 현재 시간으로 설정
            comment.question = question  # 해당 댓글이 달릴 질문을 지정
            comment.save()  # 댓글을 DB에 저장
        return redirect('pybo:detail', question_id=question.id)  # 댓글 작성 후 질문 상세 페이지로 리다이렉트
    else:  # GET 요청 시 (댓글 작성 폼 페이지 렌더링)
        form = CommentForm()

    # 댓글을 작성 순서로 조회 (대댓글 포함)
    comments = question.comments.filter(parent__isnull=True).order_by('create_date').prefetch_related('replies')
    comments_reply = Comment.objects.filter(parent__in=comments).order_by('create_date')

    # 템플릿에 전달할 데이터 설정
    context = {'form': form, 'comments': comments, 'comments_reply': comments_reply}
    return render(request, 'pybo/comment_form.html', context)  # 댓글 작성 페이지 렌더링

# 질문 댓글 수정 뷰 (로그인 필요)
@login_required(login_url='common:login')  # 로그인이 되어있지 않으면 로그인 페이지로 이동
def comment_modify_question(request, comment_id):
    # 댓글 객체 조회 (존재하지 않으면 404 에러 발생)
    comment = get_object_or_404(Comment, pk=comment_id)

    # 현재 로그인한 사용자가 댓글 작성자가 아닐 경우 권한 에러 메시지
    if request.user != comment.author:
        messages.error(request, 
    
    '댓글 수정 권한이 없습니다.'
    
    )
        return redirect('pybo:detail', question_id=comment.question.id)  # 권한이 없을 경우 질문 상세 페이지로 리다이렉트

    if request.method == "POST":  # POST 요청 시 (댓글 수정 요청)
        form = CommentForm(request.POST, instance=comment)  # 기존 댓글 내용을 폼에 넣어 수정
        if form.is_valid():  # 폼 데이터가 유효할 때
            comment = form.save(commit=False)  # DB에 바로 저장하지 않고 일단 폼에서 객체 생성
            comment.author = request.user  # 댓글 작성자를 현재 로그인한 사용자로 재설정 (원 작성자 유지)
            comment.modify_date = timezone.now()  # 댓글 수정 시간을 현재 시간으로 설정
            comment.save()  # 댓글 수정 내용을 DB에 저장
            return redirect('pybo:detail', question_id=comment.question.id)  # 수정 후 질문 상세 페이지로 리다이렉트
    else:  # GET 요청 시 (댓글 수정 폼 페이지 렌더링)
        form = CommentForm(instance=comment)  # 기존 댓글 내용을 폼에 채워 보여줌

    # 템플릿에 전달할 데이터 설정
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)  # 댓글 수정 페이지 렌더링

# 질문 댓글 삭제 뷰 (로그인 필요)
@login_required(login_url='common:login')  # 로그인이 되어있지 않으면 로그인 페이지로 이동
def comment_delete_question(request, comment_id):
    # 댓글 객체 조회 (존재하지 않으면 404 에러 발생)
    comment = get_object_or_404(Comment, pk=comment_id)

    # 현재 로그인한 사용자가 댓글 작성자가 아닐 경우 권한 에러 메시지
    if request.user != comment.author:
        messages.error(request,
    
    '댓글 삭제 권한이 없습니다.'
    
    )
        return redirect('pybo:detail', question_id=comment.question.id)  # 권한이 없을 경우 질문 상세 페이지로 리다이렉트
    else:
        comment.delete()  # 댓글 삭제

    # 댓글 삭제 후 질문 상세 페이지로 리다이렉트
    return redirect('pybo:detail', question_id=comment.question.id)
