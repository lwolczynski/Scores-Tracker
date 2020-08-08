from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
    reset_password = models.BooleanField(default=False)

class Sport(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class HolesNumber(models.Model):
    number = models.SmallIntegerField()

    def __str__(self):
        return str(self.number)

class Game(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete = models.PROTECT)
    time_created = models.DateTimeField(editable=False)
    sport = models.ForeignKey(Sport, on_delete = models.PROTECT)
    holes = models.ForeignKey(HolesNumber, on_delete = models.PROTECT)
    notes = models.CharField(max_length=1000, blank=True)

    def getTs(self):
        return int(self.time_created.timestamp())

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.time_created = timezone.localtime(timezone.now()).replace(microsecond=0)
        return super(Game, self).save(*args, **kwargs)

    def as_dict(self):
        return {
            "id": self.id,
            "sport": self.sport.name,
            "holes": self.holes.number,
            "time_created": self.time_created,
            "timestamp": self.getTs(),
            "notes": self.notes,
        } 

    def as_dict_with_players(self):
        if self.holes.number == 9:
            players = Score9.objects.filter(game=self).count()-1
        elif self.holes.number == 18:
            players = Score18.objects.filter(game=self).count()-1
        return {
            "id": self.id,
            "sport": self.sport.name,
            "holes": self.holes.number,
            "players": players,
            "time_created": self.time_created,
            "timestamp": self.getTs(),
        } 

class ScoreTable(models.Model):
    par_tracker = models.BooleanField(default=False)
    name = models.CharField(max_length=30, blank=True)
    game = models.ForeignKey(Game, on_delete = models.PROTECT)
    
    class Meta:
        abstract = True

class Score9(ScoreTable):
    hole1 = models.SmallIntegerField(blank=True, null=True)
    hole2 = models.SmallIntegerField(blank=True, null=True)
    hole3 = models.SmallIntegerField(blank=True, null=True)
    hole4 = models.SmallIntegerField(blank=True, null=True)
    hole5 = models.SmallIntegerField(blank=True, null=True)
    hole6 = models.SmallIntegerField(blank=True, null=True)
    hole7 = models.SmallIntegerField(blank=True, null=True)
    hole8 = models.SmallIntegerField(blank=True, null=True)
    hole9 = models.SmallIntegerField(blank=True, null=True)

    def as_dict(self):
        return {
            "id": self.id,
            "par_tracker": self.par_tracker,
            "name": self.name,
            "scoring": {
                "hole1": self.hole1,
                "hole2": self.hole2,
                "hole3": self.hole3,
                "hole4": self.hole4,
                "hole5": self.hole5,
                "hole6": self.hole6,
                "hole7": self.hole7,
                "hole8": self.hole8,
                "hole9": self.hole9
            }
        } 

class Score18(ScoreTable):
    hole1 = models.SmallIntegerField(blank=True, null=True)
    hole2 = models.SmallIntegerField(blank=True, null=True)
    hole3 = models.SmallIntegerField(blank=True, null=True)
    hole4 = models.SmallIntegerField(blank=True, null=True)
    hole5 = models.SmallIntegerField(blank=True, null=True)
    hole6 = models.SmallIntegerField(blank=True, null=True)
    hole7 = models.SmallIntegerField(blank=True, null=True)
    hole8 = models.SmallIntegerField(blank=True, null=True)
    hole9 = models.SmallIntegerField(blank=True, null=True)
    hole10 = models.SmallIntegerField(blank=True, null=True)
    hole11 = models.SmallIntegerField(blank=True, null=True)
    hole12 = models.SmallIntegerField(blank=True, null=True)
    hole13 = models.SmallIntegerField(blank=True, null=True)
    hole14 = models.SmallIntegerField(blank=True, null=True)
    hole15 = models.SmallIntegerField(blank=True, null=True)
    hole16 = models.SmallIntegerField(blank=True, null=True)
    hole17 = models.SmallIntegerField(blank=True, null=True)
    hole18 = models.SmallIntegerField(blank=True, null=True)

    def as_dict(self):
        return {
            "id": self.id,
            "par_tracker": self.par_tracker,
            "name": self.name,
            "scoring": {
                "hole1": self.hole1,
                "hole2": self.hole2,
                "hole3": self.hole3,
                "hole4": self.hole4,
                "hole5": self.hole5,
                "hole6": self.hole6,
                "hole7": self.hole7,
                "hole8": self.hole8,
                "hole9": self.hole9,
                "hole10": self.hole10,
                "hole11": self.hole11,
                "hole12": self.hole12,
                "hole13": self.hole13,
                "hole14": self.hole14,
                "hole15": self.hole15,
                "hole16": self.hole16,
                "hole17": self.hole17,
                "hole18": self.hole18
            }
        } 