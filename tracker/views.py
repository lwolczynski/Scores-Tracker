from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, NewGameForm
from .models import Game, Score9, Score18
from datetime import datetime, timezone
import json

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
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registered and logged in succesfully.")
            return redirect('index')
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

#New game view
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
        if scores_number >= 7:
            return JsonResponse({'status': 'ok', 'message': {'tag': 'danger', 'text': 'Maximum number of player players (6) reached!'}})
        score = Score9(par_tracker=False, name='Player', game=game)
    elif game.holes.number == 18:
        scores_number = Score18.objects.filter(game=game).count()
        if scores_number >= 7:
            return JsonResponse({'status': 'ok', 'message': {'tag': 'danger', 'text': 'Maximum number of player players (6) reached!'}})
        score = Score18(par_tracker=False, name='Player', game=game)
    score.save()
    return JsonResponse({'status': 'ok', 'message': {'tag': 'success', 'text': 'New player added.'}, 'score': score.as_dict()})