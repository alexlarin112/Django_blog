from blog.models import *
from captcha.fields import CaptchaTextInput

header_menu = [
        {'title': "Добавить рецепт", 'url_name': 'add_page'},
]

footer_menu = [
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]

class DataMixin:
    paginate_by = 5

    def get_user_data(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context["cats"] = cats
        context["header_menu"] = header_menu
        context["footer_menu"] = footer_menu
        if "cat_selected" not in context:
            context["cat_selected"] = 0

        return context


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'blog/custom_captcha.html'
