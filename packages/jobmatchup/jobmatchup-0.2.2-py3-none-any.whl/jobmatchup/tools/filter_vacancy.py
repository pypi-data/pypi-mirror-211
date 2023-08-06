from functools import singledispatch


__all__ = ["filter_vacancies"]


@singledispatch
def filter_vacancies(vacancies, _):
    """
    Фильтрация вакансий.
    :param vacancies: вакансии
    :param filter_words: ключевые слова для фильтрации вакансий
    :return:
    """
    raise TypeError(f"! Value type > {vacancies.__class__} < is not correct !")


@filter_vacancies.register
def _(vacancies: dict, filter_words: list):
    return {
        k: [
            vacancy
            for vacancy in vacancies
            if any([w in vacancy.requirements for w in filter_words])
        ]
        for k, v in vacancies.items()
    }


@filter_vacancies.register
def _(vacancies: list, filter_words: list):
    return [
        vacancy
        for vacancy in vacancies
        if any([w in vacancy.requirements for w in filter_words])
    ]
