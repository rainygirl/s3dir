import os
import sys
import signal
import time
from pathlib import Path

from asciimatics.screen import Screen

from .lib.action import action_and_exit
from .lib.data import load_data as _load_data
from .lib.color import COLOR, CARTED_SIGN
from .lib.keyhandler import KeyHandler
from .lib.s3 import S3
from .lib.textmode import TextMode

S = {
    "section": "local",
    "selectedRow": {"local": 0, "remote": 0},
    "scrollTop": {"local": 0, "remote": 0},
    "cartedRows": {"local": [], "remote": []},
    "rows": {"local": 0, "remote": 0},
    "path": {"local": "", "remote": ""},
    "pathStr": {"local": "", "remote": ""},
    "rowlimit": 10,
    "position": {"local": {"x": 2}, "remote": {"x": 12}, "sectionWidth": 10},
    "remoteorigin": "S3",
    "kubectl": {"pod": "", "container": ""},
    "s3bucket": "",
    "layer": "box",
    "confirmaction": "",
    "queue": [],
}

data = {"local": [], "remote": []}

os.environ.setdefault("ESCDELAY", "10")


def load_data(sect):
    data[sect] = _load_data(S, sect)


def layout(screen):
    def init_path_str():
        for section in S["path"].keys():
            if section == "local":
                path_str = S["path"][section]
                path_str = path_str.replace(str(Path.home()), "~")
            else:
                if S["remoteorigin"] == "S3":
                    path_str = "s3://" + S["s3bucket"] + "/" + S["path"][section]
                else:
                    if S["kubectl"]["pod"] == "":
                        path_str = "Choose pod"
                    elif S["kubectl"]["container"] == "":
                        path_str = "Choose container in " + S["kubectl"]["pod"] + " pod"
                    else:
                        path_str = (
                            S["kubectl"]["pod"] + ":" + (S["path"][section] or ".")
                        )

                        if len(path_str) > S["position"]["sectionWidth"] + 2:
                            path_str = (
                                ".." + path_str[-S["position"]["sectionWidth"] + 4 :]
                            )

            S["pathStr"][section] = path_str

    def draw():
        for section, items in data.items():
            S["rows"][section] = len(items)
            x = S["position"][section]["x"]

            pathcolor = "pathStr" if section != S["section"] else "pathStrSelected"
            screen.print_at(
                f" {S['pathStr'][section]} ",
                x,
                0,
                colour=COLOR[pathcolor][0],
                bg=COLOR[pathcolor][1],
            )

            for i, d in enumerate(
                items[S["scrollTop"][section] : S["scrollTop"][section] + S["rowlimit"]]
            ):
                if type(d) == str:
                    text = d
                    item_type = ("normal", "selected")
                    if d == ".." or (section == "remote" and d != "" and d[-1] == "/"):
                        item_type = ("dir", "dirSelected")
                elif section == "remote" and type(d) == dict:
                    text = d["key"]
                    item_type = ("normal", "selected")
                else:
                    text = d.name
                    item_type = ("normal", "selected")
                    if d.is_dir():
                        item_type = ("dir", "dirSelected")

                if section != S["section"]:
                    if item_type[0] == "dir":
                        item_type = ("dirDimmed",)
                    elif item_type[0] == "normal":
                        item_type = ("dimmed",)

                kwargs = {
                    "colour": COLOR[item_type[0]][0],
                    "bg": COLOR[item_type[0]][1],
                }

                y = i + 1

                current_row = i + S["scrollTop"][section]
                if S["section"] == section and current_row == S["selectedRow"][section]:
                    kwargs = {
                        "colour": COLOR[item_type[1]][0],
                        "bg": COLOR[item_type[1]][1],
                    }

                carted = (
                    CARTED_SIGN
                    if (
                        current_row in S["cartedRows"][section]
                        and S["section"] == section
                    )
                    else " "
                )

                screen.print_at(" " * S["position"]["sectionWidth"], x, y, **kwargs)

                right_text = ""
                size = -1
                if (
                    section == "local"
                    and type(data[section][current_row]) != str
                    and not data[section][current_row].is_dir()
                ):
                    try:
                        size = data[section][current_row].stat().st_size
                    except:
                        size = 0
                elif section == "remote" and type(data[section][current_row]) == dict:
                    size = data[section][current_row]["size"]
                if size > -1:
                    right_text = tm.size_humanize(size)

                    if right_text != "":
                        screen.print_at(
                            f"{right_text}",
                            (x + S["position"]["sectionWidth"] - len(right_text) - 2),
                            y,
                            **kwargs,
                        )

                text = text[: S["position"]["sectionWidth"] - len(right_text) - 6]

                screen.print_at(f"{carted} {text}", x, y, **kwargs)

                if carted != " " and current_row != S["selectedRow"][section]:
                    screen.print_at(
                        f"{carted}",
                        x,
                        y,
                        colour=COLOR["carted"][0],
                        bg=COLOR["carted"][1],
                    )

        screen.refresh()

    def draw_confirm_button():
        yescolor = "confirmSelected" if S["confirm"] == "yes" else "confirm"
        nocolor = "confirmSelected" if S["confirm"] == "no" else "confirm"
        screen.print_at(
            " Yes ",
            35,
            screen.height - 1,
            colour=COLOR[yescolor][0],
            bg=COLOR[yescolor][1],
        )
        screen.print_at(
            " No ",
            40,
            screen.height - 1,
            colour=COLOR[nocolor][0],
            bg=COLOR[nocolor][1],
        )

    def confirm(confirm_msg):
        screen.print_at(" " * screen.width, 0, screen.height - 1)
        screen.print_at(confirm_msg, 0, screen.height - 1)
        S["confirm"] = "no"
        S["layer"] = "confirm"
        draw_confirm_button()
        screen.refresh()

    def clear_confirm():
        draw_bottom()
        S["layer"] = "box"
        screen.refresh()

    def draw_bottom():
        screen.print_at(" " * screen.width, 0, screen.height - 1)

        key_args = {
            "y": screen.height - 1,
            "colour": COLOR["lineSelected"][1],
            "bg": COLOR["lineSelected"][0],
        }
        desc_args = {
            "y": screen.height - 1,
            "colour": COLOR["lineSelected"][0],
            "bg": COLOR["lineSelected"][1],
        }

        screen.print_at(" Space ", 1, **key_args)
        screen.print_at(" Select ", 8, **desc_args)
        screen.print_at(" Enter ", 18, **key_args)
        screen.print_at(" Enter ", 25, **desc_args)
        screen.print_at(" Alt+C ", 33, **key_args)
        screen.print_at(" Copy ", 40, **desc_args)
        screen.print_at(" ESC ", 58, **key_args)
        screen.print_at(" Quit ", 63, **desc_args)
        screen.refresh()

    def draw_box(section, is_active=False):
        polygon = {
            "local": [
                (0, 0),
                (int(screen.width / 2) - 1, 0),
                (int(screen.width / 2) - 1, screen.height - 2),
                (0, screen.height - 2),
            ],
            "remote": [
                (int(screen.width / 2), 0),
                (screen.width - 1, 0),
                (screen.width - 1, screen.height - 2),
                (int(screen.width / 2), screen.height - 2),
            ],
        }
        fillcolor = "fill"
        linecolor = "line"

        if is_active:
            fillcolor = "fillSelected"
            linecolor = "lineSelected"

        tm.clear_area(
            polygon[section],
            colour=COLOR[fillcolor][0],
            bg=COLOR[fillcolor][1],
        )
        tm.draw_box(
            polygon[section], colour=COLOR[linecolor][0], bg=COLOR[linecolor][1]
        )

    def do():
        tm.init_screen(S)
        init_path_str()
        screen.clear()
        draw_box("local", S["section"] == "local")
        draw_box("remote", S["section"] == "remote")
        draw_bottom()
        while True:
            is_wait = True
            draw()

            if screen.has_resized():
                tm.clear()
                break

            if key_code := screen.get_key():

                is_wait = False
                KeyHandler.check(key_code, S)
                if action := S.get("action", None):
                    sect = S["section"]
                    if action == "enter":
                        enter_item = data[sect][S["selectedRow"][sect]]
                        if sect == "remote" and S["remoteorigin"] == "kubectl":
                            if S["kubectl"]["pod"] == "":
                                S["kubectl"]["pod"] = enter_item.split(" ")[0]
                            elif S["kubectl"]["container"] == "":
                                if enter_item == "..":
                                    S["kubectl"]["pod"] = ""
                                else:
                                    S["kubectl"]["container"] = enter_item
                            else:
                                if enter_item == "..":
                                    if S["path"]["remote"] == "":
                                        S["kubectl"]["container"] = ""
                                    else:
                                        if len(S["path"]["remote"].split("/")) == 2:
                                            S["path"]["remote"] = ""
                                        else:
                                            S["path"]["remote"] = os.path.dirname(
                                                S["path"]["remote"][:-1]
                                            )
                                elif type(enter_item) == str:
                                    S["path"]["remote"] += enter_item
                                else:
                                    continue

                            init_path_str()
                            load_data(sect)

                        elif type(enter_item) == str and enter_item == "..":
                            if sect == "local":
                                newpath = os.path.dirname(S["path"][sect])
                            else:
                                newpath = S3.parent_dir(S["path"][sect])
                            S["path"][sect] = newpath
                            init_path_str()
                            load_data(sect)
                        elif sect == "local" and (
                            type(enter_item) != str and enter_item.is_dir()
                        ):
                            S["path"][sect] = enter_item.path
                            init_path_str()
                            load_data(sect)
                        elif (
                            sect == "remote"
                            and type(enter_item) == str
                            and enter_item[-1] == "/"
                        ):
                            S["path"][sect] += enter_item
                            init_path_str()
                            load_data(sect)
                        else:
                            continue
                        draw_box(sect, S["section"] == sect)
                        S["selectedRow"][sect] = 0
                        S["scrollTop"][sect] = 0
                        S["cartedRows"][sect] = []

                    elif action == "select":
                        row = S["kwargs"]["row"]
                        rowdata = data[sect][row]
                        if (
                            sect == "local"
                            and not (type(rowdata) == str and rowdata == "..")
                            and not (type(rowdata) != str and rowdata.is_dir())
                        ) or (sect == "remote" and type(rowdata) == dict):
                            if row in S["cartedRows"][sect]:
                                S["cartedRows"][sect].remove(row)
                            else:
                                S["cartedRows"][sect].append(row)

                        pass

                    elif action == "esc":
                        S["confirmaction"] = "quit"
                        confirm_msg = f"Are you sure you want to quit?"
                        confirm(confirm_msg)

                    elif action == "copy":
                        if S["cartedRows"][sect]:
                            sources = [data[sect][row] for row in S["cartedRows"][sect]]
                        else:
                            sources = [data[sect][S["selectedRow"][sect]]]
                            if (
                                (sect == "local" and sources[0].is_dir())
                                or (type(sources[0]) == str and sources[0] == "..")
                                or (sect == "remote" and type(sources[0]) != dict)
                            ):
                                continue
                        if S["remoteorigin"] == "kubectl" and (
                            S["kubectl"]["pod"] == "" or S["kubectl"]["container"] == ""
                        ):
                            continue
                        if sect == "local":
                            S["queue"] = [
                                os.path.join(S["path"]["local"], source.name)
                                for source in sources
                            ]
                        else:
                            S["queue"] = [
                                S["path"]["remote"] + source["key"]
                                for source in sources
                            ]
                        S["confirmaction"] = "copy"
                        action = "download" if sect == "remote" else "upload"
                        confirm_msg = f"Are you sure you want to {action}?"
                        confirm(confirm_msg)

                    elif action == "yes":
                        S["confirm"] = "yes"
                        draw_confirm_button()

                    elif action == "no":
                        S["confirm"] = "no"
                        draw_confirm_button()

                    elif action == "confirm":
                        draw_confirm_button()
                        if S["confirm"] == "yes":
                            if S["confirmaction"] == "copy":
                                S["destination"] = S["path"][
                                    "remote" if sect == "local" else "local"
                                ] + ("/" if sect == "local" else "")
                                screen.close()

                                action_and_exit("copy", S)
                                sys.exit()

                            if S["confirmaction"] == "quit":
                                tm.clear()
                                sys.exit("Bye")

                        S["confirmaction"] = ""
                        clear_confirm()

                    elif action == "cancel":
                        clear_confirm()

                    elif action == "tab":
                        draw_box("local", S["section"] == "local")
                        draw_box("remote", S["section"] == "remote")
                        pass

                    if "kwargs" in S:
                        del S["kwargs"]
                    del S["action"]

            if is_wait:
                time.sleep(0.02)

    tm = TextMode(screen)
    do()


def main():
    if len(sys.argv) == 1 or (
        not sys.argv[1].startswith("s3://")
        and sys.argv[1] not in ["k8s", "kube", "kubectl", "k"]
    ):
        sys.stdout.write("Usage: s3dir s3://{bucket-name} , s3dir k\n")
        sys.exit()

    if sys.argv[1] in ["k8s", "kube", "kubectl", "k"]:
        S["remoteorigin"] = "kubectl"
    else:
        S["s3bucket"] = sys.argv[1][5:]
        if S["s3bucket"][-1] == "/":
            S["s3bucket"] = S["s3bucket"][:-1]

    def signal_handler(sig, frame):
        sys.exit("Bye")

    signal.signal(signal.SIGINT, signal_handler)

    S["path"]["local"] = os.getcwd()
    load_data("local")
    load_data("remote")

    while True:
        if Screen.wrapper(layout):
            break

    sys.stdout.write("Bye\n")


if __name__ == "__main__":
    main()
