import PySimpleGUI as sg
import os.path
from backend import __backend__ as go

left_pane = [
    [
        sg.Text("Login"),
    ],
    [
        sg.Text("Password"),
    ],
    [
        sg.Text("Captcha solver API key"),
    ],
]
right_pane = [
    [
        sg.Input(size=(25,1), enable_events=True, key="-LOGIN-", right_click_menu=[[''], ['Paste Login']]),
    ],
    [
        sg.Input(size=(25,1), enable_events=True, key="-PASSWORD-", right_click_menu=[[''], ['Paste Password']], password_char='*'),
    ],
    [
        sg.Input(size=(25,1), enable_events=True, key="-API-", right_click_menu=[[''], ['Paste API']]),
    ],
]
left_layout = [
    [
        sg.Column(left_pane),
        sg.VSeparator(),
        sg.Column(right_pane)
    ]
]
file_list_column = [
    [
        sg.Text("User IDs Folder"),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(values=[], enable_events=True, size=(40,5), key="-FILE LIST-")
    ],
    [
      sg.Col(left_layout, vertical_alignment='center')
    ],
    [
        sg.Button("Scrape", key="-SCRAPE-"),
    ],
]
preview_column = [
    [sg.Text("Progress:", s=(20,2))],
    [sg.ProgressBar(100, orientation='h', s=(20,5), k='-PBAR-')]
]
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(preview_column),
    ]
]
window = sg.Window("snParser", layout, element_justification='c', font='Helvetica')
# global vars
filename = ""
login = ""
password = ""
api = ""

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".txt"))
        ]
        window["-FILE LIST-"].update(fnames)
    if event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"],values["-FILE LIST-"][0]
            )
        except:
            pass
    if event == "-LOGIN-":
        login = values["-LOGIN-"]
    if event == "Paste Login":
        window["-LOGIN-"].update(sg.clipboard_get())
    if event == "-PASSWORD-":
        password = values["-PASSWORD-"]
    if event == "Paste Password":
        window["-PASSWORD-"].update(sg.clipboard_get())
    if event == "-API-":
        api = values["-API-"]
    if event == "Paste API":
        window["-API-"].update(sg.clipboard_get())
    if event == "-SCRAPE-":
        args = ""
        if not filename:
            args += "Путь не указан. "
        if not login:
            args += "Логин не указан. "
        if not password:
            args += "Пароль не указан. "
        if not api:
            args += "АПИ-ключ не указан. "
        if args:
            sg.Popup(args, keep_on_top=True, title='Ошибка')
        else:
            try:
                IDs = go.readIds(filename)
                count = go.np.count_nonzero(IDs)
                output_array = []
                go.getToMainPage(login, password, api)
                counter = 1
                for single_id in go.np.nditer(IDs):
                    output_array.append(go.singleHumanHandler(single_id))
                    window["-PBAR-"].update((counter/count)*100)
                    counter += 1
                go.writeOutput(output_array)
                go.driver.save_screenshot("4.png")
            except Exception as ex:
                print(ex)
            finally:
                go.driver.close()
                go.driver.quit()

window.close()
