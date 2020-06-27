from django.db import models
from django.contrib.auth.models import User

class Sport(models.Model):
    name = models.CharField(max_length=30)

class HolesNumber(models.Model):
    number = models.SmallIntegerField()

class Game(models.Model):
    owner = models.ForeignKey(User, on_delete = models.PROTECT)
    time_created = models.DateTimeField(auto_now_add=True)
    sport = models.ForeignKey(Sport, on_delete = models.PROTECT)
    holes = models.ForeignKey(HolesNumber, on_delete = models.PROTECT)
    notes = models.CharField(max_length=1000)

class ScoreTable(models.Model):
    par_tracker = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete = models.PROTECT)
    
    class Meta:
        abstract = True

class Score9(ScoreTable):
    hole1 = models.SmallIntegerField()
    hole2 = models.SmallIntegerField()
    hole3 = models.SmallIntegerField()
    hole4 = models.SmallIntegerField()
    hole5 = models.SmallIntegerField()
    hole6 = models.SmallIntegerField()
    hole7 = models.SmallIntegerField()
    hole8 = models.SmallIntegerField()
    hole9 = models.SmallIntegerField()

class Score18(ScoreTable):
    hole1 = models.SmallIntegerField()
    hole2 = models.SmallIntegerField()
    hole3 = models.SmallIntegerField()
    hole4 = models.SmallIntegerField()
    hole5 = models.SmallIntegerField()
    hole6 = models.SmallIntegerField()
    hole7 = models.SmallIntegerField()
    hole8 = models.SmallIntegerField()
    hole9 = models.SmallIntegerField()
    hole10 = models.SmallIntegerField()
    hole11 = models.SmallIntegerField()
    hole12 = models.SmallIntegerField()
    hole13 = models.SmallIntegerField()
    hole14 = models.SmallIntegerField()
    hole15 = models.SmallIntegerField()
    hole16 = models.SmallIntegerField()
    hole17 = models.SmallIntegerField()
    hole18 = models.SmallIntegerField()
