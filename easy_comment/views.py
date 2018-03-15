from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404

from .forms import CommentForm
from .models import Comment, Favour
from blog.models import Post
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


class Post_FavourView(View):

    def get(self, request, post_id):
        if request.user.is_authenticated:
            post = get_object_or_404(Post, id=post_id)

        return JsonResponse({'status': 0})
