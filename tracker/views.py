import os
import json

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import SignUpForm, NewGameForm
from .tokens import account_activation_token
from .models import CustomUser, Game, Score9, Score18
from datetime import datetime, timezone

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email

def index(request):
    return render(request = request,
                  template_name = "index.html")

#Register view
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            site = get_current_site(request) # get the domain
            message = render_to_string('emails/activate_account.html', {
                'user': user,
                'protocol': 'http',
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # SendGrid setup
            message = Mail(
                from_email=Email("donotreply@myscore.golf", "MyScore"),
                to_emails=user.email,
                subject='Activate your MyScore account',
                html_content=message)
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)  # .status_code, .body, .headers
                messages.warning(request, 'A verification email has been sent.')
                return redirect('login')
            except Exception as e:
                print(e)  # e.message
                messages.warning(request, str(e))
    else:
        form = SignUpForm
    return render(request, 'register.html', {'form': form})

#Login view
def login_request(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in succesfully.")
                return redirect('index')
            else:
                messages.warning(request, "Invalid username or password.")
        else:
            messages.warning(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

#Logout view
@login_required
def logout_request(request):
    logout(request)
    messages.success(request, "Logged out succesfully.")
    return redirect('index')

#Activate account view
def activate(request, uidb64, token):
    """Check the activation token sent via mail."""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        messages.warning(request, str(e))
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, 'Account activated. You have been logged in.')
    else:
        messages.warning(request, 'Account activation link is invalid.')
    return redirect('index')

#New game view
@login_required
def new_game(request):
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.owner = request.user
            game.save()
            if game.holes.number == 9:
                par_tracker = Score9(par_tracker=True, name='Par', game=game)
                par_tracker.save()
                score = Score9(par_tracker=False, name='Player', game=game)
                score.save()
            elif game.holes.number == 18:
                par_tracker = Score18(par_tracker=True, name='Par', game=game)
                par_tracker.save()
                score = Score18(par_tracker=False, name='Player', game=game)
                score.save()
            return redirect('game_edit', game_id=game.id, timestamp=game.getTs())
    else:
        form = NewGameForm
    return render(request, 'new_game.html', {'form': form})

#Game view
def history(request):
    games = Game.objects.filter(owner=request.user).order_by('-id')
    return render(request, "history.html", {'games': [game.as_dict_with_players() for game in games]})

#Game view
def game(request, game_id, timestamp):
    date = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc).astimezone(tz=None)
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return redirect('index')
    if game.time_created!=date:
        return redirect('index')
    return render(request, "game.html", {'edit': False, 'game': game.as_dict()})

#Game edit view
@login_required
def game_edit(request, game_id, timestamp):
    date = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc).astimezone(tz=None)
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return redirect('index')
    if game.time_created!=date or game.owner!=request.user:
        return redirect('index')
    return render(request, "game_edit.html", {'edit': True, 'game': game.as_dict()})

#Get scores view
def get_scores(request, game_id, timestamp):
    date = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc).astimezone(tz=None)
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=500)
    if game.time_created!=date:
        return JsonResponse({'status': 'error'}, status=500)
    if game.holes.number == 9:
        try:
            scores = Score9.objects.filter(game=game)
        except Score9.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=500)
    elif game.holes.number == 18:
        try:
            scores = Score18.objects.filter(game=game)
        except Score18.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=500)
    else:
        return JsonResponse({'status': 'error'}, status=500)
    return JsonResponse({'status': 'ok', 'scores': [score.as_dict() for score in scores]})

#Save scores view
@login_required
def save_scores(request, game_id, timestamp):
    date = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc).astimezone(tz=None)
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=500)
    if game.time_created!=date or game.owner!=request.user:
        return JsonResponse({'status': 'error'}, status=500)
    json_received = json.loads(request.body.decode())
    for score_received in json_received['scores']:
        if game.holes.number == 9:
            try:
                score = Score9.objects.get(pk=score_received['id'])
            except Score9.DoesNotExist:
                return JsonResponse({'status': 'error'}, status=500)
        elif game.holes.number == 18:
            try:
                score = Score18.objects.get(pk=score_received['id'])
            except Score18.DoesNotExist:
                return JsonResponse({'status': 'error'}, status=500)
        if score.game.owner == request.user:
            if not score.par_tracker:
                score.name=score_received['name']
            for (key, value) in score_received['scoring'].items():
                setattr(score, key, value)
            score.save()
    game.notes = json_received['notes']
    return JsonResponse({'status': 'ok', 'message': {'tag': 'success', 'text': 'Saved successfully.'}})

#Add player view
@login_required
def add_player(request, game_id, timestamp):
    date = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc).astimezone(tz=None)
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=500)
    if game.time_created!=date or game.owner!=request.user:
        return JsonResponse({'status': 'error'}, status=500)
    if game.holes.number == 9:
        scores_number = Score9.objects.filter(game=game).count()
        if scores_number >= 11:
            return JsonResponse({'status': 'ok', 'message': {'tag': 'danger', 'text': 'Maximum number of player players (10) reached!'}})
        score = Score9(par_tracker=False, name='Player', game=game)
    elif game.holes.number == 18:
        scores_number = Score18.objects.filter(game=game).count()
        if scores_number >= 11:
            return JsonResponse({'status': 'ok', 'message': {'tag': 'danger', 'text': 'Maximum number of player players (10) reached!'}})
        score = Score18(par_tracker=False, name='Player', game=game)
    score.save()
    return JsonResponse({'status': 'ok', 'message': {'tag': 'success', 'text': 'New player added.'}, 'score': score.as_dict()})