from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

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
class PostFavourView(View):

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post_type = ContentType.objects.get_for_model(post)
        object, created = Favour.objects.get_or_create(content_type=post_type, object_id=post_id, user=request.user)
        action = request.POST.get('action')
        update = 1
        if not created:
            if action == 'like':
                object.liked = True
            else:
                object.liked = False
                update = -1
            object.save()
        count = post.favour_count(update=update)
        return JsonResponse({'count': count})

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        count = post.favours.filter(liked=True).count()
        status = -1
        """
        也可以这样写，需要在post模型里的GenericRelation里添加related_query_name='posts'
        count = Favour.objects.filter(posts__id=post_id, liked=True).count()
        """
        if request.user.is_authenticated:
            user_favour = Favour.objects.filter(posts__id=post_id, user=request.user, liked=True)
            status = 1 if user_favour.exists() else 0
        return JsonResponse({'status': status, 'count': count})


