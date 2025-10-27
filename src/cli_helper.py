import ast
import astor 

def compare_and_confirm(func_info, suggested_docstring):
    """
    Muestra docstring original vs sugerido y pregunta si se acepta.

    Returns:
        bool: True si acepta, False si rechaza
    """
    print(f"\nFunction: {func_info['name']}")
    print("ORIGINAL DOCSTRING:")
    print(func_info['docstring'] or "(None)")
    print("\nSUGGESTED DOCSTRING:")
    print(suggested_docstring)
    
    respuesta = input("\nAccept suggested docstring? (y/n): ")
    return respuesta.lower() == "y"



def update_docstring_in_file(file_path, func_name, new_docstring):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            # reemplaza o agrega docstring
            node.body[0] = ast.Expr(value=ast.Constant(value=new_docstring))

    # convertir AST a código
    new_code = astor.to_source(tree)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_code)
