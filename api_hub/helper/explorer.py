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
                    if isinstance(arg, ast.constants):
                        route_info['route_args'].append(arg.value)

                # Extract keyword arguments
                for kw in route.keywords:
                    if kw.arg == 'auth_level':
                        if isinstance(kw.value, ast.Attribute):
                            route_info['auth_level'] = kw.value.attr
                    elif kw.arg == 'methods':
                        if isinstance(kw.value, ast.List):
                            route_info['methods'] = [elem.value for elem in kw.value.elts if isinstance(elem, ast.Constant)]

                # Extract all return values
                route_info['returns'] = extract_return_values(node.body)

                routes.append(route_info)

    return routes

def extract_return_values(body):
    """Extract return statements from a list of AST nodes."""
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

