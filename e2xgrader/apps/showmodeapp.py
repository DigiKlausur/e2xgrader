from .baseapp import E2xGrader


class ShowModeApp(E2xGrader):
    description = "Show the currently active mode"

    def start(self) -> None:
        super().start()
        print(f"Current mode: {self.mode}")
