from dataclasses import dataclass
from database.operations import select, select_dict, call_procedure


@dataclass
class InfoResponse:
    result: list
    id_rep: int = 0
    code_error: int = 0
    is_create: bool = False
    error_message: str = None


def model_route(db_config: dict, sql_provider, request) -> InfoResponse:
    report_list = [
        {'rep_id': '1', 'proc_name': 'schema_1.SaleReport', 'sql': 'sales_report.sql'},
        {'rep_id': '2', 'proc_name': 'schema_1.OrderReport', 'sql': 'workers_report.sql'}
    ]
    if not request.form.get('report_choice') or not request.form.get('month_choice'):
        return InfoResponse(result=[], id_rep=2, error_message="Все поля должны быть заполнены")

    context = {}
    for report in report_list:
        if request.form['report_choice'] == report['rep_id']:
            context = report
            break
    context['month'] = request.form['month_choice']
    context['year'] = request.form['year_choice']
    context['action'] = request.form['action']

    id_rep = 1 if context["rep_id"] == '2' else 0
    if context['action'] == 'create':
        return_code = call_procedure(db_config, context['proc_name'], id_rep,
                                     int(context['month']), int(context['year']))

        if return_code == 1:
            error_message = 'Данные за указаный период отсутствуют'
        elif return_code == 2:
            error_message = 'Данные за указаный период уже добавлены в отчётность'
        else:
            error_message = 'Данные успешно занесены в отчёт'
        return InfoResponse(result=[], id_rep=id_rep, error_message=error_message, is_create=True)
    else:
        _sql = sql_provider.get(context["sql"], {"rep_month": context["month"], "rep_year": context["year"]})
        result, schema = select(db_config, _sql)
        if result or schema:
            if result:
                return InfoResponse(result=result, id_rep=id_rep)
            error_message = "Отчёт за данный период отсутствует"
            return InfoResponse(result=result, id_rep=id_rep, error_message=error_message)
        error_message = "Нет подключения к базе данных"
        return InfoResponse(result=result, id_rep=id_rep, error_message=error_message)
