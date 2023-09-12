def duplicate_with_related(object, related_object):
    object.pk = None
    setattr(object, related_object.__class__.__name__.lower(), related_object)
    object.save()
