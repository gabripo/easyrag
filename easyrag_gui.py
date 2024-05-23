import PySimpleGUI as sg

def ui_get_choices() -> list:
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

    choices_submitted = False
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            if not choices_submitted:
                print("Window closed without submitting preferences!")
                data_folder = None
                llm = None
            break
        elif event == "Submit":
            choices_submitted = True
            data_folder = values['-FOLDER-']
            llm = values['-LLM-']

    window.close()
    return [data_folder, llm]

if __name__ == '__main__':
    choices = ui_get_choices()
    if any(choices):
        print('Chosen folder is: ', choices[0])
        print('Chosen LLM is: ', choices[1])