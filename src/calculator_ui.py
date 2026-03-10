import tkinter as tk
from calculator import calculate


class CalculatorUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)

        self._first: float | None = None
        self._op: str | None = None
        self._reset_next = False

        self._build_ui()

    def _build_ui(self):
        self._display_var = tk.StringVar(value="0")
        display = tk.Entry(
            self.root,
            textvariable=self._display_var,
            font=("Helvetica", 24),
            justify="right",
            state="readonly",
            readonlybackground="white",
            bd=10,
            relief="flat",
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=(10, 5))

        btn_cfg = dict(font=("Helvetica", 18), width=4, height=2, relief="flat", cursor="hand2")

        buttons = [
            ("C",  1, 0, "#e74c3c", "white"),
            ("±",  1, 1, "#bdc3c7", "black"),
            ("%",  1, 2, "#bdc3c7", "black"),
            ("/",  1, 3, "#f39c12", "white"),
            ("7",  2, 0, "#ecf0f1", "black"),
            ("8",  2, 1, "#ecf0f1", "black"),
            ("9",  2, 2, "#ecf0f1", "black"),
            ("*",  2, 3, "#f39c12", "white"),
            ("4",  3, 0, "#ecf0f1", "black"),
            ("5",  3, 1, "#ecf0f1", "black"),
            ("6",  3, 2, "#ecf0f1", "black"),
            ("-",  3, 3, "#f39c12", "white"),
            ("1",  4, 0, "#ecf0f1", "black"),
            ("2",  4, 1, "#ecf0f1", "black"),
            ("3",  4, 2, "#ecf0f1", "black"),
            ("+",  4, 3, "#f39c12", "white"),
            ("0",  5, 0, "#ecf0f1", "black"),
            (".",  5, 2, "#ecf0f1", "black"),
            ("=",  5, 3, "#2ecc71", "white"),
        ]

        for (label, row, col, bg, fg) in buttons:
            colspan = 2 if label == "0" else 1
            btn = tk.Button(
                self.root,
                text=label,
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                command=lambda l=label: self._on_button(l),
                **btn_cfg,
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)

        for i in range(6):
            self.root.rowconfigure(i, weight=1)
        for i in range(4):
            self.root.columnconfigure(i, weight=1)

    def _current(self) -> str:
        return self._display_var.get()

    def _set(self, value: str):
        self._display_var.set(value)

    def _on_button(self, label: str):
        if label == "C":
            self._first = None
            self._op = None
            self._reset_next = False
            self._set("0")

        elif label in ("+", "-", "*", "/"):
            try:
                self._first = float(self._current())
            except ValueError:
                return
            self._op = label
            self._reset_next = True

        elif label == "=":
            if self._first is None or self._op is None:
                return
            try:
                b = float(self._current())
                result = calculate(self._first, self._op, b)
                # Strip unnecessary decimals
                display = str(int(result)) if result == int(result) else str(result)
                self._set(display)
            except ZeroDivisionError:
                self._set("Can't divide by zero!")
            except ValueError:
                self._set("Error")
            self._first = None
            self._op = None
            self._reset_next = True

        elif label == "±":
            try:
                val = float(self._current()) * -1
                self._set(str(int(val)) if val == int(val) else str(val))
            except ValueError:
                pass

        elif label == "%":
            try:
                val = float(self._current()) / 100
                self._set(str(val))
            except ValueError:
                pass

        elif label == ".":
            current = self._current()
            if self._reset_next:
                self._set("0.")
                self._reset_next = False
            elif "." not in current:
                self._set(current + ".")

        else:  # digit
            if self._reset_next or self._current() == "0":
                self._set(label)
                self._reset_next = False
            else:
                self._set(self._current() + label)


def main():
    root = tk.Tk()
    CalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
