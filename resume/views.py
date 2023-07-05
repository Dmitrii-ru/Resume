from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect, get_object_or_404

from .cache import get_cache_resume, get_filter_cards, get_filter_stacks
from .models import AboutMe, MyEducation, Stack, Projects, CardProject
from django.views.generic import ListView
from .forms import EmailSendForm
from .tasks import send_email_task
from user_app.user_session import UserSessionToDo, UserSessionEmail, get_today, get_date, navigate_month
from .forms import AddTodo
from .python_prog.calendar_session_todo import MyCalendar
from django.core.cache import cache


# def cache_index():
#     print(cache)
#     index_cache_list = cache.get('index_cache')
#     if not index_cache_list:
#         index_cache_list = {
#             'about_me': AboutMe.objects.all().first(),
#             'my_education': MyEducation.objects.all(),
#             'stacks': Stack.objects.all(),
#         }
#         cache.set('index_cache', index_cache_list, 60*60)
#     return index_cache_list


def index(request):
    context = {'about_me': get_cache_resume(model='index_key', name='about_me'),
               'my_education': get_cache_resume(model='index_key', name='my_education'),
               'stacks': get_cache_resume(model='index_key', name='stacks_all')}
    # 'my_education': get_cache('my_education'),
    # 'stacks': get_cache('stacks')}

    return render(request, 'resume/resume.html', context=context)


def send_email_view(request):
    stacks = Stack.objects.all()
    user_s = UserSessionEmail(request)
    # Обновляю дату
    user_s.update_date_count()
    count = user_s.user_session_email['email_count']

    if count != 0:
        letter = 'письмо' if count == 1 else 'письма'
        if request.method == 'POST':
            form = EmailSendForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                name = form.cleaned_data.get('name')
                send_email_task.delay(name=name,
                                      to_send=email,
                                      subject=1,
                                      massage_num=1,
                                      )
                user_s.update()
                return redirect('resume_urls:index')
        else:
            form = EmailSendForm()
        return render(request, 'resume/send_email.html',
                      {'form': form, 'stacks': stacks, 'count': count, 'letter': letter})

    else:
        return render(request, 'resume/send_email.html', {'stacks': stacks})


class ProjectsView(ListView):
    model = Projects

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectsView, self).get_context_data(**kwargs)
        stacks = get_cache_resume(model='index_key', name='stacks_all')
        stack = stacks.get(slug=self.kwargs['stack_slug'])

        projects = Projects.objects.filter(prod_stack__slug=self.kwargs['stack_slug'])
        context['stack'] = stack
        context['projects'] = projects
        context['stacks'] = stacks
        context['stack_slug'] = self.kwargs['stack_slug']
        return context


def TodoSessionView(request, **kwargs):
    ust = UserSessionToDo(request)

    form_add_todo = AddTodo()
    if request.method == "POST":
        post = request.POST.copy()
        post['day_slug'] = request.POST['add']
        post['sess'] = request.session.session_key
        form_add_todo = AddTodo(post)

        if form_add_todo.is_valid():
            ust.add_todo(request.POST['todo'], request.POST['add'])
            return redirect(request.path)
    today = get_today().isoformat()
    # Если нет дня то берем день сегодня
    day = ust.get_obj(kwargs.get('slug_day', today))
    # Берем текущий месяц и год
    day_datetime = get_date(day['slug'])
    cal = MyCalendar(day_datetime.year, day_datetime.month, ust)
    html_cal = cal.formatmonth(withyear=True)
    next_m = navigate_month(day_datetime)
    prev_m = navigate_month(day_datetime, prev=True)
    today_day = {'slug': today}
    context = {'cal': mark_safe(html_cal),
               'day': day,
               'form_add_todo': form_add_todo,
               'next_m': next_m,
               'prev_m': prev_m,
               'today_day': today_day,
               'style_btn1': 'btn btn-outline-dark',
               }

    return render(request, 'resume/todo_session.html', context)


def TodoDelReplaceSessionView(request, **kwargs):
    ust = UserSessionToDo(request)
    post_date = request.POST
    if request.method == 'POST':
        if request.POST.get('replace'):
            ust.replace_del(kwargs['slug_day'], post_date['replace'], rep=True)
        elif request.POST.get('del'):
            ust.replace_del(kwargs['slug_day'], post_date['del'])
    return redirect('resume_urls:todo_session_day', kwargs['slug_day'])


class ProjectsDetailView(ListView):
    model = CardProject

    def get_context_data(self, **kwargs):
        context = super(ProjectsDetailView, self).get_context_data(**kwargs)
        project = get_object_or_404(get_cache_resume('project_key', 'projects_all'), slug=self.kwargs['project_slug'])
        context['project'] = project
        context['cards'] = get_filter_cards('project_key', 'cards_all', project)
        context['stacks'] = get_filter_stacks('index_key', 'stacks_all', project)
        return context
