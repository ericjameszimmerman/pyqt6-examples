import customtkinter as ctk
import tkinter as tk
from threading import Thread
import zmq
from datetime import datetime

class ZMQListener(Thread):
    def __init__(self, app, update_callback):
        super().__init__()
        self.app = app
        self.update_callback = update_callback
        self.active = True
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        try:
            self.socket.connect("tcp://localhost:5555")  # Adjust as needed
        except zmq.ZMQError as e:
            print(f"Failed to connect: {e}")
            self.active = False
        self.topics = {str(i): {'subscribe': False, 'visible': True} for i in range(1, 33)}

    def run(self):
        while self.active:
            try:
                message = self.socket.recv_string(zmq.NOBLOCK)
                topic, msg = message.split()
                if topic in self.topics and self.topics[topic]['subscribe'] and self.topics[topic]['visible']:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    self.app.after(0, self.update_callback, timestamp, topic, msg)
            except zmq.Again:
                continue

    def stop(self):
        self.active = False
        self.socket.close()
        self.context.term()

    def subscribe(self, topic):
        if self.active:
            self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)
            self.topics[topic]['subscribe'] = True

    def unsubscribe(self, topic):
        if self.active:
            self.socket.setsockopt_string(zmq.UNSUBSCRIBE, topic)
            self.topics[topic]['subscribe'] = False

    def toggle_visibility(self, topic):
        self.topics[topic]['visible'] = not self.topics[topic]['visible']

class App(ctk.CTk):
    WIDTH = 1200
    HEIGHT = 800

    def __init__(self):
        super().__init__()
        self.title('ZeroMQ Topic Monitor')
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.listener = ZMQListener(self, self.add_message)
        if self.listener.active:
            self.listener.start()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_widgets()

    def create_widgets(self):
        self.frame_sidebar = ctk.CTkFrame(master=self, width=300, corner_radius=0)
        self.frame_sidebar.pack(side="left", fill="y", expand=False)

        self.frame_content = ctk.CTkFrame(master=self)
        self.frame_content.pack(side="left", fill="both", expand=True)

        # Using tkinter Listbox for messages display
        self.message_list = tk.Listbox(self.frame_content, bg="white", fg="black", font=('Arial', 12))
        self.message_list.pack(pady=20, padx=20, fill="both", expand=True)

        for i in range(1, 33):
            frame = ctk.CTkFrame(master=self.frame_sidebar)
            frame.pack(pady=2, padx=20, fill="x")

            toggle = ctk.CTkSwitch(master=frame, text=f"Topic {i}")
            toggle.pack(side="left", fill="x", expand=True)
            toggle.command = lambda topic=str(i), t=toggle: self.toggle_topic(topic, t.get())

            eye_button = ctk.CTkButton(master=frame, text="👁", width=40, height=40)
            eye_button.pack(side="right")
            eye_button.command = lambda topic=str(i): self.toggle_visibility(topic)

    def toggle_topic(self, topic, checked):
        if checked:
            self.listener.subscribe(topic)
        else:
            self.listener.unsubscribe(topic)

    def toggle_visibility(self, topic):
        self.listener.toggle_visibility(topic)

    def add_message(self, timestamp, topic, message):
        if self.listener.topics[topic]['visible']:
            self.message_list.insert(tk.END, f"{timestamp} {topic} {message}")

    def on_closing(self):
        self.listener.stop()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
