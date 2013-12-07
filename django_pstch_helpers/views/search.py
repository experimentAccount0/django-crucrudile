from __future__ import unicode_literals

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

from django.shortcuts import render_to_response

from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView, FormView
from django.views.generic.list import MultipleObjectMixin
from .mixins import AuthMixin

from haystack.forms import ModelSearchForm, FacetedSearchForm
from haystack.query import EmptySearchQuerySet


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


class SearchView(AuthMixin, MultipleObjectMixin, FormView):
    template_name = 'search/search.html'

    queryset = EmptySearchQuerySet()
    object_list = queryset
    query = ''
    
    load_all = True
    searchqueryset = None
    form_class = ModelSearchForm

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(SearchView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)

        if len(self.request.GET):
            data = self.request.GET

        context['query'] = self.query

        results = self.queryset
        results_query = getattr(results, 'query', None)
        if results and results_query and results_query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        return context

    def form_invalid(self):
        raise Exception
        
    def get_form_kwargs(self):
        kwargs = super(SearchView, self).get_form_kwargs()
        kwargs.update({'searchqueryset' : self.searchqueryset,
                       'load_all' : self.load_all })
        return kwargs
        
    def form_valid(self, form):
        self.query = form.cleaned_data['q']
        self.queryset = form.search()
        self.object_list = self.queryset
        print "QS: %s" % self.queryset


        context = self.get_context_data()
        return self.render_to_response(context)
        
    def get_queryset(self):
        return self.queryset