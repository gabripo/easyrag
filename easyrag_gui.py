import PySimpleGUI as sg

def ui_get_options() -> dict:
    data_column = sg.Column([
        [sg.Text("Select folder with documents:")],
        [sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()]
    ])

    supported_llms = ['llama3']
    default_llm = 'llama3'
    llm_column = sg.Column([
        [sg.Text("Select LLM to use:")],
        [sg.Combo(supported_llms, key='-LLM-', readonly=True, default_value=default_llm)]
    ])

    options_column = sg.Column([
        [sg.Button("Submit")]
    ], element_justification='center', expand_x=True)

    layout = [
        [data_column,
        llm_column],
        [options_column]
    ]

    window_title = 'Load folder'
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
            user_options['data_folder'] = values['-FOLDER-']
            user_options['llm'] = values['-LLM-']
            break

    window.close()
    return user_options

def ui_check_options(user_options={}) -> bool:
    if user_options and all(value for value in user_options.values()):
        print('Chosen folder is: ', user_options['data_folder'])
        print('Chosen LLM is: ', user_options['llm'])
    else:
        print('Some user-specified options are missing!')

if __name__ == '__main__':
    user_options = ui_get_options()
    ui_check_options(user_options)