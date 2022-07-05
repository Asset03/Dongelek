from car.models import *

menu = [
    {'title': "About site", 'url_name': 'about'},
    {'title': "Feedback", 'url_name': 'contact'},
    {'title': "Login", 'url_name': 'login'},
    {'title': "Register", 'url_name': 'register'},
]
class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all()
        context['menu'] = menu
        context['categories'] = categories
        if 'categories_selected' not in context:
            context['categories_selected'] = 0
        return context