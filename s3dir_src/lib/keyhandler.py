KEY = {
    "up": -204,
    "down": -206,
    "left": -203,
    "right": -205,
    "shiftUp": 337,
    "shiftDown": 336,
    "enter": 10,
    "space": 32,
    "tab": -301,
    "shiftTab": -302,
    "backspace": -300,
    "esc": -1,
    "altC": 231,
    ":": ord(":"),
    "?": ord("?"),
}

KEYLIST = {
    "move": [
        KEY["up"],
        KEY["down"],
        KEY["shiftUp"],
        KEY["shiftDown"],
        KEY["esc"],
        KEY["left"],
        KEY["right"],
        KEY["enter"],
    ],
    "number": range(48, 58),
    "y": [ord("Y"), ord("y")],
    "n": [ord("N"), ord("n")],
}


class KeyHandler:
    @staticmethod
    def check(key_code, CURRENT):
        sect = CURRENT["section"]
        if CURRENT["layer"] == "confirm":
            if key_code == KEY["left"] or key_code in KEYLIST["y"]:
                CURRENT["action"] = "yes"
            elif key_code == KEY["right"] or key_code in KEYLIST["n"]:
                CURRENT["action"] = "no"
            elif key_code == KEY["enter"]:
                CURRENT["action"] = "confirm"
            elif key_code == KEY["esc"]:
                CURRENT["action"] = "cancel"
            return

        if key_code == KEY["esc"]:
            CURRENT["action"] = "esc"
            return

        if key_code in [KEY["down"], KEY["space"]]:
            if key_code == KEY["space"]:
                CURRENT["action"] = "select"
                CURRENT["kwargs"] = {"row": CURRENT["selectedRow"][sect]}

            CURRENT["selectedRow"][sect] += 1

            if CURRENT["selectedRow"][sect] >= CURRENT["rows"][sect]:
                if key_code == KEY["space"]:
                    CURRENT["selectedRow"][sect] -= 1
                else:
                    CURRENT["selectedRow"][sect] = 0
                    CURRENT["scrollTop"][sect] = 0

            elif (
                CURRENT["selectedRow"][sect] >= CURRENT["rowlimit"]
                and CURRENT["selectedRow"][sect]
                >= CURRENT["scrollTop"][sect] + CURRENT["rowlimit"]
            ):
                CURRENT["scrollTop"][sect] += 1

        elif key_code == KEY["up"]:
            CURRENT["selectedRow"][sect] -= 1
            if CURRENT["selectedRow"][sect] < 0:
                CURRENT["selectedRow"][sect] = CURRENT["rows"][sect] - 1
                if CURRENT["rows"][sect] > CURRENT["rowlimit"]:
                    CURRENT["scrollTop"][sect] = (
                        CURRENT["rows"][sect] - CURRENT["rowlimit"]
                    )

            if (
                CURRENT["rows"][sect] > CURRENT["rowlimit"]
                and CURRENT["selectedRow"][sect] < CURRENT["scrollTop"][sect]
            ):
                CURRENT["scrollTop"][sect] = CURRENT["selectedRow"][sect]

        elif key_code == KEY["shiftDown"]:
            CURRENT["selectedRow"][sect] += 10
            if CURRENT["selectedRow"][sect] >= CURRENT["rowlimit"]:
                CURRENT["selectedRow"][sect] = 0

        elif key_code == KEY["shiftUp"]:
            CURRENT["selectedRow"][sect] -= 10
            if CURRENT["selectedRow"][sect] < 0:
                CURRENT["selectedRow"][sect] = CURRENT["rowlimit"] - 1

        if key_code == KEY["enter"]:
            CURRENT["action"] = "enter"
            return

        elif key_code == KEY["?"]:
            CURRENT["action"] = "help"
            return

        elif key_code == KEY["altC"]:
            CURRENT["action"] = "copy"
            return

        elif key_code in [KEY["tab"], KEY["shiftTab"], KEY["left"], KEY["right"]]:
            CURRENT["section"] = "remote" if CURRENT["section"] == "local" else "local"
            CURRENT["action"] = "tab"
            return

        if key_code in KEYLIST["move"]:
            CURRENT["action"] = "move"
            return
