import socket
from threading import *
from tkinter import *
import tkinter.scrolledtext as tkst


def client(m, ip, port):
    try:
        m.destroy()
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.bind((ip, int(port)))
        c.listen(3)

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

        sendtext = Entry(mk)
        sendtext.grid(row=1, column=0, sticky="NEWS")

        global cli_list
        cli_list = list()

        def cli(s, d):

            def send(data):
                for i in cli_list:
                    i.send(data.encode('utf-8'))
                    editArea.config(state=NORMAL)
                    editArea.insert(INSERT, data)
                    editArea.config(state=DISABLED)
            if d == "s":
                send(s)
            else:
                while True:
                    data = s.recv(1024)
                    send(str(d) + ":" + data.decode('utf-8') + "\n")

        def acc():
            while True:
                s, d = c.accept()
                cli_list.append(s)
                editArea.config(state=NORMAL)
                editArea.insert(INSERT, str(d)+"Joint in the fun\n")
                editArea.config(state=DISABLED)
                t1 = Thread(target=cli, args=[s, d])

                t1.start()

        t3 = Thread(target=acc)

        t3.start()

        button=Button(mk, text='SEND', width=25, command=lambda: cli("server:" + sendtext.get() + "\n", "s"))
        button.grid(row=1, column=1, sticky="NEWS")

        mk.mainloop()

        for i in cli_list:
            i.close()

    except Exception as a:
        print(a)


try:
    m = Tk()
    m.title("Server")
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
