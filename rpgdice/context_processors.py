from django.templatetags.static import static

from rpgdice import settings

# django-vue: production@3
# Add the proper vue frontend url to the context
def vue_frontend_url_processor(request: object) -> dict[str, str]:
    url = settings.VUE_FRONTEND_DEV_SERVER_ENTRYPOINT if settings.VUE_FRONTEND_USE_DEV_SERVER \
        else str(static(settings.VUE_FRONTEND_STATIC_ENTRYPOINT))
    return {'vue_frontend_url': url}

