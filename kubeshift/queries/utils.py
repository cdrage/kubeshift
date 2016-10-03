"""Query helpers."""
import six.moves.urllib.parse as url_parse


def selectors_to_qs(selectors):
    """Convert list of selector dict to query string.

    :param list selectors: list of dicts representing selectors
    :returns: querystring
    :rtype: str|None
    """
    qs = None
    if not isinstance(selectors, list) or not selectors:
        return qs

    qs_list = []
    for s in selectors:
        key = s.get('key')
        if not key:
            # invalid w/o key
            break
        val = s.get('value')
        # default missing op to equal with the assumption that the
        # intent is exists or equal.
        op = s.get('op', '=')

        # set-based has equivalence to equality-based, therefore leverage
        # the set-based formatting
        if op in ['=', '==', 'in']:
            # in / equality / exists
            if val is None:
                qs_list.append('{}'.format(key))
            else:
                if not isinstance(val, list):
                    val = [val]
                qs_list.append('{} in ({})'.format(key, ','.join(val)))

        elif op in ['!=', 'notin']:
            # not in / non-equality / not exists
            if val is None:
                qs_list.append('!{}'.format(key))
            else:
                if not isinstance(val, list):
                    val = [val]
                qs_list.append('{} notin ({})'.format(key, ','.join(val)))
        else:
            # unknown op
            break
    else:
        # successfully processed each selector; format as proper query string
        qs = '?labelSelector=' + url_parse.quote_plus(','.join(qs_list))

    return qs
