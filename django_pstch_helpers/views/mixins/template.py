"""
#TODO: Fix module docstring
"""
#from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.db import models
from django.conf import settings
from django.core.urlresolvers import resolve
from django.core.exceptions import ImproperlyConfigured

from django.views.generic.base \
    import TemplateResponseMixin as DjangoTemplateResponseMixin



class TemplateResponseMixin(DjangoTemplateResponseMixin):
    #TODO: Fix comments & doc
    """
    A mixin that can be used to render a template.
    """
    app_name = None
    app_prefix = None
    template_add_app_prefix = False


    def get_app_name(self):
        """
        #TODO: Fix comments & doc
        """
        if not self.app_name:
            self.app_name = resolve(self.request.path).app_name
            if not self.app_name:
                raise Exception("Could not get application name.")
        return self.app_name

    def get_app_prefix(self):
        """
        #TODO: Fix comments & doc
        """
        if not self.app_prefix:
            self.app_prefix = getattr(getattr(settings,
                                              "PER_APP_TEMPLATE_PREFIX",
                                              {}),
                                      self.get_app_name(),
                                      self.get_app_name())
        return self.app_prefix

    def prefix_name_if_needed(self, name):
        """
        #TODO: Fix comments & doc
        """
        if self.template_add_app_prefix:
            return "%s/%s" % (self.get_app_prefix(), name)
        else:
            return name

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                """TemplateResponseMixin requires either a definition of
                'template_name' or an implementation of 'get_template_names()'
                """)
        else:
            name = self.prefix_name_if_needed(self.template_name)
            return [name]

class SingleObjectTemplateResponseMixin(TemplateResponseMixin):
    """
    #TODO: Fix comments & doc
    """
    #TODO: Maybe we could remove those attributes and subclass this
    #with Django's SingleObjectTemplateResponseMixin ?
    #(to see when current structure is working)
    template_name_field = None
    template_name_suffix = '_detail'

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. May not be
        called if render_to_response is overridden. Returns the following list:

        * the value of ``template_name`` on the view (if provided)
        * the contents of the ``template_name_field`` field on the
          object instance that the view is operating upon (if available)
        * ``<app_label>/<object_name><template_name_suffix>.html``
        """
        #TODO: Fix comments & doc
        try:
            names = super(SingleObjectTemplateResponseMixin,
                          self).get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        # If self.template_name_field is set, grab the value of the field
        # of that name from the object; this is the most specific template
        # name, if given.
        if self.object and self.template_name_field:
            name = getattr(self.object, self.template_name_field, None)
            name = self.prefix_name_if_needed(name)
            if name:
                names.insert(0, name)

        # The least-specific option is the default <app>/<model>_detail.html;
        # only use this if the object in question is a model.
        model_name = None
        if isinstance(self.object, models.Model):
            model_name = self.object.get_model_name()
        elif hasattr(self, 'model') and \
             self.model is not None and \
             issubclass(self.model, models.Model):
            model_name = self.model.get_model_name()
        if model_name:
            name = "%s/%s%s.html" % (
                self.get_app_name(),
                model_name,
                self.template_name_suffix)
            name = self.prefix_name_if_needed(name)
            names.append(name)

        return names
