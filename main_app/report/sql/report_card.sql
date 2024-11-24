select 
    rc.id_report as id_report, rc.id_employee as id_employee, 
    emp.last_name as last_name, rc.start_work_date as date_work, rc.work_hours as work_hours
from 
    report_cards rc
    join employees emp ON rc.id_employee = emp.id_employee
where rc.start_work_date >= '$_start' and rc.start_work_date < '$_finish';
