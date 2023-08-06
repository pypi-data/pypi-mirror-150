def cleanNullTerms(d):
    """
    Removes dictionary elements that contain
    null as their values
    """
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean


def Span(content, class_name=None):
    """

    :param content: span element's content
    :param class_name: class name of span element
    :return: span element and type as dictionary
    """
    return {
        "_type": "Span",
        "props": cleanNullTerms({
            "className": class_name,
            "content": content,
        })
    }


def Container(children, class_name=None):
    """

    :param children: child elements of container
    :param class_name: class name of container element
    :return: container element and type as dictionary
    """
    return {
        "_type": "Container",
        "props": cleanNullTerms({
            "className": class_name,
            "children": children
        })
    }


def Row(children, class_name=None):
    """

    :param children: child elements of row
    :param class_name: class name of row element
    :return: row element and type as dictionary
    """
    return {
        "_type": "Row",
        "props": cleanNullTerms({
            "className": class_name,
            "children": children
        })
    }


def Div(children, class_name=None, style=None):
    return {
        "_type": "Div",
        "props": cleanNullTerms({
            "className": class_name,
            "children": children,
            "style": style,
        })
    }


def Col(children, class_name=None):
    """

    :param children: child elements of column
    :param class_name: class name of column element
    :return: column element and type as dictionary
    """
    return {
        "_type": "Col",
        "props": cleanNullTerms({
            "className": class_name,
            "children": children
        })
    }


def Icon(name, class_name=None, size=None):
    """

    :param name: icon name
    :param class_name: class name of icon element
    :param size: icon size
    :return: icon element and type as dictionary
    """
    return {
        "_type": "Icon",
        "props": cleanNullTerms({
            "className": class_name,
            "name": name,
            "size": size
        })
    }


def Datatable(data, columns, class_name=None, busy_when=None, show_export=None):
    """

    :param data: content of datatable
    :param columns: columns list of datatable
    :param class_name: class attribute of datatable
    :param busy_when: busy attribute of datatable
    :param show_export: boolean
    :return: datatable
    """
    return {
        "_type": "Datatable",
        "props": cleanNullTerms({
            "busyWhen": busy_when,
            "className": class_name,
            "columns": columns,
            "data": data,
            "showExport": show_export
        })
    }


def Badge(color, children, class_name=None):
    """

    :param color: badge color
    :param children: child elements of badge
    :param class_name: classname element of badge
    :return: badge element with type as dict
    """
    return {
        "_type": "Badge",
        "props": cleanNullTerms({
            "children": children,
            "className": class_name,
            "color": color,
        })
    }


def Column(id, value=None, title=None, format=None, right=None, width=None, min_width=None, grow=None, cell=None):
    return cleanNullTerms({
        "cell": cell,
        "format": format,
        "grow": grow,
        "id": id,
        "minWidth": min_width,
        "right": right,
        "title": title,
        "value": value,
        "width": width,
    })


def Form(name, schema, children, class_name=None):
    """

    :param name: form name
    :param schema: form schema
    :param children: child elements of form
    :param class_name: form class
    :return: form element with type as dict
    """
    return {
        "_type": "Form",
        "props": cleanNullTerms({
            "children": children,
            "className": class_name,
            "name": name,
            "schema": schema,
        })
    }


def Select(label, name, options, min_width=None, class_name=None):
    """

    :param label: selector label
    :param name: selector name
    :param options: selector options
    :param min_width: minimum width of selector
    :param class_name: selector class name
    :return: selector element with type as dict
    """
    return {
        "_type": "Select",
        "props": cleanNullTerms({
            "className": class_name,
            "label": label,
            "name": name,
            "options": options,
            "minWidth": min_width,
        })
    }


def Button(label, is_submit=None, class_name=None, busyWhen=None):
    """

    :param label: button label
    :param is_submit: boolean that describes if button is submit or not
    :param class_name: button class name
    :param busyWhen: button busy parameter
    :return: button element with type as dict
    """
    return {
        "_type": "Button",
        "props": cleanNullTerms({
            "className": class_name,
            "label": label,
            "isSubmit": is_submit,
            "busyWhen": busyWhen,
        })
    }


def collection(collectionName):
    """
    Returns collection name
    """
    return collectionName


def documents(collectionName):
    """
    Returns document of particular collection
    """
    return f'$["{collection(collectionName)}"].*'


def is_busy(collection):
    """
    Returns business of collection
    """
    return f'$..busy[?(@.id=="{collection}")]'


def format_currency(rpc, symbol):
    """
    Returns dictionary with currency format
    """
    return {
        "method": "formatCurrency",
        "params": [rpc, symbol]
    }

def form_value(event, form_name, property_name):
    """
    Returns form value by form name, if specified, otherwise None
    """
    if (event is None):
        return None

    if ("state" not in event.keys()):
        return None

    if ("forms" not in event["state"].keys()):
        return None

    if (form_name not in event["state"]["forms"].keys()):
        return None

    if (property_name not in event["state"]["forms"][form_name].keys()):
        return None

    return event["state"]["forms"][form_name][property_name]


def format_template(template, values):
    """
    Return template formatting
    """
    return {
        "method": "formatTemplate",
        "params": [template, values]
    }


def switch_case(on, cases):
    return {
        "method": "switchCase",
        "params": [on, cases]
    }


def commify(value):
    """
    Return commify dictionary
    """
    return {
        "method": "commify",
        "params": [value]
    }
