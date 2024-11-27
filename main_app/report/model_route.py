from dataclasses import dataclass
from database.operations import select, select_dict, call_proc


@dataclass
class InfoResponse:
    result: list
    code_error: int = 0
    is_create: bool = False
    error_message: str = None


def model_route(sql_provider, context: dict) -> InfoResponse:
    if context['action'] == 'create':
        return_code = call_proc(context['db_config'], context['proc_name'],
                                int(context['month']), int(context['year']))
        print(f"context['proc_name'] = {context['proc_name']}")
        print(return_code)
        if return_code == 1:
            error_message = 'Данные за указаный период отсутствуют'
        elif return_code == 2:
            error_message = 'Данные за указаный период уже добавлены в отчётность'
        else:
            error_message = 'Данные успешно занесены в отчёт'
        return InfoResponse(result=(), error_message=error_message, is_create=True)
    else:
        _sql = sql_provider.get(context["sql"], {"rep_month": context["month"], "rep_year": context["year"]})
        # results = select_dict(db_config=context["db_config"], _sql=_sql)
        result, schema = select(context["db_config"], _sql)
        if result or schema:
            if result:
                return InfoResponse(result=result)
            error_message = "Отчёт за данный период отсутствует"
            return InfoResponse(result=result, error_message=error_message)
        error_message = "Это чушь"
        return InfoResponse(result=result, error_message=error_message)
