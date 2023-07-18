import logging

from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin

from system.error import ServerException, PermissionDeniedException


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if type(exception) == ServerException:
            print("发生异常：{}".format(exception), request)
            logging.error("发生异常：{}".format(exception), request)
            return render(request, 'error.html', {
                'message': exception.message,
            })
        elif type(exception) == PermissionDeniedException:
            return render(request, 'error.html', {
                'message': exception.message,
            })
        else:
            print("发生异常：{}".format(exception), request)
