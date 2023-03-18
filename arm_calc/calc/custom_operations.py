from django.db.models import AutoField


def duplicate_object(orig_object):
    new_object = orig_object
    new_object.id = None
    new_object.pk = None
    new_object.save()
    for field in orig_object._meta.fields:
        if not isinstance(field, AutoField):
            setattr(new_object, field.name, getattr(orig_object, field.name))
    for related in orig_object._meta.related_objects:
        if related.one_to_many:
            for obj in getattr(orig_object, related.get_accessor_name()).all():
                dup_obj = obj
                dup_obj.id = None
                dup_obj.pk = None
                setattr(dup_obj, related.field.name, new_object)
                dup_obj.save()
        elif related.one_to_one:
            obj = getattr(orig_object, related.get_accessor_name())
            dup_obj = obj
            dup_obj.id = None
            dup_obj.pk = None
            setattr(dup_obj, related.field.name, new_object)
            dup_obj.save()
        else:
            raise NotImplementedError('Unexpected related object')

    return new_object