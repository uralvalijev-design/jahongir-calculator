
import math
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp

Window.clearcolor = (0.035, 0.05, 0.11, 1)

BG = (0.035, 0.05, 0.11, 1)
BLUE = (0.08, 0.30, 0.75, 1)
BTN = (0.10, 0.14, 0.25, 1)
WHITE = (0.95, 0.97, 1, 1)

class JahongirCalculator(App):

    def build(self):
        self.expression = ""
        self.history = []
        self.dark = True

        self.sm = ScreenManager()

        for name in ["home", "calc", "science",
                     "history", "settings"]:
            self.sm.add_widget(Screen(name=name))

        self.make_home()
        self.make_calc()
        self.make_science()
        self.make_history()
        self.make_settings()

        root = BoxLayout(orientation="vertical")
        root.add_widget(self.sm)

        nav = GridLayout(
            cols=5,
            size_hint_y=None,
            height=dp(58),
            spacing=3
        )

        pages = [
            ("🏠", "home"),
            ("🧮", "calc"),
            ("🔬", "science"),
            ("📜", "history"),
            ("⚙️", "settings")
        ]

        for icon, page in pages:
            b = Button(
                text=icon,
                font_size=22,
                background_normal="",
                background_color=BLUE
            )
            b.bind(on_press=lambda x, p=page: self.go(p))
            nav.add_widget(b)

        root.add_widget(nav)
        return root

    def label(self, text, size=22):
        return Label(
            text=text,
            font_size=size,
            color=WHITE
        )

    def button(self, text, callback, color=BTN):
        b = Button(
            text=text,
            font_size=20,
            background_normal="",
            background_color=color,
            color=WHITE
        )
        b.bind(on_press=callback)
        return b

    def go(self, page):
        self.sm.current = page
        if page == "history":
            self.refresh_history()

    def make_home(self):
        screen = self.sm.get_screen("home")
        box = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        box.add_widget(self.label(
            "JAHONGIR\nCALCULATOR", 30
        ))

        box.add_widget(self.label(
            "Aqlli va zamonaviy kalkulyator", 17
        ))

        box.add_widget(self.button(
            "🧮  Kalkulyator",
            lambda x: self.go("calc"), BLUE
        ))

        box.add_widget(self.button(
            "🔬  Ilmiy kalkulyator",
            lambda x: self.go("science")
        ))

        box.add_widget(self.button(
            "📜  Hisoblash tarixi",
            lambda x: self.go("history")
        ))

        box.add_widget(self.button(
            "⚙️  Sozlamalar",
            lambda x: self.go("settings")
        ))

        screen.add_widget(box)

    def make_calc(self):
        screen = self.sm.get_screen("calc")
        box = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8
        )

        box.add_widget(self.label("JAHONGIR CALCULATOR", 22))

        self.display = Label(
            text="0",
            font_size=36,
            color=WHITE,
            halign="right",
            valign="middle",
            size_hint_y=0.23
        )
        box.add_widget(self.display)

        grid = GridLayout(cols=4, spacing=6)

        keys = [
            "C", "⌫", "%", "/",
            "7", "8", "9", "*",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "00", "0", ".", "="
        ]

        for key in keys:
            color = BLUE if key in "+-*/=%" else BTN
            if key == "C":
                color = (0.7, 0.12, 0.18, 1)

            grid.add_widget(self.button(
                key,
                lambda x, k=key: self.press(k),
                color
            ))

        box.add_widget(grid)
        screen.add_widget(box)

    def make_science(self):
        screen = self.sm.get_screen("science")
        box = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8
        )

        box.add_widget(self.label("ILMIY KALKULYATOR", 22))

        self.sc_display = Label(
            text="0",
            font_size=32,
            color=WHITE,
            halign="right",
            size_hint_y=0.22
        )
        box.add_widget(self.sc_display)

        grid = GridLayout(cols=4, spacing=6)

        keys = [
            "sin(", "cos(", "tan(", "sqrt(",
            "log(", "log10(", "pi", "e",
            "(", ")", "^", "/",
            "7", "8", "9", "*",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "C", "0", ".", "="
        ]

        for key in keys:
            grid.add_widget(self.button(
                key,
                lambda x, k=key: self.press(k),
                BLUE if key in ["=", "+", "-", "*", "/", "^"] else BTN
            ))

        box.add_widget(grid)
        screen.add_widget(box)

    def press(self, key):
        if key == "C":
            self.expression = ""

        elif key == "⌫":
            self.expression = self.expression[:-1]

        elif key == "=":
            try:
                expr = self.expression.replace("^", "**")

                allowed = {
                    "sin": lambda x: math.sin(math.radians(x)),
                    "cos": lambda x: math.cos(math.radians(x)),
                    "tan": lambda x: math.tan(math.radians(x)),
                    "sqrt": math.sqrt,
                    "log": math.log,
                    "log10": math.log10,
                    "pi": math.pi,
                    "e": math.e
                }

                result = eval(
                    expr,
                    {"__builtins__": {}},
                    allowed
                )

                old = self.expression
                self.expression = str(result)

                self.history.append(
                    old + " = " + self.expression
                )

            except Exception:
                self.expression = "Xato"

        elif key == "%":
            try:
                value = eval(
                    self.expression,
                    {"__builtins__": {}},
                    {"pi": math.pi, "e": math.e}
                )
                self.expression = str(value / 100)
            except Exception:
                self.expression = "Xato"

        else:
            if self.expression == "Xato":
                self.expression = ""
            self.expression += key

        self.update_display()

    def update_display(self):
        value = self.expression or "0"
        self.display.text = value
        self.sc_display.text = value

    def make_history(self):
        screen = self.sm.get_screen("history")
        box = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        box.add_widget(self.label("HISOBLASH TARIXI", 23))

        self.history_label = Label(
            text="Hozircha tarix bo'sh",
            color=WHITE,
            font_size=17,
            halign="left",
            valign="top"
        )

        box.add_widget(self.history_label)

        box.add_widget(self.button(
            "🗑 Tarixni tozalash",
            self.clear_history,
            (0.7, 0.12, 0.18, 1)
        ))

        screen.add_widget(box)

    def refresh_history(self):
        if self.history:
            self.history_label.text = "\n".join(
                reversed(self.history[-30:])
            )
        else:
            self.history_label.text = "Hozircha tarix bo'sh"

    def clear_history(self, instance):
        self.history.clear()
        self.refresh_history()

    def make_settings(self):
        screen = self.sm.get_screen("settings")
        box = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        box.add_widget(self.label("SOZLAMALAR", 25))

        box.add_widget(self.label(
            "JAHONGIR CALCULATOR\nVersion 2.0", 20
        ))

        box.add_widget(self.button(
            "🌙 / ☀️ Rangni almashtirish",
            self.change_theme
        ))

        box.add_widget(self.label(
            "Yaratuvchi: Jahongir", 17
        ))

        screen.add_widget(box)

    def change_theme(self, instance):
        self.dark = not self.dark

        if self.dark:
            Window.clearcolor = BG
        else:
            Window.clearcolor = (0.85, 0.90, 1, 1)

        instance.text = (
            "🌙 Tungi rejim" if not self.dark
            else "☀️ Kunduzgi rejim"
        )

JahongirCalculator().run()
