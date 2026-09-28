import pygame
from src.Settings import *

class DialogBox:
    def __init__(self, screen: pygame.Surface, font_size: int = 28):
        self.screen = screen
        self.font = pygame.font.Font(None, font_size)
        self.visible = False
        self.dialog = ""
        self.npc_name = None

        self.pages: list[list[str]] = []
        self.current_page = 0

        self.padding = 20
        self.box_height = 120
        self.box_rect = pygame.Rect(
            self.padding,
            screen.get_height() - self.box_height - self.padding,
            screen.get_width() - 2 * self.padding,
            self.box_height,
        )

    def show(self, dialog: str, npc_name: str | None = None):
        self.dialog = dialog
        self.npc_name = npc_name
        self.visible = True
        self.current_page = 0

        max_text_width = self.box_rect.width - 2 * self.padding - 100
        lines = self.wrapText(dialog, max_text_width)
        self.pages = [
                         lines[i:i + MAX_LINES]
                         for i in range(0, len(lines), MAX_LINES)
                     ] or [[]]

    def hide(self):
        self.visible = False

    def wrapText(self, text: str, max_width: int) -> list[str]:
        lines = []
        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            words = paragraph.split(" ")
            current_line = ""

            for word in words:
                test_line = f"{current_line} {word}".strip()
                if self.font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            lines.append(current_line)

        return lines

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
        else:
            self.hide()

    def has_next_page(self) -> bool:
        return self.current_page < len(self.pages) - 1

    def draw(self):
        if not self.visible:
            return

        surface = pygame.Surface(self.box_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), width=2, border_radius=10)
        self.screen.blit(surface, self.box_rect.topleft)

        text_x = self.box_rect.x + self.padding
        text_y = self.box_rect.y + self.padding

        if self.npc_name is not None:
            name_surface = self.font.render(self.npc_name, True, "Light Blue")
            self.screen.blit(name_surface, (text_x, text_y))
            text_y += name_surface.get_height() + 5

        for line in self.pages[self.current_page]:
            line_surface = self.font.render(line, True, "white")
            self.screen.blit(line_surface, (text_x, text_y))
            text_y += line_surface.get_height() + 4

        if self.has_next_page():
            hint_surface = self.font.render("(E) Suite -->", True, "yellow")
            hint_rect = hint_surface.get_rect(
                bottomright=(self.box_rect.right - 10, self.box_rect.bottom - 5)
            )
            self.screen.blit(hint_surface, hint_rect)