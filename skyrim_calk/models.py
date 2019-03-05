import sqlite3
from django import forms


class CalculateForm(forms.Form):

    #наполнение списка выборов для формы из бд
    @staticmethod
    def selectors():
        select = (('', '',),)
        conn = sqlite3.connect("Skyrim.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM Positive")
        result = cursor.fetchall()
        conn.close()
        for i in range(len(result)):
            select += ((result[i][0], result[i][0],),)
        conn = sqlite3.connect("Skyrim.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM Negative")
        result = cursor.fetchall()
        conn.close()
        for i in range(len(result)):
            select += ((result[i][0], result[i][0],),)
        return select

    #простой поиск по бд
    @staticmethod
    def connection_to_bd(simplifier):
        conn = sqlite3.connect("Skyrim.sqlite3")
        cursor = conn.cursor()
        # cursor.execute("SELECT * FROM Ingredients WHERE (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4)",
        #  (simplifier[0], simplifier[1]))
        if len(simplifier) == 1:
            cursor.execute("SELECT * FROM Ingredients "
                           "WHERE (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4) ", (simplifier[0],))
        elif len(simplifier) == 2:
            cursor.execute("SELECT * FROM Ingredients "
                           "WHERE (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4) "
                           "AND (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4) ", (simplifier[0],
                                                                                                simplifier[1]))
        elif len(simplifier) == 3:
            cursor.execute("SELECT * FROM Ingredients "
                           "WHERE (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4) "
                           "AND (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4) "
                           "AND (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4) ", (simplifier[0],
                                                                                                simplifier[1],
                                                                                                simplifier[2]))
        elif len(simplifier) == 4:
            cursor.execute("SELECT * FROM Ingredients "
                           "WHERE (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4) "
                           "AND (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4) "
                           "AND (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4) "
                           "AND (?) IN (ATTRIBUTE_1, ATTRIBUTE_2, ATTRIBUTE_3, ATTRIBUTE_4)", (simplifier[0],
                                                                                               simplifier[1],
                                                                                               simplifier[2],
                                                                                               simplifier[3]))
        result = cursor.fetchall()
        conn.close()
        return result

    #простой поиск по бд (ищет от 1 до 4 атрибутов в запросе)
    @staticmethod
    def finder (attribute_1, attribute_2, attribute_3, attribute_4):
        attributes = (attribute_1, attribute_2, attribute_3, attribute_4)
        attributes = tuple(filter(None, attributes))
        # if not attributes: attributes = ('',) //проверка на все пустые поля, убрана так как 1 поле обязательное
        bd_result = CalculateForm.connection_to_bd(attributes)
        return bd_result

    #поиск по бд с последующим поиском (ищет по ключевым атрибутам, потом ищет по дополнительным атрибутам)
    @staticmethod
    def optimizer (attribute_1, attribute_2, attribute_3, attribute_4, bd_data):
        attributes = (attribute_1, attribute_2, attribute_3, attribute_4)
        attributes = tuple(filter(None, attributes))
        bd_result = CalculateForm.connection_to_bd(attributes)

        #получаем набор элементов по условию
        conn = sqlite3.connect("Skyrim.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM {0}".format(bd_data))
        bd_data = cursor.fetchall()
        conn.close()

        #init
        bd_result_optima = []
        bd_result_optima_extend = []

        #определяем основные и вторичные атрибуты, производим поиск по вторичным
        for ingredient in bd_result:
            attributes_optima = ()
            for attribute in ingredient:
                if ((attribute,) in bd_data) and (attribute not in attributes):
                    attributes_optima += (attribute,)
            if len(attributes_optima) == 1:
                bd_result_optima += CalculateForm.connection_to_bd(attributes_optima)
            elif len(attributes_optima) == 2:
                bd_result_optima += CalculateForm.connection_to_bd(attributes_optima)
                bd_result_optima += CalculateForm.connection_to_bd((attributes_optima[0],))
                bd_result_optima += CalculateForm.connection_to_bd((attributes_optima[1],))
            elif len(attributes_optima) == 3:
                bd_result_optima += CalculateForm.connection_to_bd(attributes_optima)
                bd_result_optima += CalculateForm.connection_to_bd((attributes_optima[0],))
                bd_result_optima += CalculateForm.connection_to_bd((attributes_optima[1],))
                bd_result_optima += CalculateForm.connection_to_bd((attributes_optima[2],))
                bd_result_optima += CalculateForm.connection_to_bd(attributes_optima[0:1])
                bd_result_optima += CalculateForm.connection_to_bd(attributes_optima[1:2])
                bd_result_optima += CalculateForm.connection_to_bd(attributes_optima[1:3:2])
            else:
                pass
            bd_result_optima += (('', '', '', '', '', '',),)
        bd_result_optima = bd_result + [('', '', '', '', '', '',),] + bd_result_optima

        #еб*сь разметка конём, убираем повторы в массиве
        for i in bd_result_optima:
            if (i not in bd_result_optima_extend) and (i != ('', '', '', '', '', '',)):
                bd_result_optima_extend.append(i)
            elif i == ('', '', '', '', '', '',):
                bd_result_optima_extend.append(i)
        bd_result_optima = [bd_result_optima_extend[0],]
        for i in range (1, len(bd_result_optima_extend)):
            if (bd_result_optima_extend[i-1] == ('', '', '', '', '', '',)) and (bd_result_optima_extend[i] == ('', '', '', '', '', '',)):
                pass
            else:
                bd_result_optima.append(bd_result_optima_extend[i])

        return bd_result_optima

    CHOICES = selectors
    attrib_1 = forms.ChoiceField(label='', choices=CHOICES, required=True)
    attrib_2 = forms.ChoiceField(label='', choices=CHOICES, required=False)
    attrib_3 = forms.ChoiceField(label='', choices=CHOICES, required=False)
    attrib_4 = forms.ChoiceField(label='', choices=CHOICES, required=False)

    CHOICES = (('0', 'Поиск',), ('1', 'Оптимизация',))
    choice_field = forms.ChoiceField(label='Режим', widget=forms.RadioSelect, choices=CHOICES, initial='0')
    CHOICES2 = (('0', 'Положительные',), ('1', 'Отрицательные',))
    choice_field_last = forms.ChoiceField(label='Ключевой эффект', widget=forms.RadioSelect, choices=CHOICES2,
                                          initial='0')



