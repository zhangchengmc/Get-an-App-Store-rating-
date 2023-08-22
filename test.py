import requests
from bs4 import BeautifulSoup
import PySimpleGUI as sg

# 创建对话框布局
layout = [
    [sg.Text('App Store 预览链接:')],
    [sg.InputText(key='-URL-', size=(40, 1)), sg.Button('粘贴')],
    [sg.Button('获取评分', size=(20, 1))],
    [sg.Text('App Store 软件评分是:', pad=((0, 0), (10, 10)))],
    [sg.Output(size=(50, 10), key='-OUTPUT-')],
    [sg.Radio('获取模式', 'RADIO1', default=True, key='-RELINK-'), sg.Radio('保存模式', 'RADIO1', key='-SAVE-')],
    [sg.Button('复制输出', size=(15, 1)), sg.Button('取消', size=(15, 1))]
]

# 创建主窗口
window = sg.Window('App Store 数据获取器', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == '取消':
        break
    elif event == '粘贴':
        clipboard_data = sg.clipboard_get()
        window['-URL-'].update(clipboard_data)
    elif event == '获取评分':
        url = values['-URL-']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find('span', class_='we-customer-ratings__averages__display').text
        window['-OUTPUT-'].update(f'App Store 软件评分是: {data}\n')
        if values['-SAVE-']:
            with open('data.md', 'w') as f:
                f.write(data)
                window['-OUTPUT-'].print('数据已保存为data.md\n')
    elif event == '复制输出':
        output_text = window['-OUTPUT-'].get()
        sg.clipboard_set(output_text)

window.close()