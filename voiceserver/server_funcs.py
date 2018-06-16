from voiceserver.api_for_vk import GetVkApi
import re
import json


class ServerFunctions(object):
    def __init__(self, query):
        self.query = query
        self.keywords = re.compile(
            'Состав|СОСТАВ|'
            'Ингредиенты|ИНГРЕДИЕНТЫ|'
            'Приготовление|ПРИГОТОВЛЕНИЕ|'
            'Сложность|СЛОЖНОСТЬ|'
            'Время|ВРЕМЯ|'
            'Порций|ПОРЦИЙ'
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
            first_word = recipe.split()[0]
            find_ = re.findall('[\d]+|Топ|ТОП|топ', first_word)
            if len(find_) == 0:
                split_for_keywords = re.split(self.keywords, recipe)
                if len(split_for_keywords) == 6:
                    checked_list.append(split_for_keywords)
        return checked_list

    @staticmethod
    def _no_dupl(list_):
        cook_list = []
        no_dupl = []
        for recipe in list_:
            cook_list.append(recipe['cook'])
        for cook in cook_list:
            if cook not in no_dupl:
                index = cook_list.index(cook)
                no_dupl.append(list_[index])
        return no_dupl

    def _get_recipe_title(self, recipes_list):
        reg = re.compile('^[А-ЯЁЙ].[а-яё,\-\s\d]+')
        recipes_title = []
        for recipe in recipes_list:
            recipe_title = re.findall(reg, recipe[0])
            if len(recipe_title) == 0:
                recipe_title = (re.split(self.keywords, recipe[0]))
            if len(recipe_title) != 0:
                recipes_title.append(' '.join(recipe_title[0].split()))
            else:
                recipes_title.append('')
        return recipes_title

    # RETURN FUCKING JSON ONLY
    def _parse_to_json(self, title_list, recipes_list):
        recipes_untitle = []
        for recipe in recipes_list:
            recipe_content = re.split(self.keywords, recipe)
            recipes_untitle.append([recipe_content[1], recipe_content[2]])
        recipes_content_dict = {}
        list_len = len(title_list)
        for count in range(0, list_len):
            recipes_content_dict['id ' + str(count)] = {
                'title': title_list[count],
                'ing': recipes_untitle[count][1],
                'hard': recipes_untitle[count][2],
                'time': recipes_untitle[count][3],
                'port': recipes_untitle[count][4],
                'cook': recipes_untitle[count][5],
            }
        recipe_content_json = json.dumps(
            recipes_content_dict,
            ensure_ascii=False,
            indent=3
        )
        return recipe_content_json

    # IT'S USED
    def _parse_to_json_list(self, title_list, recipes_list):
        recipes_untitle = recipes_list
        json_list = []
        list_len = len(title_list)
        for count in range(0, list_len):
            json_list.append(
                {
                    'id': count,
                    'title': self._fix_elem(title_list[count]),
                    'hard': self._clear_json_elem(recipes_untitle[count][1]),
                    'time': self._clear_json_elem(recipes_untitle[count][2]),
                    'porth': self._clear_json_elem(recipes_untitle[count][3]),
                    'ing': self._fix_elem(recipes_untitle[count][4]),
                    'cook': self._fix_elem(recipes_untitle[count][5]),
                }
            )
        return self._no_dupl(json_list)

    @staticmethod
    def _clear_json_elem(elem):
        return re.findall('[\w\d]+', elem)[0]

    @staticmethod
    def _fix_elem(elem):
        return ' '.join(elem.split())

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
        json_recipes = self._parse_to_json_list(title_list, checked_list)
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
