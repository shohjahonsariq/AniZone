from django import template

register = template.Library()

@register.filter
def get_category_name(categories, selected_id):
    for cat in categories:
        if cat.id == selected_id:
            return cat.name
    return '' 