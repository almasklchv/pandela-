from django import template

register = template.Library()
@register.inclusion_tag('profiles/tags/profile_info.html')
def load_profile_detail(profile):
    """
    Загрузить статью Подробнее
    :param profile:
    :return:
    """

    return {
        'profile': profile,
    }
@register.simple_tag
def query(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)