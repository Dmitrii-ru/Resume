from django.shortcuts import render, redirect

from ather.forms import VisitCongratulation


# Create your views here.

def congratulation(request):
    return render(request, 'ather/congratulation.html')


def congratulation_password(request):
    if request.method == 'POST':
        copy_request = request.copy()
        form = VisitCongratulation(request.POST, copy_request)
        if form.is_valid():
            return redirect('ather:congratulation')
    else:
        form = VisitCongratulation()
    context = {'form': form}

    return render(request, 'ather/congratulation_password.html', context=context)
