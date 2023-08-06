from customtkinter import CTk, CTkFrame, CTkLabel, ThemeManager, get_appearance_mode


NORMAL = "normal"
SUCCESS = "success"
CAUTION = "caution"
CRITICAL = "critical"


class CTkInfoBar(CTkFrame):
    def __init__(self, master=None,
                 corner_radius: int | str | None = None,
                 border_width: int | str | None = 0,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = None,
                 border_color: str | tuple[str, str] | None = None,

                 text: str = "CTkInfoBar",

                 mode: str = "normal",

                 **kwargs):
        super().__init__(master, bg_color=bg_color, border_width=border_width, corner_radius=corner_radius, **kwargs)

        if "CTkInfoBar" in ThemeManager.theme:
            if fg_color is None:
                if mode == NORMAL:
                    self._fg_color = ThemeManager.theme["CTkInfoBar"]["fg_color"]
                elif mode == SUCCESS:
                    self._fg_color = ThemeManager.theme["CTkInfoBar"]["success_color"]
                elif mode == CAUTION:
                    self._fg_color = ThemeManager.theme["CTkInfoBar"]["caution_color"]
                elif mode == CRITICAL:
                    self._fg_color = ThemeManager.theme["CTkInfoBar"]["critical_color"]
            elif border_color is None:
                self._border_color = ThemeManager.theme["CTkInfoBar"]["border_color"]

        self.__label_info = CTkLabel(self, text=text, anchor="w")
        self.__label_info.pack(fill="both", expand="true", padx=8, pady=8)

        self._draw()

    def info(self):
        return self.__label_info

    def configure(self, require_redraw=False, **kwargs):
        if "text" in kwargs:
            self.__label_info.configure(text=kwargs.pop("text"))

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self.__label_info.cget("text")
        else:
            return super().cget(attribute_name)

    def show(self, *args, **kwargs):
        self.pack_configure(side="top", fill="x", ipadx=3, ipady=3, padx=5, pady=5)
        self.pack(*args, **kwargs)


if __name__ == '__main__':
    from customtkinterx import CTkCustom, CTkFluentTheme
    from customtkinter import set_appearance_mode, CTkButton

    CTkFluentTheme()

    root = CTkCustom()
    root.create_sizegrip()

    set_appearance_mode("system")

    CTkInfoBar(root.mainframe, text="hello, i am a infobar", mode=NORMAL).show()
    CTkInfoBar(root.mainframe, text="hello, i am a infobar", mode=SUCCESS).show()
    CTkInfoBar(root.mainframe, text="hello, i am a infobar", mode=CAUTION).show()
    CTkInfoBar(root.mainframe, text="hello, i am a infobar", mode=CRITICAL).show()

    CTkButton(root.mainframe, text="Light", command=lambda: set_appearance_mode("light")).pack(fill="x", padx=5, pady=5)
    CTkButton(root.mainframe, text="Dark", command=lambda: set_appearance_mode("dark")).pack(fill="x", padx=5, pady=5)

    root.mainloop()