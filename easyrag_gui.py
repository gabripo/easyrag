import PySimpleGUI as sg

def ui_get_options() -> dict:
    data_column = sg.Column([
        [sg.Text("Select folder with documents:")],
        [sg.In(size=(25,1), enable_events=True, key='-DATA_FOLDER-'), sg.FolderBrowse()],
        [sg.Text("Select target folder for RAG data:")],
        [sg.In(size=(25,1), enable_events=True, key='-RAG_FOLDER-'), sg.FolderBrowse()],
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
        [data_column, llm_column],
        [options_column]
    ]
    window_title = 'RAG options'
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
            user_options['data_folder'] = values['-DATA_FOLDER-']
            user_options['llm'] = values['-LLM-']
            user_options['rag_folder'] = values['-RAG_FOLDER-']
            break

    window.close()
    return user_options

def ui_check_options(user_options={}) -> bool:
    if user_options and all(value for value in user_options.values()):
        print('Selected data folder is: ', user_options['data_folder'])
        print('Selected target folder for RAG data is: ', user_options['rag_folder'])
        print('Selected LLM is: ', user_options['llm'])
    else:
        print('Some user-specified options are missing!')

if __name__ == '__main__':
    user_options = ui_get_options()
    ui_check_options(user_options)