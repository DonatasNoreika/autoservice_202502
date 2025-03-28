from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from tinymce.models import HTMLField
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    class Meta:
        verbose_name = "Profilis"
        verbose_name_plural = "Profiliai"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        # Apkarpyti nuotrauką į kvadratą
        if img.height != img.width:
            min_dim = min(img.height, img.width)
            left = (img.width - min_dim) / 2
            top = (img.height - min_dim) / 2
            right = (img.width + min_dim) / 2
            bottom = (img.height + min_dim) / 2
            img = img.crop((left, top, right, bottom))

        # Sumažinti nuotraukos dydį
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)


class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
    price = models.FloatField(verbose_name="Kaina")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"


class CarModel(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=100)
    model = models.CharField(verbose_name="Modelis", max_length=100)

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = "Modelis"
        verbose_name_plural = "Modeliai"


class Car(models.Model):
    car_model = models.ForeignKey(to="CarModel", verbose_name="Modelis", on_delete=models.SET_NULL, null=True,
                                  blank=True)
    license_plate = models.CharField(verbose_name="Valstybinis numeris", max_length=10, unique=True)
    vin_code = models.CharField(verbose_name="VIN kodas", max_length=20)
    client_name = models.CharField(verbose_name="Klientas", max_length=100)
    photo = models.ImageField('Nuotrauka', upload_to='cars', null=True, blank=True)
    description = HTMLField(verbose_name="Aprašymas", max_length=5000, default="")

    def __str__(self):
        return f"{self.car_model} - {self.license_plate}"

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Order(models.Model):
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    car = models.ForeignKey(to="Car", verbose_name="Automobilis", on_delete=models.CASCADE, related_name="orders")
    client = models.ForeignKey(to=User, verbose_name="Klientas", on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateTimeField(verbose_name="Gražinimo terminas", null=True, blank=True)

    def is_overdue(self):
        if self.deadline and datetime.today() > self.deadline:
            return True
        return False

    is_overdue.short_description = "Ar praėjo terminas?"

    ORDER_STATUS = (
        ('p', 'Administruojama'),
        ('v', 'Vykdoma'),
        ('i', 'Įvykdyta'),
        ('a', 'Atšaukta'),
    )

    status = models.CharField(verbose_name="Būsena", max_length=1, choices=ORDER_STATUS, default="p")

    def total_sum(self):
        total = 0
        lines = self.lines.all()
        for line in lines:
            total += line.service.price * line.quantity
        return total

    total_sum.short_description = "Bendra užsakymo suma"

    def __str__(self):
        return f"{self.car} ({self.deadline})"

    class Meta:
        verbose_name = "Taisymas"
        verbose_name_plural = "Taisymai"
        ordering = ['-id']


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(verbose_name="Kiekis", default=1)

    def line_sum(self):
        return self.service.price * self.quantity

    line_sum.short_description = "Suma"

    def __str__(self):
        return f"{self.service} - {self.quantity} ({self.order})"

    class Meta:
        verbose_name = "Eilutė"
        verbose_name_plural = "Eilutės"


class OrderComment(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Taisymas", on_delete=models.SET_NULL, null=True, blank=True,
                              related_name="comments")
    author = models.ForeignKey(to=User, verbose_name="Komentatorius", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    content = models.TextField(verbose_name="Komentaras", max_length=2000)

    class Meta:
        verbose_name = "Komentaras"
        verbose_name_plural = 'Komentarai'
        ordering = ['-date_created']
