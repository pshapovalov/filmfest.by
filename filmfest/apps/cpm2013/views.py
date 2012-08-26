import io
import os

from django.http import HttpResponse
from django.views.generic.create_update import create_object
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import translation
from django.conf import settings

from apps.cpm2013.models import Submission, NewsEntry, Page
from apps.cpm2013.forms import SubmissionForm

def index(request):
    news = NewsEntry.objects.language().order_by('-added_at')[:10]
    return render_to_response(
        'cpm2013/index.html',
        {'news': news},
        context_instance=RequestContext(request),
    )

def submit(request):
    return render_to_response(
        'cpm2013/submit_temp.html',
        {},
        context_instance=RequestContext(request),
    )

    return create_object(
        request, model=Submission, form_class=SubmissionForm,
        template_name='cpm2013/submit.html'
    )

def page(request, slug):
    base_page = get_object_or_404(Page, slug=slug)
    pages = base_page._meta.translations_model.objects.all()
    pages = dict((t.language_code, t) for t in pages)

    current_lang = translation.get_language()
    if current_lang in pages:
        page = pages[current_lang]
    else:
        for lang_code in ['en', 'ru', 'be']:
            if lang_code in pages:
                page = pages[lang_code]
                break

    return render_to_response(
        'cpm2013/page.html',
        {'page': page},
        context_instance=RequestContext(request),
    )

class Rules:
    BE = 'rules_ru.md'
    RU = 'rules_ru.md'
    EN = 'rules_ru.md'

    PATH = os.path.join(settings.PROJECT_ROOT, 'apps', 'cpm2013', 'docs')

    @classmethod
    def translation(cls, lang):
        return os.path.join(cls.PATH, getattr(cls, lang.upper(), cls.EN))

    def __call__(self, request):
        rules = io.open(
            self.translation(translation.get_language()),
            'r', encoding='utf-8'
        ).read()
        return render_to_response(
            'cpm2013/rules.html',
            {'rules': rules},
            context_instance=RequestContext(request),
        )

from django_xhtml2pdf.utils import generate_pdf

def test(request):
    template_name = 'cpm2013/pdf/submission.html'
    context = {}

    resp = HttpResponse(content_type='application/pdf')

    from django.template.loader import get_template
    from django.template.context import Context

    tmpl = get_template(template_name)
    html = tmpl.render(Context(context))

    from xhtml2pdf import pisa
    pisa.pisaDocument(html.encode("utf-8"), resp , encoding='utf-8')
    
    return resp

