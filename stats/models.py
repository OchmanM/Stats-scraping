from django.db import models

# Create your models here.


class Guild:
    name = models.CharField(max_length=100)


class Player(models.Model):
    SEX_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    VOCATION_CHOICES = (
        ('No Vocation', "No Vocation"),
        ("Knight", "Knight"),
        ("Paladin", "Paladin"),
        ("Druid", "Druid"),
        ("Sorcerer", "Sorcerer"),
        ("Elite Knight", "Elite Knight"),
        ("Royal Paladin", "Royal Paladin"),
        ("Elder Druid", "Elder Druid"),
        ("Master Sorcerer", "Master Sorcerer"),
    )
    ONLINE_CHOICES = (
        ("ONLINE", "ONLINE"),
        ("OFFLINE", "OFFLINE"),
    )
    #FK:

    name = models.CharField(max_length=100, unique=True)
    guild = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=7)
    level = models.PositiveSmallIntegerField()
    vocation = models.CharField(choices=VOCATION_CHOICES, max_length=50)
    house = models.CharField(null=True, max_length=100, blank=True)
    status = models.CharField(choices=ONLINE_CHOICES, max_length=10)
    lastlogin = models.DateTimeField()
    comment = models.CharField(null=True, blank=True, max_length=500)

    def __str__(self):
        return self.name


class Deaths(models.Model):
    text = models.CharField(max_length=500)
    killed = models.ForeignKey(Player, null=True, on_delete=models.CASCADE, related_name='killed')
    killer = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE, related_name='killer')
    date = models.DateTimeField()
    level = models.PositiveSmallIntegerField()
    pvp = models.BooleanField()

    class Meta:
        ordering = ('date',)


class OnlineDetails(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    level = models.PositiveSmallIntegerField(null=True, blank=True)
    login = models.DateTimeField()
    logout = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.player.name + " " + str(self.logout) if self.logout else self.player.name

    class Meta:
        ordering = ('logout', 'login')


class CeleryInUse(models.Model):
    is_in_use = models.BooleanField()

    def __str__(self):
        return str(self.is_in_use)