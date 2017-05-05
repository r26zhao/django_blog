from django.shortcuts import render
import logging
from django.conf import settings

logger = logging.getLogger('blog.views')
# Create your views here.

#获得全局变量
def global_setting(request):
    return {'SITE_NAME':settings.SITE_NAME, 'SITE_DESCP':settings.SITE_DESCP,}

def index(request):
    try:
        pass
    except Exception as e:
        logger.error(e)
    return render(request, 'blog/index.html', locals())