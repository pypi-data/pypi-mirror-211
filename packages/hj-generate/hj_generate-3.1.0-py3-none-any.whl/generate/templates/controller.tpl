from flask import Blueprint

from aop import handle_web_result
from aop.handle_web_request import handle_web_request
from returnmessage import ReturnMessage


from service import {{varName}}Service

{{name}} = Blueprint("{{name}}", __name__)




@{{name}}.route("/{{name}}/list", methods=["GET"])
@handle_web_request
@handle_web_result
def {{name}}_list(**kwargs):
    return ReturnMessage(data={{varName}}Service.{{name}}_list(query_data=kwargs.get("params")))