from datetime import datetime

from core.settings import ALLOWED_HOSTS
from resume.models import UniqueIP
import redis
import json

# list_exclude = ['188.233.76.49', '188.233.76.100', ALLOWED_HOSTS[1]]
list_path = ['send_email', 'feedback', 'todo_session', 'projects', 'project', 'mptt_blog', 'quiz', 'api', 'index']
list_exclude = []


class UniqueIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        num = 3
        if 'todo' in request.path:
            num = 2
        tuple_req = tuple(request.__dict__.items())
        path_split = request.path.split('/')[:num]
        get_ip = self.get_client_ip(request)
        path_l = list(filter(None, path_split))
        q = set(list_path) & set(path_l)
        if get_ip and q:
            _path = '/'.join(request.path.split('/')[:num])
            if get_ip not in list_exclude:
                db2 = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True)
                if not db2.get(get_ip):
                    to_save = {'path_client': {_path: 1}, "info_client": str(tuple_req)}
                    db2.set(get_ip, json.dumps(to_save))
                else:
                    ip_cache = json.loads(db2.get(get_ip))
                    path_client = ip_cache.setdefault('path_client', {})
                    if _path in path_client:
                        path_client[_path] += 1
                    else:
                        path_client[_path] = 1
                    db2.set(get_ip, json.dumps(ip_cache))
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
