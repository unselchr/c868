from django.utils.decorators import classonlymethod

def check_roles(class_view):
    def as_view(cls, **initkwargs):
        view = super(cls, cls).as_view(**initkwargs)
        view.cbv = class_view
        return view
    return type(class_view.__name__, (class_view,), {
        'as_view': classonlymethod(as_view),
    })