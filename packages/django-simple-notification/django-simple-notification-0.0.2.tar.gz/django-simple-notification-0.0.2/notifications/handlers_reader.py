import ast


def get_handlers():
    with open('apps/notifications/handlers.py', 'r') as f:  # todo make this came from settings
        f = f.read()

    p = ast.parse(f)

    function_names = [node.name for node in ast.walk(p) if isinstance(node, ast.FunctionDef)]

    return function_names
