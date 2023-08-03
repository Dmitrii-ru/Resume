from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect, get_object_or_404
from .cache import get_model_all, get_single_model_obj, get_filter_model, get_mtm_all, count_send_email, \
    get_model_all_order
from .models import AboutMe, MyEducation, Stack, Project, CardProject
from django.views.generic import ListView
from .forms import EmailSendForm, FeedbackForm
from .tasks import send_email_task
from user_app.user_session import UserSessionToDo, UserSessionEmail, get_today, get_date, navigate_month
from .forms import AddTodo
from .python_prog.calendar_session_todo import MyCalendar


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    context = {}
    about_me = get_model_all(AboutMe)
    if about_me:
        context['about_me'] = about_me[0]
    context['my_education'] = get_model_all_order(MyEducation, '-percent')
    context['stacks'] = get_model_all(Stack)
    return render(request, 'resume/resume.html', context=context)


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resume_urls:index')
    else:
        form = FeedbackForm()
    context = {'form': form}
    return render(request, 'resume/feedback.html', context=context)


def send_email_view(request):
    ip = get_ip(request)
    stacks = Stack.objects.all()
    user_s = UserSessionEmail(request)
    # Обновляю дату
    user_s.update_date_count()
    # count = user_s.user_session_email['email_count']
    count = count_send_email(ip)
    count_bool = count < 2
    if count_bool:

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
                user_s.update(ip)
                return redirect('resume_urls:index')
        else:
            form = EmailSendForm()
        return render(request, 'resume/send_email.html',
                      {'form': form, 'stacks': stacks, 'count': abs(count - 2), 'count_bool': count_bool,
                       'letter': letter})

    else:
        return render(request, 'resume/send_email.html', {'stacks': stacks})


class ProjectsView(ListView):
    model = Project

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectsView, self).get_context_data(**kwargs)
        context['stacks'] = get_model_all(Stack)
        context['stack'] = get_single_model_obj(Stack, 'slug', self.kwargs['stack_slug'])
        context['projects'] = get_filter_model(Project, 'stacks__slug', self.kwargs['stack_slug'])
        context['stack_slug'] = self.kwargs['stack_slug']
        return context


def TodoSessionView(request, **kwargs):
    ust = UserSessionToDo(request)
    form_add_todo = AddTodo()
    if request.method == "POST":
        print(request.POST)
        print(request.session.session_key)
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
    print(post_date)
    if request.method == 'POST':
        if request.POST.get('replace'):
            ust.replace_del(kwargs['slug_day'], post_date['replace'].split(','), rep=True)
        elif request.POST.get('del'):
            ust.replace_del(kwargs['slug_day'], post_date['del'].split(','))
    return redirect('resume_urls:todo_session_day', kwargs['slug_day'])


class ProjectDetailView(ListView):
    model = CardProject

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = get_single_model_obj(Project, 'slug', self.kwargs['project_slug'])
        context['project'] = project
        context['cards'] = get_filter_model(CardProject, 'project', project)
        context['stacks'] = get_mtm_all(Project, 'stacks', project)
        return context
