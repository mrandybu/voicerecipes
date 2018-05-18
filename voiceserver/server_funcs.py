from voiceserver.api_for_vk import GetVkApi
import re
import json


class ServerFunctions(object):
    def __init__(self, query, keywords=None):
        self.query = query
        self.keywords = re.compile(
            'Состав:|СОСТАВ:|'
            'Ингредиенты:|ИНГРЕДИЕНТЫ:|'
            'Приготовление:|ПРИГОТОВЛЕНИЕ:'
        )

    @staticmethod
    def _get_recipe_text(recipe_list):
        recipes_list_text = []
        for recipe in recipe_list:
            recipes_list_text.append(recipe['text'])
        return recipes_list_text

    def _check_recipe(self, recipes_list):
        checked_list = []
        for recipe in recipes_list:
            split_for_keywords = re.split(self.keywords, recipe)
            if len(split_for_keywords) == 3:
                checked_list.append(recipe)
        return self._no_dupl(checked_list)

    @staticmethod
    def _no_dupl(list_):
        list_no_dupl = []
        for elem in list_:
            list_line = ' '.join(elem.split())
            list_no_dupl.append(list_line)
        return list(set(list_no_dupl))

    def _get_recipe_title(self, recipes_list):
        reg = re.compile('^[А-ЯЁЙ].[а-яё,\-\s]+')
        recipes_title = []
        for recipe in recipes_list:
            recipe_title = re.findall(reg, recipe)
            if len(recipe_title) == 0:
                recipe_title = (re.split(self.keywords, recipe))
            if len(recipe_title) != 0:
                recipes_title.append(' '.join(recipe_title[0].split()))
            else:
                recipes_title.append('')
        return recipes_title

    def _parse_to_json(self, title_list, recipes_list):
        recipes_untitle = []
        for recipe in recipes_list:
            recipe_content = re.split(self.keywords, recipe)
            recipes_untitle.append([recipe_content[1], recipe_content[2]])
        recipes_content_dict = {}
        list_len = len(title_list)
        for count in range(0, list_len):
            recipes_content_dict[count] = {
                count: {
                    'title': title_list[count],
                    'ing': recipes_untitle[count][0],
                    'cook': recipes_untitle[count][1]
                }
            }
        recipe_content_json = json.dumps(
            recipes_content_dict,
            ensure_ascii=False,
            indent=3
        )
        return recipe_content_json

    def preprocessing_recipe_text(self):
        recipes_list_text = self._get_recipes()
        processed_list = []
        reg = re.compile('[\w,.!:\-\s]+')
        for recipe in recipes_list_text:
            recipe_line = ' '.join(recipe.split('\n'))
            cleaned_text = re.findall(reg, recipe_line)
            processed_list.append(''.join(cleaned_text))
        checked_list = self._check_recipe(processed_list)
        title_list = self._get_recipe_title(checked_list)
        json_recipes = self._parse_to_json(title_list, checked_list)
        return str(json_recipes)

    def _get_recipes(self):
        new_request = GetVkApi(query=self.query, count=10)
        response = new_request.search_recipes()
        recipes_list = []
        for domain in response:
            for recipe in domain:
                recipes_list.append(recipe)
        recipes_list_text = self._get_recipe_text(recipes_list)
        return recipes_list_text
