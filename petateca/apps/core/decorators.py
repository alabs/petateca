from django.shortcuts import render_to_response
from django.template import RequestContext


try:
    from functools import wraps
except ImportError: 
    def wraps(wrapped, assigned=('__module__', '__name__', '__doc__'),
              updated=('__dict__',)):
        def inner(wrapper):
            for attr in assigned:
                setattr(wrapper, attr, getattr(wrapped, attr))
            for attr in updated:
                getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
            return wrapper
        return inner


def render_to(template=None, mimetype=None):
    """
    Decorator for Django views that sends returned dict to render_to_response 
    function.

    Template name can be decorator parameter or TEMPLATE item in returned 
    dictionary.  RequestContext always added as context instance.
    If view doesn't return dict then decorator simply returns output.

    Parameters:
     - template: template name to use
     - mimetype: content type to send in response headers

    Examples:
    # 1. Template name in decorator parameters

    @render_to('template.html')
    def foo(request):
        bar = Bar.object.all()  
        return {'bar': bar}

    # equals to 
    def foo(request):
        bar = Bar.object.all()  
        return render_to_response('template.html', 
                                  {'bar': bar}, 
                                  context_instance=RequestContext(request))


    # 2. Template name as TEMPLATE item value in return dictionary.
         if TEMPLATE is given then its value will have higher priority 
         than render_to argument.

    @render_to()
    def foo(request, category):
        template_name = '%s.html' % category
        return {'bar': bar, 'TEMPLATE': template_name}
    
    #equals to
    def foo(request, category):
        template_name = '%s.html' % category
        return render_to_response(template_name, 
                                  {'bar': bar}, 
                                  context_instance=RequestContext(request))

    """
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            return render_to_response(tmpl, output, \
                        context_instance=RequestContext(request), mimetype=mimetype)
        return wrapper
    return renderer

