=====
eq-utils version 0.0.7
=====

'eq-utils' is a Django reusable app to help you make models easier.


Quick start
-----------
1. pip install eq-utils==<version>
2. Add "eq_utils" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        'eq_utils',
    ]

3. Import the module like this:

    from eq_utils.base_model import ModelAddressBase (or whatever you need)
    or
    from eq_utils.base_model import AbstractNameModel (or whatever you need)

And that's all.

Usage:

-----
Modelos
1. Inherit the ModelAddressBase in the model.
2. Inherit the AbstractNameModel in the model.

-----
Admins
1. Inherit the AdminHide in the admin.
2. Inherit the EditOnlyTabularInline in the admin.
3. Inherit the BaseReadOnlyAdmin in the admin.

-----
Filtros
1. Inherit the EqAutofilter in the filter.

-----
Recuperacion de datos
1. Inherit the DataRecover in the class to recover data.
