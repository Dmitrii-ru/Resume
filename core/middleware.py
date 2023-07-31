from django.db.models import Q
from core.settings import ALLOWED_HOSTS
from resume.models import UniqueIP

list_exclude = ['188.233.76.49', '188.233.76.100', ALLOWED_HOSTS[1]]



class UniqueIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        get_ip = self.get_client_ip(request)
        print(get_ip)

        if get_ip not in list_exclude:
            ip = UniqueIP.objects.filter(ip_address=self.get_client_ip(request))
            if ip.exists():
                obj = ip.first()
                obj.count_visit += 1
            else:
                obj = UniqueIP.objects.create(ip_address=get_ip, count_visit=1)
            obj.save()
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
