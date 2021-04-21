def decide_on_model(model):
    """Small helper function to pipe all DB operations of a myDatabase model to the sysdb DB"""
    return 'sysdb' if model._meta.app_label == 'myDatabase' else None


class SysDbRouter:
    """
    Implements a database router so that:

    * Django related data - DB alias `default` - SQLITE3 DB `default`
    * Legacy "world" database data (everything "non-Django") - DB alias `sysdb` - MySQL DB `world`
    """
    def db_for_read(self, model, **hints):
        return decide_on_model(model)

    def db_for_write(self, model, **hints):
        return decide_on_model(model)

    def allow_relation(self, obj1, obj2, **hints):
        # Allow any relation if both models are part of the myDatabase app
        if obj1._meta.app_label == 'myDatabase' and obj2._meta.app_label == 'myDatabase':
            return True
        # Allow if neither is part of myDatabase app
        elif 'myDatabase' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        # by default return None - "undecided"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # allow migrations on the "default" (django related data) DB
        if db == 'default' and app_label != 'myDatabase':
            return True

        # allow migrations on the legacy database too:
        # this will enable to actually alter the database schema of the legacy DB!
        if db == 'sysdb' and app_label == "myDatabase":
           return True

        return False