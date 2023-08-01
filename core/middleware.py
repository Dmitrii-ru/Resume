from django.db.models import Q
from core.settings import ALLOWED_HOSTS
from resume.models import UniqueIP

# list_exclude = ['188.233.76.49', '188.233.76.100', ALLOWED_HOSTS[1]]

list_exclude = []


class UniqueIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        num = 3
        if 'todo' in request.path:
            num = 2

        path = '/'.join(request.path.split('/')[:num])
        get_ip = self.get_client_ip(request)
        if get_ip not in list_exclude:
            ip = UniqueIP.objects.filter(ip_address=self.get_client_ip(request))
            if ip.exists():
                obj = ip.first()
                obj.count_visit += 1
                if obj.info_client == UniqueIP._meta.get_field('info_client').default:
                    obj.info_client = request.__dict__

                if path in obj.path_client:
                    obj.path_client[path] += 1
                else:
                    obj.path_client.update({path: 1})

            else:
                obj = UniqueIP.objects.create(ip_address=get_ip,
                                              count_visit=1,
                                              path_client={path: 1},
                                              info_client={request.__dict__})

            obj.save()

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
