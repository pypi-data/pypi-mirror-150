

class DataRecover(object):
    """
    Recuperacion de instancias en foreignkey en casos de reseteo de base de datos.
    Parametros:
    recover_cls --> Clase modelo base.
    populate_cls --> Clase foreignkey.
    recover_field --> Campo foreignkey.
    populate_field --> Campo de referencia en clase foreignkey.
    populate_ref_field --> Campo de referencia en modelo base.
    """

    def recover(self, recover_cls, populate_cls, recover_field, populate_field, populate_ref_field):
        qs = recover_cls.objects.all()
        for item in qs:
            key = {populate_field: getattr(item, populate_ref_field)}
            p_object = populate_cls.objects.get(**key)
            exec(f"item.{recover_field} = p_object")
            item.save()
