# planner/templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='add_tailwind_classes')
def add_tailwind_classes(field):
    return field.as_widget(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-transparent'
    })