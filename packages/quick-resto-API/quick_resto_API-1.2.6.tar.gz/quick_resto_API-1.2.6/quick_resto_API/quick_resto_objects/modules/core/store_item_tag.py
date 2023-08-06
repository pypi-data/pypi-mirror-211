from quick_resto_API.quick_resto_objects.quick_resto_object import QuickRestoObject


class StoreItemTag(QuickRestoObject):
    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str = None, **kwargs):
        class_name = "ru.edgex.quickresto.modules.core.dictionaries.storeitemtag.StoreItemTag"

        super().__init__(class_name=class_name, **kwargs)

        self._name = name
