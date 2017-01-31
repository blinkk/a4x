from google.appengine.ext import ndb


class Model(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

    def delete(self):
        self.key.delete()

    @classmethod
    def get(cls, ident):
        key = ndb.Key(urlsafe=ident)
        return key.get()

    @property
    def ident(self):
        return self.key.urlsafe()

    def __getattr__(self, name):
        # Allow dynamic lookups of references. For example, an entity with
        # a property `category_key` will return the corresponding category
        # when accessing `entity.category`.
        reference_key_name = '{}_key'.format(name)
        if hasattr(self, reference_key_name) and not name in self.__dict__:
            key = getattr(self, reference_key_name)
            return key.get() if key is not None else None
        return self.__getattribute__(name)
