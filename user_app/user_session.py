import locale
from operator import itemgetter
from core import settings
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import uuid


class UserSessionEmail:

    def __init__(self, request, session=None):

        if session:
            self.session = session
        else:
            self.session = request.session
        user_session_email = self.session.get(settings.USER_SESSION_EMAIL_ID)

        if not user_session_email:
            user_session_email = self.session[settings.USER_SESSION_EMAIL_ID] = {}
            self.user_session_email = user_session_email
            self.add()
        else:
            self.user_session_email = user_session_email

    def add(self):
        self.user_session_email['email_count'] = 2
        self.user_session_email['date'] = str(datetime.now().date())
        self.save()

    def update(self):
        self.user_session_email['email_count'] -= 1
        self.save()

    def __str__(self):
        return f'{self.user_session_email.get("email_count"), self.user_session_email.get("date")}'

    def clear(self):
        del self.session[settings.USER_SESSION_EMAIL_ID]
        self.save()

    def update_date_count(self):
        data_now = str(datetime.now().date())
        if self.user_session_email['date'] != data_now:
            self.user_session_email['date'] = data_now
            self.user_session_email['email_count'] = 2
        self.save()

    def save(self):
        self.session.modified = True


def get_today():
    date1 = datetime.now()
    return date(date1.year, date1.month, date1.day)


def get_date(req_day):
    try:
        year, month, day = (int(x) for x in req_day.split('-'))
        return date(year, month, day)
    except:
        return get_today()


def navigate_month(day, prev=None):
    m = 1
    if prev:
        m = -1
    n = (day + relativedelta(months=m))
    next_m = n.replace(day=1)
    return {"slug": next_m.isoformat(), 'name': next_m.strftime("%B %Y").title()}


"""-----|UserSessionToDo|-----"""


class UserSessionToDo:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    def __init__(self, request, sess=None):

        if sess:
            self.session = request
        else:
            self.session = request.session
        user_session_todo = self.session.get(settings.USER_SESSION_TODO_ID)

        if not user_session_todo:
            user_session_todo = self.session[settings.USER_SESSION_TODO_ID] = {}
            self.todo_days = user_session_todo
            self.month = get_today()
        self.todo_days = user_session_todo

    def new_obj(self, day):

        new_day = self.todo_days[day] = {'actual': [],
                                         'close': [],
                                         'slug': day,
                                         'name': get_date(day).strftime("%A %d %B %Y").title()}
        self.save()
        return new_day

    def get_obj(self, day):
        # Проверяем являться day == форматом datetime , иначе дату сегодня возвращаем
        day = get_date(day).isoformat()
        obj = self.todo_days.get(day, None)
        # Если объекта нет, то создаем новый
        if not obj:
            obj = self.new_obj(day)
        return obj

    def add_todo(self, todo, key):
        self.todo_days[key]['actual'].append(todo)
        self.save()

    def replace_del(self, slug, post, rep=False):
        post = post.split(',')
        old_flag = post[1]
        todo = post[0]
        flags = ['actual', 'close']
        flags.remove(post[1])
        new_flag = flags[0]
        # Удаляем объект
        self.todo_days[slug][old_flag].remove(todo)
        if rep:
            # То добавляем в противоположный словарь
            self.todo_days[slug][new_flag].append(todo)
        self.save()

    def get_actual_count(self):
        list_actual_day = [day for day in self.todo_days.values() if day.get('actual')]
        return len(list_actual_day)

    def get_actual_todo(self):

        list_actual = []
        count = 0
        for day in self.todo_days.values():
            if day.get('actual'):
                if get_today() >= get_date(day.get('slug')):
                    count += 1
                    list_actual.append(day)
        todo_actual_session = sorted(list_actual, key=itemgetter('slug'), reverse=True)[:3]
        data = {'list_actual': todo_actual_session, 'count_actual': self.get_actual_count}
        return data

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.USER_SESSION_TODO_ID]
        self.save()


"""-----|UserSessionApp|-----"""


class UserSessionApp:

    def __init__(self, request):
        self.session = request.session
        user_session = self.session.get(settings.USER_SESSION)
        if not user_session:
            user_session = self.session[settings.USER_SESSION] = {}
            self.user_session = user_session
        else:
            self.user_session = user_session

    def profile_previous_path(self, path):
        self.user_session['profile_previous_path'] = path
        self.save()

    def get_profile_previous_path(self):
        return self.user_session.get('profile_previous_path')

    def save(self):
        self.session.modified = True
