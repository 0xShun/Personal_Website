from django import template

register = template.Library()

@register.filter
def filter_by_category(projects, category):
    return [project for project in projects if project.category == category] 