import requests, json
import PySimpleGUI as sg
from pypresence import Presence

RPC = None

def main():
    global RPC
    sg.theme('DarkAmber')
    layout = [  [sg.Text('Search for a game (min 3 characters):'), sg.InputText(enable_events=True, key='gameNameInput')],
                [sg.Listbox([], size=(40,5), key='gameList', enable_events=True)],
                [sg.Text("Game Selected:"), sg.Text('', key='gameSelectedText', size=(50,1))],
                [sg.Text("Set Details: "), sg.InputText(key='rpcDetails', size=(20,1)), sg.Text("Set State: "), sg.InputText(key='rpcState', size=(20,1)) ],
                [sg.Button("Submit", key='submit'), sg.Button("Cancel", key='cancel')] ]

    window = sg.Window("diGame", layout)

    while True:
        event, values = window.read()
        print(event, values)

        if event == sg.WIN_CLOSED or event == 'cancel': # if user closes window or clicks cancel
            if RPC: RPC.close()
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

        elif event == 'submit':
            if not values['gameList']:
                sg.Popup('You have to select a game!', keep_on_top=True)

            else:
                client_id = DATA[values['gameList'][0]]
                state = window['rpcState'].get() or None
                details = window['rpcDetails'].get() or None

                if RPC: RPC.close() # if not rpc -> RPC = Presence... wont work because
                                    # then the user cannot change to different game
                RPC = Presence(client_id, pipe=0)
                RPC.connect()

                RPC.update(details=details, state=state)

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
