def sort_datas(keys, list_of_list_values=[], list_values=[], return_list=True):

    if list_of_list_values :
        #if return list:
        return [
            sort_datas(
                keys,
                list_values=e,
                return_list=False
            )
            for e in list_of_list_values
        ]

    elif list_values:

        out = {}

        for i in range(len(keys)):
            if i < len(list_values) :
                out[keys[i]] = list_values[i]
            else:
                out[keys[i]] = None
            #endIf
        #endFor

        if return_list:
            return [out,]
        else:
            return out
        #endIf
    else:
        return [] if return_list else {}
    #endIf

    raise Exception
#endDef
