from tkinter import *
from tkinter import font
from tkinter import ttk

import asyncio, uuid
import threading

from aioconsole import ainput
from common.socketconnection import SocketConnection


class GUI:
    # constructor method
    def __init__(self):
        # chat window which is currently hidden
        self.id = str(uuid.uuid4())
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)
        # create a Label
        self.pls = Label(
            self.login,
            text="Please login to continue",
            justify=CENTER,
            font="Helvetica 14 bold",
        )

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)
        # create a Label
        self.labelName = Label(self.login, text="Name: ", font="Helvetica 12")

        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login, font="Helvetica 14")

        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)

        # set the focus of the cursor
        self.entryName.focus()

        # create a Continue Button
        # along with action
        self.go = Button(
            self.login,
            text="CONTINUE",
            font="Helvetica 14 bold",
            command=lambda: self.goAhead(self.entryName.get()),
            # command=lambda: self.main(),
        )

        self.go.place(relx=0.4, rely=0.55)
        self.Window.mainloop()

    # def goAhead(self, name):
    #     self.login.destroy()
    #     self.layout(name)
    #     self.main()
    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        #     # the thread to receive messages
        socket_thread = threading.Thread(target=self.socket_loop, args=(name,))
        socket_thread.start()

    # The main layout of the chat
    def layout(self, name):
        self.name = name
        print(name)
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#17202A")
        self.labelHead = Label(
            self.Window,
            bg="#17202A",
            fg="#EAECEE",
            text=self.name,
            font="Helvetica 13 bold",
            pady=5,
        )

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window, width=450, bg="#ABB2B9")

        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = Text(
            self.Window,
            width=20,
            height=2,
            bg="#17202A",
            fg="#EAECEE",
            font="Helvetica 14",
            padx=5,
            pady=5,
        )

        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = Label(self.Window, bg="#ABB2B9", height=80)

        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = Entry(
            self.labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13"
        )

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(
            self.labelBottom,
            text="Send",
            font="Helvetica 10 bold",
            width=20,
            bg="#ABB2B9",
            command=lambda: self.sendButton(self.entryMsg.get()),
        )

        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1, relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        self.sendMessage()
        # snd = threading.Thread(target=self.sendMessage)
        # snd.start()

    async def receive_messages(self, conn):
        while True:
            data = await conn.receive_json()
            name = self.getName(data)
            eventType = data["type"]
            if eventType == "join":
                self.addText(f"{name} joined the chat")
            elif eventType == "leave":
                self.addText(f"{name} left the chat")
            elif eventType == "message":
                self.addText(f"{name}: {data['message']}")
            print(f"server: {data}")

    def getName(self, data):
        if data["id"] == self.id:
            return "You"
        return data["name"]

    def addText(self, text):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, text + "\n")

        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def sendMessage(self):
        print(self.msg)
        self.textCons.config(state=DISABLED)
        asyncio.run_coroutine_threadsafe(
            self.conn.send_json({"event": "message", "message": self.msg}), self.loop
        )

    async def init_socket(self, name):
        reader, writer = await asyncio.open_connection("127.0.0.1", 8080)
        conn = SocketConnection(reader, writer)
        await conn.send_json({"id": self.id, "name": name})
        return conn

    def socket_loop(self, name):
        self.loop = asyncio.new_event_loop()
        self.conn = self.loop.run_until_complete(self.init_socket(name))
        self.loop.run_until_complete(self.receive_messages(self.conn))
        self.loop.close()
        writer.close()


g = GUI()
