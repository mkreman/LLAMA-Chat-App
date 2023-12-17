from langchain.llms import CTransformers
from customtkinter import *
import threading
from PIL import Image


# Loading the llama-2 model
llm = CTransformers(model='llama-2-7b-chat.ggmlv3.q8_0.bin',
                        model_type='llama',
                        config={'max_new_tokens':256,
                                'temperature':0.01})

class App:
    def __init__(self, main):
        self.main_window = main
        self.theme = 'System'
        self.output_box = CTkTextbox(master=self.main_window, width=480, height=530, activate_scrollbars=True,
                                    font=('Times New Roman', 17), wrap='word')
        # Set a different color for queries
        self.output_box.tag_config('query', foreground="#780000")

        # Set the default theme
        set_appearance_mode(self.theme)  # Modes: "System" (standard), "Dark", "Light"
        set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"        

        self.main_window.title('LLAMA Chat App')
        self.entry_frame = CTkFrame(master=self.main_window)

        self.entry = CTkEntry(master=self.entry_frame, placeholder_text="Enter your query", width=350)
        self.entry.grid(row=0, column=0, sticky="nsew")
        
        send_image = CTkImage(dark_image=Image.open('./send.png'))
        self.send_button = CTkButton(self.entry_frame,
                                     image=send_image,
                                     text='',
                                     width=45, 
                                     command=self.send_query)
        self.send_button.grid(row=0, column=1, padx=(5,))
        
        self.entry_frame.pack(side='bottom', pady=(0,15))

        self.output_box.pack(side='top', padx=10, pady=10)

        self.main_window.bind('<Return>', lambda event: self.send_query())
        self.main_window.resizable(False, False)
        self.main_window.geometry("500x600")
        self.main_window.mainloop()

    def send_query(self):
        query = self.entry.get()
        if query != '':
            self.output_box.insert(END, 'Query: ' + query+'\n', 'query')
            self.output_box.see(END)
            
            self.entry.delete(first_index=0, last_index=END)
            self.entry.configure(state="disabled")

            threading.Thread(target=self.get_response, args=(query,), daemon=True).start()

    def get_response(self, query):
        response = llm(query)
        self.output_box.insert(END, 'Response: ' + response +'\n\n')
        self.output_box.see(END)
        self.entry.configure(state="normal")


if __name__ == '__main__':
    App(CTk())