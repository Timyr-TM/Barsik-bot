from disnake import Embed, ButtonStyle, MessageInteraction
from disnake.ui import View, button, Button


class ButtonsEmbedScroller(View):
    def __init__(self, pages: list[Embed], page: int = 0) -> None:
        super().__init__()
        self._page: int = page
        self._pages: list[Embed] = pages
        self.update_items()

    @property
    def page(self) -> int:
        return self._page

    @property
    def pages(self) -> list[Embed]:
        return self._pages

    def update_items(self) -> None:
        self.back_button.disabled = self.page <= 0
        self.back_button.style = (
            ButtonStyle.gray if self.page <= 0 else ButtonStyle.blurple
        )
        self.next_button.disabled = self.page >= len(self.pages) - 1
        self.next_button.style = (
            ButtonStyle.gray
            if self.page >= len(self.pages) - 1
            else ButtonStyle.blurple
        )
        self.count_button.label = f"{self.page+1}/{len(self.pages)}"

    @button(emoji="⬅️", style=ButtonStyle.blurple)
    async def back_button(self, btn: Button, inter: MessageInteraction) -> Button:
        self._page -= 1
        self.update_items()
        await inter.response.edit_message(view=self, embed=self.pages[self.page])

    @button(label="...", disabled=True, style=ButtonStyle.gray)
    async def count_button(self, btn: Button, inter: MessageInteraction) -> Button:
        pass

    @button(emoji="➡️", style=ButtonStyle.blurple)
    async def next_button(self, btn: Button, inter: MessageInteraction) -> Button:
        self._page += 1
        self.update_items()
        await inter.response.edit_message(view=self, embed=self.pages[self.page])

    async def on_timeout(self) -> None:
        for item in self.children:
            if isinstance(item, Button):
                item.disabled = True
                item.style = ButtonStyle.gray
