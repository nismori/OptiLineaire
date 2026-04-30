import customtkinter as ctk

app = ctk.CTk()
app.geometry("1920x1080")
app.title("Application de résolution de problèmes linéaires")
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
button = ctk.CTkButton(app, text="Méthode du Simplexe")
button.pack()
button.grid(row=0,column=1)
app.mainloop()