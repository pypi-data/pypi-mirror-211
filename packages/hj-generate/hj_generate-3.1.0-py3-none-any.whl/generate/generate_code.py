"""
生成固定代码类
"""
from jinja2 import Environment, FileSystemLoader
import argparse
import os


# 创建模板环境
def generate_code(data):
    current_file_path = os.path.abspath(__file__)
    current_package_path = os.path.dirname(current_file_path)
    # print(current_package_path)
    env = Environment(loader=FileSystemLoader(current_package_path + os.sep + 'templates'))

    # controller
    controller_template = env.get_template('controller.tpl')

    controller_output = controller_template.render(data)

    co_append = """
from controllers.{{name}}_controller import {{name}}
blueprint_list.append({{name}})
            """
    co_str_temp = env.from_string(co_append)

    # 追加
    with open('./controllers' + os.sep + '__init__.py', 'a') as f:
        f.write(co_str_temp.render(data))

    # 生成文件
    with open('./controllers' + os.sep + data.get("name") + '_controller.py', 'w') as f:
        f.write(controller_output)

    # service
    service_template = env.get_template('service.tpl')

    service_output = service_template.render(data)

    se_append = """
from service.{{name}}_service import {{className}}Service
{{varName}}Service = {{className}}Service()
        """
    se_str_temp = env.from_string(se_append)

    # 追加
    with open('./service' + os.sep + '__init__.py', 'a') as f:
        f.write(se_str_temp.render(data))

    # 生成文件
    with open('./service' + os.sep + data.get("name") + '_service.py', 'w') as f:
        f.write(service_output)

    # sql
    sql_template = env.get_template('sql.tpl')

    sql_output = sql_template.render(data)
    sql_append = """
from sql.{{name}}_sql import {{className}}Sql
{{varName}}Sql = {{className}}Sql()
    """
    sql_str_temp = env.from_string(sql_append)

    # 追加
    with open('./sql' + os.sep + '__init__.py', 'a') as f:
        f.write(sql_str_temp.render(data))

    # 生成文件
    with open('./sql' + os.sep + data.get("name") + '_sql.py', 'w') as f:
        f.write(sql_output)


def underscore_to_camelcase_up(text):
    parts = text.split('_')
    return ''.join(word.capitalize() for word in parts)


def underscore_to_camelcase(text):
    parts = text.split('_')
    return parts[0] + ''.join(word.title() for word in parts[1:])


# 示例


def main():
    # 创建命令行解析器
    parser = argparse.ArgumentParser(description="代码生成")

    # 添加命令行参数和选项
    parser.add_argument("name", help="服务名称")

    # 解析命令行参数和选项
    name = parser.parse_args()
    # 调用相应的命令处理函数
    data = {
        'className': underscore_to_camelcase_up(name.name),
        'name': name.name,
        'varName': underscore_to_camelcase(name.name),
    }
    generate_code(data)


if __name__ == '__main__':
    # main()
    import os

    current_file_path = os.path.abspath(__file__)
    current_package_path = os.path.dirname(current_file_path)
    print(current_package_path)
