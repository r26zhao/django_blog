from .forms import CommentForm
from .models import Comment, Like
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.cache import cache
from django.views.generic.edit import CreateView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import handlers

# Create your views here.
class PostCommentView(LoginRequiredMixin, View):

    def post(self, request):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.user_name = request.user.username
            new_comment.save()
            result = new_comment.post.comment_update(new_comment)
            return JsonResponse({'msg': 'success!',
                                 'html': result[0],
                                 'user_num': result[1],
                                 'comment_num': result[2]})
        return JsonResponse({'msg': '评论出错!'})


@require_POST
def like(request):
    comment_id = request.POST.get('id')
    action = request.POST.get('action')
    if comment_id and action:
        try:
            comment = Comment.objects.get(id=comment_id)
            obj, created = Like.objects.get_or_create(user=request.user, comment=comment)
            if action == 'like':
                if not created:
                    obj.status = True
                    obj.save()
            if action == 'cancel-like' or action == 'cancel-dislike':
                obj.delete()
            if action == 'dislike':
                obj.status = False
                obj.save()
            return JsonResponse({'msg': 'OK'})
        except Comment.DoesNotExist:
            return JsonResponse({"msg": "KO"})
    return JsonResponse({"msg": "KO"})
