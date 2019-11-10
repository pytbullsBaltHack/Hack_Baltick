from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SourceAddForm
from webface.models import StreamSource, UserFace, Visitor, Event


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
        has_streams = StreamSource.objects.\
            filter(user=request.user, camera_source=s_form['camera_source'].value()).first()
        if has_streams is None:
            try:
                event = Event.objects.filter(pk=int(s_form['event_id'].value())).first()
            except Exception:
                event = None
            if event != None:
                if s_form.is_valid():
                    stream_source = s_form.save(commit=False)
                    stream_source.user = request.user
                    stream_source.save()
                    messages.success(request, f'Your source has been added!')
                    return redirect('streams')
                else:
                    messages.warning(request, f'Form is invalid!')
            else:
                messages.warning(request, f'Event Id is invalid!')
        else:
            messages.warning(request, f'You already have this source!')

    else:
        s_form = SourceAddForm(initial={'camera_source': '', 'event_id': ''})

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


@login_required
def events2(request, ev_id=-1, is_review=0):
    all_events = Event.objects.filter(user=request.user).all()
    if ev_id != -1:
        visitors = Visitor.objects.filter(user=request.user, event_id=ev_id).all()
        full_visitors = []
        for visitor in visitors:
            if visitor.real_user_id > 0:
                userface = UserFace.objects.filter(pk=visitor.real_user_id).first()
                full_visitors.append((visitor, userface))
            else:
                full_visitors.append((visitor, None))

        if is_review:
            visitors_num = len(visitors)
            known_num = len([k for v, k in full_visitors if k != None])
        else:
            visitors_num = None
            known_num = None

    else:
        full_visitors = None
        visitors_num = None
        known_num = None

    context = {
        'is_review': is_review,
        'visitors_num': visitors_num,
        'known_num': known_num,
        'events': all_events,
        'visitors': full_visitors
    }

    return render(request, 'users/events.html', context)


@login_required
def events(request, ev_id=-1):
    all_events = Event.objects.filter(user=request.user).all()
    if ev_id != -1:
        visitors = Visitor.objects.filter(user=request.user, event_id=ev_id).all()
        full_visitors = []
        for visitor in visitors:
            if visitor.real_user_id > 0:
                userface = UserFace.objects.filter(pk=visitor.real_user_id).first()
                full_visitors.append((visitor, userface))
            else:
                full_visitors.append((visitor, None))
    else:
        full_visitors = None

    is_review = 0
    visitors_num = None
    known_num = None
    context = {
        'is_review': is_review,
        'events': all_events,
        'visitors': full_visitors
    }

    return render(request, 'users/events.html', context)


@login_required
def choose_event(request, ev_id):
    return redirect('events', ev_id=ev_id)


@login_required
def overview_event(request, ev_id):
    return redirect('events2', ev_id=ev_id, is_review=1)
