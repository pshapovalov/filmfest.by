from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from hvad.models import TranslatableModel, TranslatedFields
from dirtyfields import DirtyFieldsMixin

from constants import YESNO, YESNOMAYBE, COUNTRIES, LANGUAGES,\
     SECTIONS, BACKLINKS


class Submission(models.Model, DirtyFieldsMixin):
    title = models.CharField(verbose_name=_('Original title'), max_length=1000)
    title_en = models.CharField(verbose_name=_('English title'),
                                max_length=1000)
    country = models.CharField(verbose_name=_('Country of production'),
                                max_length=2, choices=COUNTRIES)
    language = models.CharField(verbose_name=_('Language of original version'),
                                max_length=10, choices=LANGUAGES)
    genre = models.CharField(verbose_name=_('Genre'),
                             max_length=1000, blank=True, null=True)
    section = models.IntegerField(verbose_name=_('Section'),
                                  choices=SECTIONS)
    synopsis = models.TextField(verbose_name=_('Synopsis'))
    length = models.IntegerField(verbose_name=_('Runtime (in minutes)'))
    aspect_ratio = models.CharField(verbose_name=_('Aspect ratio'),
                                    max_length=1000)
    year = models.IntegerField(verbose_name=_('Year of production'))
    premiere = models.IntegerField(verbose_name=_('Premiere'), choices=YESNO) ##
    film_awards = models.TextField(verbose_name=_('Film awards'), blank=True)
    director_awards = models.TextField(
        verbose_name=_('Director awards'), blank=True)
    budget = models.CharField(verbose_name=_('Film budget'), max_length=1000)
    film_link = models.CharField(
        verbose_name=_('Link to download the film (optional)'),
        max_length=1000, blank=True
    )

    attend = models.IntegerField(
        verbose_name=_('I intend to visit final part of festival'),
        choices=YESNOMAYBE, default=0)
    backlink = models.IntegerField(
        verbose_name=_('The source of information about '\
                       'Cinema Perpetuum Mobile'),
        choices=BACKLINKS
    )##

    director = models.CharField(verbose_name=_('Name'),
                                max_length=1000)
    director_address = models.TextField(verbose_name=_('Address'))
    director_email = models.CharField(verbose_name=_('Email'),
                                      max_length=1000)
    director_site = models.CharField(verbose_name=_('Website'),
                                      max_length=1000, blank=True)
    director_phone = models.CharField(
        verbose_name=_('Tel.'),
        max_length=1000, blank=True)

    producer = models.CharField(verbose_name=_('Name'),
                                max_length=1000, blank=True)
    producer_address = models.TextField(verbose_name=_('Address'), blank=True)
    producer_email = models.CharField(
        verbose_name=_('Email'), max_length=1000, blank=True)
    producer_site = models.CharField(
        verbose_name=_('Website'), max_length=1000, blank=True)
    producer_phone = models.CharField(
        verbose_name=_('Tel.'),
        max_length=1000, blank=True)

    screenwriter = models.CharField(verbose_name=_('Script writer'),
                                    max_length=1000, blank=True)
    editor = models.CharField(verbose_name=_('Editor'),
                                 max_length=1000, blank=True)
    music = models.CharField(verbose_name=_('Music composer'),
                                max_length=1000, blank=True)
    director_photography = models.CharField(
        verbose_name=_('Director of photography'),
        max_length=1000, blank=True)
    other_credits = models.TextField(verbose_name=_('Other credits'), blank=True)

    
    allow_tv = models.IntegerField(
        verbose_name=_('Authorization to use excerpts of the film for promotion (max 10% of the total length) in television'),
        choices=YESNO, default=1)
    allow_noncommercial = models.IntegerField(
        verbose_name=_('Authorization to include the film in the festival video collection for non-commercial screenings'),
        choices=YESNO, default=1)
    allow_network = models.IntegerField(
        verbose_name=_('Authorization to screen the film at film festivals from Cinema Perpetuum Mobile partner network'),
        choices=YESNO, default=1)

    applicant = models.CharField(verbose_name=_('Name'),
                                max_length=1000)
    applicant_address = models.TextField(verbose_name=_('Address'))
    applicant_email = models.CharField(verbose_name=_('Email'),
                                      max_length=1000)
    applicant_site = models.CharField(verbose_name=_('Website'),
                                      max_length=1000, blank=True)
    applicant_phone = models.CharField(
        verbose_name=_('Tel.'),
        max_length=1000, blank=True)

    submission_language = models.CharField(
        verbose_name=_('Submission language'),
        max_length=2, choices=settings.LANGUAGES,
        default=settings.LANGUAGES[0][0])

    comment = models.TextField(
        verbose_name=_('Comment'), null=True, blank=True)
    comment_email_sent = models.BooleanField(
        verbose_name=_('E-mail was sent'), default=False)
    comment_film_received = models.BooleanField(
        verbose_name=_('Film is received'), default=False)
    comment_papers_received = models.BooleanField(
        verbose_name=_('Papers were received'), default=False)
    comment_vob_received = models.BooleanField(
        verbose_name=_('Vob received'), default=False)

    submitted_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Submitted at'))
    email_sent_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_('E-mail sent at'))
    film_received_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Film received at'))
    papers_received_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Papers received at'))
    vob_received_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Vob received at'))

    preview = models.FloatField(
        null=True, blank=True, verbose_name=_('Preview result'))
    previewers = models.IntegerField(
        null=True, blank=True, verbose_name=_('Previewers count'))

    def __unicode__(self):
        return 'Film %s' % (self.title)

    def __repr__(self):
        return '<Film %s>' % (self.title)

    def _track_facts(self):
        facts = {
            'comment_email_sent': 'email_sent_at',
            'comment_film_received': 'film_received_at',
            'comment_papers_received': 'papers_received_at',
            'comment_vob_received': 'vob_received_at',
        }
        dirty_fields = self.get_dirty_fields()

        now = datetime.now()

        for comment_field, date_field in facts.iteritems():
            value = getattr(self, comment_field)
            if comment_field in dirty_fields:
                if value == True:
                    new_datetime = now
                else:
                    new_datetime = None
                setattr(self, date_field, new_datetime)

    def save(self, *args, **kwargs):
        self._track_facts()

        dirty_fields = self.get_dirty_fields().copy()
        new_fact = lambda fact: getattr(self, fact) and fact in dirty_fields

        res = super(Submission, self).save(*args, **kwargs)

        countdown = 60 * 20  # 20 minutes
        if new_fact('comment_film_received'):
            from apps.cpm2013.tasks import SendEmailUpdate
            SendEmailUpdate().apply_async(
                args=[self.id, 'comment_film_received'],
                countdown=countdown
            )
        if new_fact('comment_papers_received'):
            from apps.cpm2013.tasks import SendEmailUpdate
            SendEmailUpdate().apply_async(
                args=[self.id, 'comment_papers_received'],
                countdown=countdown
            )

        return res

class NewsEntry(TranslatableModel):
    added_at = models.DateTimeField(auto_now_add=True)

    translations = TranslatedFields(
        title = models.CharField(verbose_name=_('Title'), max_length=100),
        short_text = models.TextField(verbose_name=_('Short text'), max_length=1000),
        text = models.TextField(verbose_name=_('Text'), max_length=1000),
    )

    __unicode__ = lambda self: self.title

class Page(TranslatableModel):
    slug = models.SlugField(max_length=50)

    translations = TranslatedFields(
        title = models.CharField(verbose_name=_('Title'), max_length=100),
        text = models.TextField(verbose_name=_('Text')),
    )

    __unicode__ = lambda self: self.slug

class LetterTemplate(TranslatableModel):
    code = models.SlugField(max_length=50, unique=True)

    translations = TranslatedFields(
        subject = models.CharField(verbose_name=_('Subject'), max_length=100),
        text = models.TextField(verbose_name=_('Text')),
    )

    def __unicode__(self):
        return self.code

class ActionRegistry(models.Model):
    code = models.CharField(verbose_name=_('Action code'), max_length=100,
                            db_index=True)
    at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('At'))
