import Tkinter as tk

class mainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.read_config()
        self.root.title("Cliente - Check4Face! {} v{}".format(self.conf["build"], self.conf["version"]))
        self.root.geometry("700x500")
        self.root.resizable(0,0) #Bloquea el cambio de tamano
        self.load_estructures()
        self.read_news()
        self.root.mainloop()

    def read_config(self):
        config = open("../data/config.dat") #Abre el archivo de configuracion
        self.conf = {}
        for linea in config:
            if "#" in linea:
                if linea[0] == "#": #Si comienza con # es un comentario, por lo tanto ignora esa linea
                    continue
                else: #Si no comienza con #
                    linea = (linea.strip().split("#"))[0] #Considera solo lo que esta antes del #
            key, val = linea.strip().split("=")
            key = key.strip()
            val = val.strip()
            self.conf[key] = val #Guarda valor de la configuracion en el dic
        config.close()

    def load_estructures(self):
        #Frames
        self.frame_news = tk.Frame(self.root, bg="black", width=425, height=480).place(x="10", y="10")
        self.frame_log = tk.Frame(self.root, bg="black", width=250, height=370).place(x="440", y="10")
        self.frame_panel = tk.Frame(self.root , bg="black", width=250, height=200).place(x="440", y="700")
        #Botones
        self.but_log = tk.Button(self.frame_log, text="Entrar").place(x=520, y=460)
        self.but_reg = tk.Button(self.frame_log, text="Registar").place(x=600, y=460)
        #Entrys
        self.ent_usr = tk.Entry(self.frame_log).place(x=520,y=400)
        self.ent_pass = tk.Entry(self.frame_log).place(x=520, y=430)
        #Etiquetas
        self.title = tk.Label(self.frame_panel, text="Check4Face!", font=("Calibri",34)).place(x=450, y=30)
        self.news = tk.Label(self.frame_news, text="Noticias Actualizadas!").place(x=10,y=10)
        self.lb_usr = tk.Label(self.frame_log, text="Username:").place(x=450, y=400)
        self.lb_pass = tk.Label(self.frame_log, text="Password:").place(x=450, y=430)
        #Text
        self.txt_news = tk.Text(self.frame_news)
        ########CONFIG
        self.txt_news.config(width=55, height=30)
        self.txt_news.place(x=25, y=35)

    def read_news(self):
        news = open("../data/news.dat")
        for linea in news:
            self.txt_news.insert("end", linea)
        news.close()

window = mainWindow()
