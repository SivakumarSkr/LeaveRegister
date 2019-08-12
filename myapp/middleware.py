from django.utils.deprecation import MiddlewareMixin


class StackOverFlowException(MiddlewareMixin):
    def process_exception(self, request, exception):
        print(dir(exception))
        print(dir(self))
        print(dir(request))
        return None

    def process_template_response(self,request, response):
        print('process template response')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('process_view')

    def process_response(self, response, request):
        print('process response')
        return response

    def process_request(self, request):
        print('process request')



