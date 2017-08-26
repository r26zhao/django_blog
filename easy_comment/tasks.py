import time
from django.apps import apps
from django.conf import settings
from django_blog import celery_app
from django.core.mail import send_mail
from django.template.loader import render_to_string


@celery_app.task
def email_handler(args):
    app_model = settings.AUTH_USER_MODEL.split('.')
    user_model = apps.get_model(*app_model)
    recipient = user_model.objects.filter(id__in=args)
    d = {}
    for user in recipient:
        try:
            if not (hasattr(user, 'onlinestatus') and user.onlinestatus.is_online()):
                context = {'receiver': user.username,
                           'unsend_count': user.notifications.filter(unread=True, emailed=False).count(),
                           'notice_list': user.notifications.filter(unread=True, emailed=False),
                           'unread_link': 'http://www.aaron-zhao.com/notifications/unread/'}
                msg_plain = render_to_string("notifications/email/email.txt", context=context)
                result = send_mail("来自[AA的博客] 您有未读的评论通知",
                                   msg_plain,
                                   'support@aaron-zhao.com',
                                   recipient_list=[user.email])
                user.notifications.unsent().update(emailed=True)
                if result == 1:
                    d[user.username] = 1
        except Exception as e:
            print("Error in easy_comment.handlers.py.email_handler: %s" % e)
    return d
