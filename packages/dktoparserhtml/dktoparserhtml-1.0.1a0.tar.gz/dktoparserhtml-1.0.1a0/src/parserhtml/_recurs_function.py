def recurs_function(self, function, data=None, recurs=False, **kwargs):
    """
    Effectue une récursivité sur les données en utilisant la fonction spécifiée.

    :param function: La fonction à appliquer récursivement.
    :type function: callable
    :param data: Les données à traiter de manière récursive.
    :type data: str|int|float|list|tuple|dict|None
    :param recurs: Indique si la fonction est appelée récursivement. Ne pas spécifier directement lors de l'appel externe.
    :type recurs: bool
    :param kwargs: Arguments supplémentaires à transmettre à la fonction récursive.
    :returns: Les données traitées de manière récursive.
    :rtype: str|int|float|list|tuple|dict|None
    """

    if data is None and not recurs:
        data = self.data
    #endIf

    if isinstance(data, list) or isinstance(data, tuple):

        l = [
            self.recurs_function(
                function,
                data=e, recurs=True, **kwargs)
            for e in data
        ]

        if l:
            return l
        else:
            return None if self.convertEmptyNone else ""
        #endIf

    elif isinstance(data, dict):

        if self.convert_keys:
            return {
                self.recurs_function(function, data=k, recurs=True, **kwargs)
                :
                self.recurs_function(function,data=v, recurs=True, **kwargs)
                for k, v in data.items()
            }
        else:
            return {
                k
                :
                self.recurs_function(function,data=v, recurs=True, **kwargs)
                if not k in self.skip_values else v
            for k, v in data.items()
            }
        #endIf

    elif isinstance(data, int) or isinstance(data, float):

        data = str(data)

    elif data is None:

        return None if self.convertEmptyNone else ""

    elif not isinstance(data, str) or not data:

        return None if self.convertEmptyNone else ""

    #endIf

    return function(data=data, **kwargs)

#endFunction
