from functools import singledispatch


__all__ = ["sort_vacancies_by_salary"]


@singledispatch
def sort_vacancies_by_salary(vacancies):
    """
    :param vacancies:
    """
    raise TypeError(f"! Value type > {vacancies.__class__} < is not correct !")


@sort_vacancies_by_salary.register
def _(vacancies: dict):
    """
    :param vacancies:
    :return:
    """
    return {k: sorted(v, key=lambda x: x.salary_min) for k, v in vacancies.items()}


@sort_vacancies_by_salary.register
def _(vacancies: list):
    """
    :param vacancies:
    :return:
    """
    return sorted(vacancies, key=lambda x: x.salary_min)
