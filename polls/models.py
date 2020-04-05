from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
STATUT_CHOICE=[
    (0, 'Non affecter'),
    (1, 'Negociation'),
    (2, 'Tarification fixe'),
    (3, 'En route'),
    (4, 'Arrivée'),
]


#affectation





#tarification

#user

class UserManager(BaseUserManager):
    def create_user(self, email,nom, prenom, adresse, phone, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nom=nom,
            prenom=prenom,
            adresse=adresse,
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,nom, prenom, adresse, phone, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            nom=nom,
            prenom=prenom,
            adresse=adresse,
            phone=phone
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='adresse mail',
        max_length=255,
        unique=True,
    )
    nom=models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    adresse = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    client = models.BooleanField(default=True)
    transport = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'adresse', 'phone'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.nom

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    @property
    def is_client(self):
        "Is the user a client"
        return self.client

    @property
    def is_transport(self):
        "Is the user transporteur?"
        return self.transport

    objects = UserManager()

#annonce trajet
class AnnonceTrajet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    statut = models.IntegerField( default=0, choices=STATUT_CHOICE)
    lieuDepart = models.CharField(max_length=50, verbose_name='Lieu de Depart')
    lieuArrivee = models.CharField(max_length=50, verbose_name="Lieu d'arrivée")
    lieuArret=models.CharField(max_length=250, verbose_name="Les lieu d'arret")
    moyen = models.CharField(max_length=200, verbose_name='Moyen de transport')
    killometreDevier = models.FloatField(verbose_name='Killometre a devier')
    volume = models.FloatField(verbose_name='Volume Maximum de la marchandise')
    poids = models.FloatField(verbose_name='Poids MAximum')
    dateEnvoi = models.DateField(verbose_name="Date d'envoi")
    regulier= models.BooleanField(default=True, verbose_name='Trajet Régulier')
    #si regulier
    frequence=models.IntegerField(null=True, verbose_name='Frequence')
    jourdep=models.CharField(max_length=50, null=True, verbose_name='Jour deplacement')
    #sinon
    dateDepot = models.DateField(null=True, verbose_name='Date de déposition')
    tarif = models.CharField(max_length=20, default="150DA")


#annonce marchandise
class AnnonceMarchandise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    statut = models.IntegerField( default=0, choices=STATUT_CHOICE)
    description = models.TextField(verbose_name='Description')
    lieuDepart = models.CharField(max_length=50, verbose_name='Lieu de depart')
    lieuArrivee = models.CharField(max_length=50, verbose_name="Lieu d'arrivée")
    adresseDepart = models.CharField(max_length=200, verbose_name="Adresse de depart")
    adresseArivee = models.CharField(max_length=200, verbose_name="Adresse d'arrivée")
    dateEnvoi = models.DateField(verbose_name="Date d'envoie")
    dateDepot = models.DateField(verbose_name="Date de déposition")
    volume = models.FloatField(verbose_name="Volume de la marchandise")
    poids = models.FloatField(verbose_name="Poid de la marchandise")
    demandesSpeciales= models.TextField(null=True, verbose_name="Demandes Spéciales")
    photo= models.ImageField(null=True, verbose_name='Photo de la marchandise')
    tarif = models.CharField(max_length=20, default="150DA")



class Affectation(models.Model):
    marchandise = models.ForeignKey(AnnonceMarchandise, on_delete=models.CASCADE, null=True)
    trajet = models.ForeignKey(AnnonceTrajet, on_delete=models.CASCADE, null=True)
    statut = models.IntegerField(default=0, choices=STATUT_CHOICE)
    tarif=models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        tarification = 50 + (self.marchandise.poids) * 0.2 + (self.marchandise.volume) * 0.2+ (self.trajet.killometreDevier)*0.4
        self.tarif=str(tarification)+ 'DA'
        self.marchandise.tarif=str(tarification)+ 'DA'
        self.trajet.tarif=str(tarification)+ 'DA'
        self.marchandise.statut= 1
        self.trajet.statut=1
        self.trajet.save()
        self.marchandise.save()
        super(Affectation, self).save(*args, **kwargs)








