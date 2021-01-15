from django.http import HttpResponse, JsonResponse

from config.error_config import NOT_FOUND


def not_found(request):
    raise Exception(NOT_FOUND)
