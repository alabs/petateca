# http://djangosnippets.org/snippets/2121/
from django import template
import random

register = template.Library()

class AnyNode(template.Node):
    def __init__(self, options, splitter="\n"):
        self.options = options
        self.splitter = splitter
    def render(self, context):
        raw_content = self.options.render(context)
        options = raw_content.split(self.splitter)
        clean_options = []
        for option in options:
            stripped = option.strip()
            if stripped: clean_options.append(stripped)
        if len(clean_options) == 1:
            clean_options = clean_options[0].split("|")
        #print "clean_options:", clean_options
        return random.choice(clean_options)

@register.tag(name="any")
def do_any(parser, token):
    """
    This tag defines an area for which options will be used at random.  Options
    can be defined in either (but not mixed) of two ways.  Options can be
    defined one per line.  Empty lines are ignored.  Alternatively, options can
    be defined on ONE line, seperated by the pipe "|" character.  You may nest
    options within options.  Example usage in a template:
    
    <p>
    {% any %}
    One day
    Once upon a time
    In a galaxy far, far away
    {% endany %}
    a young foolish {% any %}programmer|lawyer|Jedi{% endany %}
    {% any %}
    set out
    began his quest
    ran screaming 
    {% endany %}
    to pay his stupid tax.
    </p>
    
    # Possible outcomes:
    <p>In a galaxy far, far away a young foolish lawyer set out to pay his stupid tax.</p>
    <p>One day a young foolish programmer ran screaming to pay his stupid tax.</p>
    """
    options = parser.parse( ('endany',))
    parser.delete_first_token()
    return AnyNode(options)

class SeedRandomizationNode(template.Node):
    def __init__(self, variable_name):
        self.variable_name = variable_name
        self.seed_var = template.Variable(variable_name)
    def render(self, context):
        if self.variable_name == 'None':
            random.seed()
            return ''
        if re.match(r'\d*$', self.variable_name):
            actual_seed = int(self.variable_name)
            random.seed(actual_seed)
            return ''
        try:
            actual_seed = self.seed_var.resolve(context)
            random.seed(actual_seed)
            return ''
        except template.VariableDoesNotExist:
            return ''
@register.tag(name='seed_randomization')
def do_seed_randomization(parser, token):
    """
    If you wish to reproduce the same random selection, seed the random number
    generator by passing any integer as the first and only parameter.  You may
    optionally pass None to reseed using the system default (system time).:
    
    # seed using the primary key of a model
    {% seed_randomization article.pk %}
    
    # reseed using a random number
    {% seed_randomization None %}
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, variable_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return SeedRandomizationNode(variable_name)
