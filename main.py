import requests, json
import PySimpleGUI as sg

def main():
    sg.theme('DarkAmber')
    layout = [  [sg.Text('Search for a game (min 3 characters):'), sg.InputText(enable_events=True, key='gameNameInput')],
                [sg.Listbox([], size=(40,5), key='gameList', enable_events=True)],
                [sg.Text("Game Selected:"), sg.Text('', key='gameSelectedText', size=(50,1))],
                [sg.Text("Set State: "), sg.InputText(key='rpcState'), sg.Text("Set Details: "), sg.InputText(key='rpcDetails')]
                [sg.Button("Submit", key='submit'), sg.Button("Cancel", key='cancel')] ]

    window = sg.Window("disGame", layout)

    while True:
        event, values = window.read()
        print(event, values)

        if event == sg.WIN_CLOSED or event == 'cancel': # if user closes window or clicks cancel
            break

        if event == 'gameNameInput' and len(values['gameNameInput']) >= 3:
            print("Looking for ", values['gameNameInput'])
            data = filterData(values['gameNameInput'])
            print(data)
            if data:
                window['gameList'].update([x for x in data])
            else: window['gameList'].update([])

        elif event == 'gameList' and len(values['gameList']):
            window['gameSelectedText'].update(value=values['gameList'][0])

    window.close()

def loadData():
    """load data and remove all unnecessary info"""
    r = requests.get('https://discord.com/api/v8/applications/detectable')
    r = r.json()
    data = {}
    for item in r:
        data[item["name"]] = item["id"]
    return data

def filterData(query):
    """create and return a new dict of values name of which matches with the query"""
    returnData = {}
    for item in DATA:
        if query.lower() in item.lower():
            returnData[str(item)] = DATA[item]
    return returnData

if __name__ == '__main__':
    global DATA
    DATA = loadData()
    main()
