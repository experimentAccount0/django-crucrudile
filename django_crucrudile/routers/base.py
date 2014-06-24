from abc import ABCMeta, abstractmethod, abstractproperty


class RoutedEntity(metaclass=ABCMeta):
    url_next_sep = ':'
    namespace = None

    def __str__(self):
        return "{}>{}".format(type(self).__name__, self.name)

    def __init__(self, name=None, label=None, namespace=None):
        self.redirect = None
        self.name = name
        self.label = label
        self.namespace = namespace

    @abstractmethod
    def patterns(self, parents=None, url_part=None,
                 namespace=None, name=None,
                 entity=None, add_redirect=True):
        pass

    def get_redirect_url_name(self, parents=None, strict=None):
        return ''.join(
            [
                ''.join([parent.namespace, parent.url_next_sep])
                for parent in parents + [self]
                if parent.namespace is not None
            ] + [
                self.redirect or self.name
            ]
        )

    @abstractproperty
    def url_part(self):
        pass


class BaseRoute(RoutedEntity):
    pass


class BaseModelRoute(BaseRoute):
    pass


class BaseRouter(RoutedEntity):
    pass


class BaseModelRouter(BaseRouter):
    pass