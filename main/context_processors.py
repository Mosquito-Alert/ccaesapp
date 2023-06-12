import ccaesapp.settings as settings

def name_processor(request):
    return {'app_name': settings.APP_NAME}
