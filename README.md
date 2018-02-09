menutree
=====

Installation
------

The project uses `pipenv` to manage its dependencies. Create a virtual environment by running

```
pipenv install
```

Activate it:

```
pipenv shell
```

Then init the database. `sqlite` is the default.

```
./manage.py migrate
```

If you have `DEBUG = True` in your settings this will also create an admin user with
the credentials `admin/admin`.

Then you can run the server:

```
./manage.py runserver
```

Implementation
------

The logic revolves around the [`MenuItem`](https://github.com/abetkin/menutree/blob/master/menu/models.py#L9) model in `menu` app.
Every menu item can have a parent and should have a unique order
among other child items of that parent (even if parent is `None` i. e. it is the root item).

There is also `GlobalId` model that lets you make an ordered list of all menu items in the database. The corresponding `GlobalId` record is inserted/updated on the `post_save` of `MenuItem`.

On the `admin` site, child menu items can be added using the formset. Their order in the parent menu,
if not provided, will be the order they are defined in.
That is implemented by overriding `FormSet.save`. When provided by user, the order is validated in `Formset.full_clean`