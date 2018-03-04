from .forms import CommentForm
from .models import Comment, Like
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.cache import cache
from . import handlers


# Create your views here.

@require_POST
def submit_comment(request):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # print('success')
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.user_name = request.user.username
        new_comment.save()
        key = 'comment_{}_html'.format(new_comment.id)
        comment_html = render_to_string('easy_comment/comment_entry.html', context={'comment': new_comment})
        cache.set(key, comment_html, timeout=300)
        post = new_comment.post
        key1 = 'post_{}_comments'.format(post.id)
        comment_list_html = cache.get(key1, None)
        if comment_list_html:
            comment_list_html = comment_html + comment_list_html
            cache.set(key1, comment_list_html, timeout=300)
        return JsonResponse({'msg': 'success!', 'html': comment_html})
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
