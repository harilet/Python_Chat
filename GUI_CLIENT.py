import socket
from threading import *
from tkinter import *
import tkinter.scrolledtext as tkst


def client(m, ip, port):
    try:
        m.destroy()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))

        mk = Tk()
        mk.title(ip)
        editArea = tkst.ScrolledText(
            master=mk,
            wrap=WORD,
            width=50,
            height=25
        )
        editArea.grid(row=0, column=0, sticky="NEWS", columnspan=2)
        editArea.config(state=DISABLED)
        sendtext=Entry(mk)
        sendtext.grid(row=1, column=0, sticky="NEWS")

        def send():

            data = sendtext.get()
            s.send(data.encode('utf-8'))
            """editArea.config(state=NORMAL)
            editArea.insert(INSERT, "YOU:"+data + "\n")
            editArea.config(state=DISABLED)"""
            sendtext.delete(0, 'end')

        button = Button(mk, text='SEND', width=25, command=lambda: send())
        button.grid(row=1, column=1, sticky="NEWS")

        def recv():

            while True:
                data = s.recv(1024)
                editArea.config(state=NORMAL)
                editArea.insert(INSERT, data.decode('utf-8', 'strict'))
                editArea.config(state=DISABLED)
                if data == "stop":
                    break

        t2 = Thread(target=recv)

        t2.start()

        mk.mainloop()

        s.close()

    except Exception as a:
        print(a)


try:
    m = Tk()
    m.title("Client")
    Label(m, text="IP").grid(row=0, column=0, sticky="NEWS")
    Label(m, text="PORT").grid(row=0, column=2, sticky="NEWS")

    ip = Entry(m)
    port = Entry(m)
    ip.grid(row=0, column=1)
    port.grid(row=0, column=3)

    button = Button(m, text='CONNECT', width=25, command=lambda: client(m,ip.get(), port.get()))
    button.grid(row=1, column=2, sticky="NEWS")

except Exception as a:
    print(a)
m.mainloop()
