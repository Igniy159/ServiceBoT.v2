from app.api.routers.router_auth import public_rout
from app.api.routers.router_rule import rule_rout
from app.api.routers.router_alert import alert_rout
from app.api.routers.router_branch import branch_rout
from app.api.routers.router_department import department_rout
from app.api.routers.router_user import user_rout
from app.api.routers.router_ticket import ticket_rout
from app.api.routers.router_role import role_rout

routers = [public_rout,
           rule_rout,
           alert_rout,
           branch_rout,
           department_rout,
           user_rout,
           ticket_rout,
           role_rout]
