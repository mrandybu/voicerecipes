from voiceserver.api_for_vk import GetVkApi
import re


class ServerFunctions(object):
    def __init__(self, query, keywords=None):
        self.query = query
        self.keywords = re.compile(
            'Состав:|СОСТАВ:|'
            'Ингредиенты:|ИНГРЕДИЕНТЫ:'
        )

    @staticmethod
    def _get_recipe_text(recipe_list):
        recipes_list_text = []
        for recipe in recipe_list:
            recipes_list_text.append(recipe['text'])
        return recipes_list_text

    def _check_recipe(self, recipes_list):
        indexes = []
        checked_list = []
        for recipe in recipes_list:
            keywords_search = re.findall(self.keywords, recipe)
            counter = 0
            for searched_recipe in keywords_search:
                if len(searched_recipe) != 0:
                    counter += 1
            if counter == 1:
                checked_list.append(recipe)
        return self._no_dupl(checked_list)

    @staticmethod
    def _no_dupl(list_):
        list_no_dupl = []
        for elem in list_:
            list_line = ' '. join(elem.split())
            list_no_dupl.append(list_line)
        return list(set(list_no_dupl))

    def _get_recipe_name(self, recipes_list):
        reg = re.compile('^[А-ЯЁЙ].[а-яё,\-\s]+')
        recipes_names = []
        for recipe in recipes_list:
            recipe_name = re.findall(reg, recipe)
            if len(recipe_name) == 0:
                recipe_name = (re.split(self.keywords, recipe))
            if len(recipe_name) != 0:
                recipes_names.append(' '.join(recipe_name[0].split()))
            else:
                recipes_names.append('')
        return recipes_names

    def preprocessing_recipe_text(self):
        recipes_list_text = self._get_recipes()
        processed_list = []
        reg = re.compile('[\w,.!:\-\s]+')
        for recipe in recipes_list_text:
            recipe_line = ' '.join(recipe.split('\n'))
            cleaned_text = re.findall(reg, recipe_line)
            processed_list.append(''.join(cleaned_text))
        checked_list = self._check_recipe(processed_list)
        names_list = self._get_recipe_name(checked_list)
        return str(names_list)

    def _get_recipes(self):
        new_request = GetVkApi(query=self.query, count=10)
        response = new_request.search_recipes()
        recipes_list = []
        for domain in response:
            for recipe in domain:
                recipes_list.append(recipe)
        recipes_list_text = self._get_recipe_text(recipes_list)
        return recipes_list_text
