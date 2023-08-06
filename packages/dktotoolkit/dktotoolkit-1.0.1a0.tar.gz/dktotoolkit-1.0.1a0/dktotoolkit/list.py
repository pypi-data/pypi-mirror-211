def replace_with_mask(arr, mask, replacement, inplace=False):
    """
    Remplace les valeurs dans un tableau selon un masque.

    :param arr: Le tableau d'origine.
    :type arr: list
    :param mask: Le masque indiquant les valeurs a remplacer.
    :type mask: list
    :param replacement: La valeur de remplacement.
    :param inplace: Indique si la modification doit etre effectuee sur place (par defaut: False).
    :type inplace: bool

    :return: Le tableau modifie.
    :rtype: list
    """
    if len(arr) != len(mask):
        raise ValueError("Les tableaux doivent avoir la meme longueur")
    #endIf

    if inplace:
        for i in range(len(arr)):
            if mask[i]:
                arr[i] = replacement
            #endIf
        #endFor
    else:
        new_arr = []
        for i in range(len(arr)):
            if mask[i]:
                new_arr.append(replacement)
            else:
                new_arr.append(arr[i])
        return new_arr
    #endIf
    return None
#endDef
