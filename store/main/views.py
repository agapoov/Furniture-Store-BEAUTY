from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BEAUTY - Главная'
        context['content'] = 'Магазин мебели BEAUTY'
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BEAUTY - О нас'
        context['content'] = 'О нас'
        context['text_on_page'] = ('Текст о том, какой прекрасный этот магазин, и какой качественный товар тут '
                                   'продаётся.')
        return context


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
