from django.db.models.signals import post_save
from notifications.signals import notify
from .models import Comment, Like
from notifications.signals import notify
from django.conf import settings
from django.apps import apps

def get_recipient():
    admins = [i[0] for i in settings.ADMINS]
    app_model = settings.AUTH_USER_MODEL.split('.')
    User_model = apps.get_model(*app_model)
    recipient = User_model.objects.filter(username__in=admins)
    return recipient

ADMINS = get_recipient()

def comment_handle(sender, instance, created, **kwargs):
    if created:
        recipient = ADMINS.exclude(id=instance.user.id)
        if not instance.parent is None:
            recipient = recipient.exclude(id=instance.parent.user.id)
            if recipient.count() > 0:
                notify.send(instance.user, recipient=recipient,
                            verb='回复了 %s' % instance.parent.user_name,
                            action_object=instance,
                            target=instance.post,
                            description=instance.content)
            if not instance.user_name == instance.parent.user_name:
                notify.send(instance.user, recipient=instance.parent.user, verb='@了你',
                            action_object=instance,
                            target=instance.post,
                            description=instance.content)
        else:
            if recipient.count() > 0:
                notify.send(instance.user, recipient=recipient, verb='发表了评论',
                            action_object=instance,
                            target=instance.post,
                            description=instance.content)

post_save.connect(comment_handle, sender=Comment)

