from contexts.base_context import BaseContext


class InventoryFilterContext(BaseContext):
    def __init__(self, req):
        super().__init__(req)

        content = req.get_json()

        self.trait = content.get("trait", "").lower()
        self.show = content.get("show", "").lower()
