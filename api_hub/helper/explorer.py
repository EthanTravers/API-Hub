import ast
import glob
import os
import logging


def get_route_info(file_content):
    tree = ast.parse(file_content)
    routes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            route = None
            # Check if the function has a route decorator
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and hasattr(decorator.func,
                                                               'attr') and decorator.func.attr == 'route':
                    route = decorator

            if route:
                # Extract route arguments
                route_info = {'function_name': node.name,
                              'route': node.name,
                              'auth_level': None,
                              'methods': None}
                for arg in route.args:
                    if (route.args.index(arg) == 0) and isinstance(arg, ast.Constant):
                        route_info['route'] = arg.value
                    elif (route.args.index(arg) == 3) and isinstance(arg, ast.List):
                        route_info['methods'] = ([a.value for a in arg.elts])
                    elif (route.args.index(arg) == 4) and isinstance(arg, ast.Constant):
                        route_info['auth_level'] = arg.value

                # Extract keyword arguments
                for kw in route.keywords:
                    if kw.arg == 'auth_level':
                        if isinstance(kw.value, ast.Attribute):
                            route_info['auth_level'] = kw.value.attr
                    elif kw.arg == 'methods':
                        if isinstance(kw.value, ast.List):
                            route_info['methods'] = [elem.value for elem in kw.value.elts if isinstance(elem, ast.Constant)]
                    elif kw.arg == 'route':
                        route_info['route'] = kw.value.value

                # Extract all return values
                route_info['returns'] = extract_return_values(node.body)

                routes.append(route_info)

    return routes

def extract_return_values(body):
    return_values = []

    for node in body:
        if isinstance(node, ast.Return):
            if isinstance(node.value, ast.Constant):
                return_values.append(node.value.value)
            elif isinstance(node.value, ast.Name):
                return_values.append(node.value.id)
            elif isinstance(node.value, ast.Call):
                # For more complex return statements
                return_values.append(ast.unparse(node.value))
        elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
            # Recursively check nested bodies
            if isinstance(node, ast.If):
                return_values.extend(extract_return_values(node.body))
                return_values.extend(extract_return_values(node.orelse))
            elif isinstance(node, ast.Try):
                return_values.extend(extract_return_values(node.body))
                for handler in node.handlers:
                    return_values.extend(extract_return_values(handler.body))
                return_values.extend(extract_return_values(node.orelse))
                return_values.extend(extract_return_values(node.finalbody))
            elif isinstance(node, (ast.For, ast.While)):
                return_values.extend(extract_return_values(node.body))
                return_values.extend(extract_return_values(node.orelse))

    return return_values

def scan_python_files(apiName):
    pattern = 'uploads/' + apiName + '/**/*.py'
    py_files = glob.glob(pattern, recursive=True)

    results = []

    for file_path in py_files:
        with open(file_path, 'r') as f:
            file_content = f.read()
        route_info = get_route_info(file_content)
        results.extend(route_info)

    return results

