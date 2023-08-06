def return_int(result):
    if result is None or len(result) < 1:
        return 0
    try:
        return int(result[0][0])
    except TypeError:
        return result[0][0]
    #endWith
    
    return None
#endDef
