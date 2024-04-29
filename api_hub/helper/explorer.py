import ast
import glob
import os
import logging


def get_route_info(file_content):
    """Parse a Python file content and return information about functions decorated with @function.route."""
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
                              'route_args': [],
                              'auth_level': None,
                              'methods': None}
                for arg in route.args:
                    if isinstance(arg, ast.Constant):
                        route_info['route_args'].append(arg.value)

                # Extract keyword arguments
                for kw in route.keywords:
                    if kw.arg == 'auth_level':
                        if isinstance(kw.value, ast.Attribute):
                            route_info['auth_level'] = kw.value.attr
                    elif kw.arg == 'methods':
                        if isinstance(kw.value, ast.List):
                            route_info['methods'] = [elem.value for elem in kw.value.elts if isinstance(elem, ast.Constant)]

                # Get all return values in the function
                return_values = []
                for stmt in node.body:
                    if isinstance(stmt, ast.Return):
                        if isinstance(stmt.value, ast.Constant):
                            return_values.append(stmt.value.value)
                        elif isinstance(stmt.value, ast.Name):
                            return_values.append(stmt.value.id)
                        elif isinstance(stmt.value, ast.Call):
                            # For more complex return statements
                            return_values.append(ast.unparse(stmt.value))

                route_info['returns'] = return_values
                routes.append(route_info)

    return routes


def scan_python_files(apiName):
    """Scan all Python files matching a given pattern for @function.route decorated functions."""
    pattern = 'uploads/' + apiName + '/**/*.py'
    py_files = glob.glob(pattern, recursive=True)

    results = []

    for file_path in py_files:
        logging.info(file_path)
        with open(file_path, 'r') as f:
            file_content = f.read()
        route_info = get_route_info(file_content)
        results.extend(route_info)

    return results

