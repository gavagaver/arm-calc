def duplicate_object(orig_object, new_object):
    if new_object.engineer_id is None:
        new_object.engineer_id = orig_object.engineer_id

    for related in orig_object._meta.related_objects:
        if related.one_to_many:
            for obj in getattr(orig_object, related.get_accessor_name()).all():
                obj.pk = None
                setattr(obj, related.field.name, new_object)
                obj.save()
        elif related.one_to_one:
            obj = getattr(orig_object, related.get_accessor_name())
            obj.pk = None
            setattr(obj, related.field.name, new_object)
            obj.save()
        else:
            raise NotImplementedError('Unexpected related object')

    new_object.save()