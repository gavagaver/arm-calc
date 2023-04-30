def dropdown_links(request, context=None):
    if not context:
        context = request.context_data
    dropdown_items = [
        {
            'name': 'Изменить',
            'url': context.get('edit_url'),
        },
        {
            'name': 'Дублировать',
            'url': context.get('duplicate_url'),
        },
        {
            'name': 'Удалить',
            'url': context.get('delete_url'),
            'color': '#e74a3b',
        },
    ]
    return {'dropdown_items': dropdown_items}
