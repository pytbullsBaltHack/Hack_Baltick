from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SourceAddForm
from webface.models import StreamSource


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi, {username}! Your account has been created!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   # request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def streams(request):
    if request.method == 'POST':
        s_form = SourceAddForm(request.POST)
        # has_streams = StreamSource.objects.\
        #     filter(user=request.user, camera_source=s_form['camera_source']).first()
        # if has_streams is None:
        if s_form.is_valid():
            stream_source = s_form.save(commit=False)
            stream_source.user = request.user
            stream_source.save()
            messages.success(request, f'Your source has been added!')
            return redirect('streams')
        else:
            messages.warning(request, f'Form is invalid!')
        # else:
        #     messages.warning(request, f'You already have this source!')

    else:
        s_form = SourceAddForm(initial={'camera_source': ''})

    str_src = StreamSource.objects.filter(user=request.user).all()
    context = {
        's_form': s_form,
        'sources': str_src
    }

    return render(request, 'users/streams.html', context)


# @login_required
# def add_stream(request):
#     source = request.GET['source']
#     new_source = StreamSource(user=request.user, camera_source=source)
#     new_source.save()
#     messages.success(request, 'Your source has been added!')
#
#     return redirect('streams')
#
#
# @login_required
# def change_stream(request, source):
#     stream = StreamSource.objects.filter(user=request.user, camera_source=source).first()
#     # messages.warning(request, 'Your source has been deleted!!!')
#
#     return redirect('streams')


@login_required
def delete_stream(request, source):
    StreamSource.objects.filter(user=request.user, camera_source=source).delete()
    messages.warning(request, 'Your source has been deleted!!!')

    return redirect('streams')
