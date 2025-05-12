from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})

@register.filter(name='first_words')
def first_words(value, num=3):
    return ' '.join(value.split()[:num])
@register.filter(name='five_words')
def five_words(value):
    return ' '.join(value.split()[:8])