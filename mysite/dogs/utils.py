from dogs.models import Category
from django.core.cache import cache

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить породу', 'url_name': 'add_dog'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        # Проверяем, есть ли кэш? см. № 22
        if not cats:
            cats = Category.objects.all()
            cache.set('cats', cats, 60)
        context['menu'] = menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
