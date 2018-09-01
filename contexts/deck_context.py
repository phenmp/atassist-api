from contexts.base_context import BaseContext

class DeckContext(BaseContext):
    def __init__(self, req):
        super().__init__(req)
        
        content = req.get_json()

        self.deck = content.get("deck", 0)
        self.update = content.get("update", 0)
        self.title = content.get("title", "")
        self.amount = content.get("amount", 0)
        self.sort = content.get("sort", 1)
