from django import template
from lib.order_links_by_vote import order_links_by_vote

register = template.Library()

def episode_links(episode):
    linklist = order_links_by_vote(episode)
    return linklist

register.filter('links_voting', episode_links)
