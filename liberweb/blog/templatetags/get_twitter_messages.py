import twitter
from django import template

register = template.Library()


class TwitterLattestMsgNode(template.Node):
    def __init__(self, user, limit, tweets):
        self.tweets = tweets
        self.user = user
        self.limit = int(limit)

    def render(self, context):
        try:
            api = twitter.Api()
            status_obj = api.GetUserTimeline(self.user)
            most_recent_messages = [
                {"text":s.text,
                "time":s.relative_created_at,
                "url": "http://twitter.com/%s/statuses/%s"\
                % (self.user, s.id), } for s in status_obj][:self.limit]
            context[self.tweets] = most_recent_messages

        except:
            context[self.tweets] = {
                "error": "Ack! Looks like Twitter's codes are broken!",
            }
        return ''


@register.tag(name='get_twitter_messages')
def twitter_status(parser, token):
    """
    Call this tag with:
        get_twitter_status as tweet
    """
    bits = token.split_contents()

    if len(bits) != 7:
        raise template.TemplateSyntaxError, "%s takes 7 arguments" % bits[0]
    if bits[1] != "user":
        raise template.TemplateSyntaxError,\
                "First argument for %s should be 'user'" % bits[0]

    if bits[3] != "limit":
        raise template.TemplateSyntaxError,\
                "Second argument for %s should be 'limit'" % bits[0]

    if bits[5] != "as":
        raise template.TemplateSyntaxError,\
                "Third argument for %s should be 'as'" % bits[0]

    return TwitterLattestMsgNode(bits[2], bits[4], bits[6])
