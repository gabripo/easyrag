import os
import PySimpleGUI as sg

sg.set_options(font=("Arial Bold", 16))
rag_folder_name = "chroma_data"


def ui_get_options() -> dict:
    data_column = sg.Column(
        [
            [sg.Text("Select folder with documents:")],
            [
                sg.In(size=(25, 1), enable_events=True, key="-DATA_FOLDER-"),
                sg.FolderBrowse(initial_folder=os.getcwd()),
            ],
        ]
    )

    supported_llms = ["llama3"]
    default_llm = "llama3"
    llm_column = sg.Column(
        [
            [sg.Text("Select LLM to use:")],
            [
                sg.Combo(
                    supported_llms,
                    key="-LLM-",
                    readonly=True,
                    default_value=default_llm,
                )
            ],
            [sg.Text("System prompt:")],
            [
                sg.Multiline(
                    default_text="You got some documents.\nReply to questions concerning them.",
                    size=(25, 4),
                    key="-SYS_PROMPT-",
                )
            ],
        ]
    )

    options_column = sg.Column(
        [
            [
                sg.Button("Submit"),
                sg.Checkbox("Use web interface", default=True, key="-USE_WEB-"),
            ]
        ],
        element_justification="center",
        expand_x=True,
    )

    layout = [[data_column, llm_column], [options_column]]
    window_title = "RAG options"
    window = sg.Window(window_title, layout)

    options_submitted = False
    user_options = {}
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            if not options_submitted:
                print("Window closed without submitting options!")
            break
        elif event == "Submit":
            options_submitted = True
            user_options["data_folder"] = values["-DATA_FOLDER-"]
            user_options["llm"] = values["-LLM-"]
            user_options["rag_folder"] = os.path.join(
                user_options["data_folder"], rag_folder_name
            )
            user_options["system_prompt"] = values["-SYS_PROMPT-"]
            user_options["use_web_interface"] = values["-USE_WEB-"]
            user_options["consider_history"] = True  # hardcoded
            break

    window.close()
    return user_options


def ui_check_options(user_options={}) -> bool:
    required_options = [
        "data_folder",
        "rag_folder",
        "llm",
        "system_prompt",
        "use_web_interface",
        "consider_history",
    ]
    if user_options and all(k in user_options for k in required_options):
        print("Selected data folder is: ", user_options["data_folder"])
        print("Selected target folder for RAG data is: ", user_options["rag_folder"])
        print("Selected LLM is: ", user_options["llm"])
        print("System prompt is: ", user_options["system_prompt"])
        print("Will the web interface be used? ", user_options["use_web_interface"])
        print(
            "Will the chatbot consider the history of messages?",
            user_options["consider_history"],
        )
        return True
    else:
        print("Some user-specified options are missing!")
        return False


def ui_get_query():
    layout = [
        [sg.Text("User prompt:")],
        [
            sg.Multiline(
                default_text="Summarize the content of the documents.",
                size=(25, 4),
                key="-USR_PROMPT-",
            )
        ],
        [sg.Button("Submit")],
    ]
    window_title = "Query"
    window = sg.Window(window_title, layout)

    user_query = ""
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "Submit":
            user_query = values["-USR_PROMPT-"]
            break

    window.close()
    return user_query


def ui_print(text_to_print, window_title="Print text"):
    layout = [[sg.Multiline(write_only=True, size=(60, 10), reroute_cprint=True)]]
    window = sg.Window(window_title, layout, finalize=True)
    sg.cprint(text_to_print)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

    window.close()
    pass


def ui_yes_no(window_text="Continue?") -> bool:
    layout = [[sg.Text(window_text)], [sg.Button("Yes"), sg.Button("No")]]
    window_title = "User action required"
    window = sg.Window(window_title, layout)

    user_choice = False
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "No":
            user_choice = False
            break
        if event == "Yes":
            user_choice = True
            break

    window.close()
    return user_choice


if __name__ == "__main__":
    while True:
        user_options = ui_get_options()
        ui_check_options(user_options)
        user_query = ui_get_query()
        ui_print(user_query)
        if not ui_yes_no():
            break
