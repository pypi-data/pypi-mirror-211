def global_registry(name:str,glob:dict):
    global_registry = if_none_default(string='global_registry',glob=globals(),default={"registry_names":[],"registry_index":[]))
    if name not in global_registry['registry_names']:
        if glob == None:
            return None
        global_registry['registry_names'].append(name)
        global_registry['registry_index'].append(glob)
    length = len(global_registry['registry_names']) 
    change_glob('global_registry',global_registry)
    for i in range(0,length):
        if name == global_registry['registry_index'][i]:
            return i
def get_registry_number(name:str):
    return global_registry(name=name,glob=None)
def update_registry(var:str,val:any,name:str):
    global_registry=get_globes(string='global_registry',glob=globals())
    change_glob(var=var,val=val,glob=get_global_from_registry(name))
    global_registry['registry_index'][get_registry_number(name)] = get_global_from_registry(name)
    change_glob(var='global_registry',val=global_registry)
def get_global_from_registry(name:str):
    return global_registry['registry_index'][global_registry(name=name,glob=None)]
def return_globals() -> dict:
    """
    Returns the global variables.

    Args:
        globs (dict, optional): The dictionary of global variables. Defaults to the current globals.

    Returns:
        dict: The global variables dictionary.
    """
    return globals()
def change_glob(var: str, val: any, glob: dict = return_globals()) -> any:
    """
    Changes the value of a global variable.

    Args:
        var (str): The name of the global variable.
        val (any): The new value.
        glob (dict, optional): The dictionary of global variables. Defaults to the current globals.

    Returns:
        any: The new value of the variable.
    """
    glob[var] = val
    return val
def get_globes(string:str='',glob:dict=return_globals()):
    if string in glob:
        return glob[string]
def if_none_default(string:str, default:any,glob:dict=return_globals()):
    piece = get_globes(string=string,glob=glob)
    if piece is None:
        piece = default
    return change_glob(var=string,val=piece,glob=glob)
