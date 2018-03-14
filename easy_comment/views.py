from .forms import CommentForm
from .models import Comment
from blog.models import Post
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from . import handlers

# Create your views here.
class PostCommentView(SingleObjectMixin, ListView):
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Post.objects.all())
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        page_obj = context['page_obj']
        html = ''
        for comment in context['object_list']:
            html += comment.to_html()
        return JsonResponse({'html': html})

    @method_decorator(login_required)
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
        if form.errors.as_data()['content']:
            msg = form.errors.as_data()['content'][0].message
        else:
            msg = '评论出错啦！'
        return JsonResponse({"msg": msg})

    def get_queryset(self):
        return self.object.comment_set.all().order_by('-submit_date')


@method_decorator(csrf_exempt, name='dispatch')
class CommentLikeView(SingleObjectMixin, View):
    model = Comment

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        action = request.POST.get('action')
        print(action)
        print(comment.user == request.user)
        if comment.user == request.user:
            return JsonResponse({'status': 'ko', 'msg': '不能对自己点赞或者踩'})
        if action == 'like':
            if request.user not in comment.users_like.all():
                comment.users_like.add(request.user)
                if request.user in comment.users_dislike.all():
                    comment.users_dislike.remove(request.user)
            else:
                return JsonResponse({'status': 'ko', 'msg': '已经赞过啦♪(^∇^*)~！'})
        else:
            if request.user not in comment.users_dislike.all():
                comment.users_dislike.add(request.user)
                if request.user in comment.users_like.all():
                    comment.users_like.remove(request.user)
            else:
                return JsonResponse({'status': 'ko', 'msg': '已经踩过啦￣□￣｜｜！'})
        result = comment.likes_count(update=True)
        comment.to_html(update=True)
        return JsonResponse({'status': 'ok', 'like': result['likes'], 'dislike': result['dislikes']})


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
