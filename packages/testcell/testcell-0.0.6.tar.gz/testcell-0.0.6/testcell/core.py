# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_ast.ipynb.

# %% auto 0
__all__ = ['last_node', 'node_source', 'is_assignment', 'extract_call', 'is_import_statement', 'is_ast_node', 'need_return',
           'end_of_last_line_of_code', 'last_statement_has_semicolon', 'code_till_node', 'auto_return']

# %% ../nbs/01_ast.ipynb 4
import ast

# %% ../nbs/01_ast.ipynb 5
def last_node(code):
    tree = ast.parse(code)
    if len(tree.body)==0: return None
    src = tree.body[-1]
    last_node = None
    parent_node = None
    for node in ast.walk(src):
        if isinstance(node, ast.stmt):
            parent_node = last_node
            last_node = node
    if parent_node is not None: return None # deal with nested statements like "for loop".
    return last_node

# %% ../nbs/01_ast.ipynb 7
def node_source(node,code):
    return ast.get_source_segment(code,node)

# %% ../nbs/01_ast.ipynb 13
def is_assignment(node):
    return isinstance(node, ast.Assign)

# %% ../nbs/01_ast.ipynb 15
def extract_call(node):
    if not isinstance(node, ast.Expr): return None
    node = node.value # step in
    if isinstance(node, ast.Name): return None # "fn"
    if isinstance(node, ast.Call):
        n = node.func # step in
        if isinstance(n, ast.Name): return n.id # "fn()"
        if isinstance(n, ast.Attribute): return n.attr
    return None # all the rest is not supported

# %% ../nbs/01_ast.ipynb 17
def is_import_statement(node):
    return isinstance(node, (ast.Import, ast.ImportFrom))

# %% ../nbs/01_ast.ipynb 19
def is_ast_node(x,ref):
    for t in ref:
        if isinstance(x,t): return True
    return False

# %% ../nbs/01_ast.ipynb 22
def need_return(node):
    if node is None: return False
    if is_assignment(node): return False
    if is_ast_node(node,ref=[ast.Delete, ast.Assert, ast.Global, ast.Nonlocal]): return False
    if is_import_statement(node): return False
    return True

# %% ../nbs/01_ast.ipynb 24
def end_of_last_line_of_code(code:str,node):
    if node is None: return ''
    t = code.splitlines()
    t = t[:node.lineno]
    return t[-1][node.end_col_offset:]

# %% ../nbs/01_ast.ipynb 27
def last_statement_has_semicolon(code):
    e = end_of_last_line_of_code(code, last_node(code))
    e = e.strip()
    return e.startswith(';')

# %% ../nbs/01_ast.ipynb 30
def code_till_node(code:str,node):
    if node is None: return code
    t = code.splitlines()
    t = t[:node.lineno]
    t[-1] = t[-1][:node.col_offset]
    if len(t[-1])==0: t = t[:-1]
    return '\n'.join(t)

# %% ../nbs/01_ast.ipynb 33
def auto_return(code):
    if last_statement_has_semicolon(code): return code
    
    n = last_node(code)
    if not need_return(n): return code
    
    ns = node_source(n,code)
    ret = code_till_node(code, last_node(code))
    ret += f'\nreturn {ns} # %%testcell'
    return ret
