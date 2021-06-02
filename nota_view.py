from os import F_OK
from aluno import Aluno
from tkinter.constants import CENTER, COMMAND, DISABLED, END, NORMAL, S
from tkinter.font import BOLD, Font
from typing import ItemsView, Sized
from nota import Nota
from PIL import Image, ImageTk
from tkinter import Event, tix
import tkinter as tk
from tkinter import BitmapImage, Image, Label, ttk
from tkinter import messagebox as mb

class Notawin:

    def __init__(self,win,):
        self.notaCRUD = Nota()
        self.alunoSelected = None
        self.alunoResult = None
        self.disciSelected = None
        self.desciResult = None

        #Criar os componentes de tela
        self.notaed2Label = tk.Label(win, text='_______________', background='#292826',foreground='#F1780e')
        self.notaedLabel = tk.Label(win, text='______________________________________',background='#292826',foreground='#F1780e')
        self.notaLabel = tk.Label(win, text='NOTAS',font="Bold 17", background='#292826',foreground='#F1780e')

        self.av1Label = tk.Label(win, text='AV1',font="Bold 10", background='#292826',foreground='#F1780e') 
        self.av1Edit = tk.Entry(width = 32, bd=1,bg='#dde')

        self.av2Label = tk.Label(win, text='AV2',font="Bold 10", background='#292826',foreground='#F1780e') 
        self.av2Edit = tk.Entry(width = 32, bd=1,bg='#dde')

        self.av3Label = tk.Label(win, text='AV3',font="Bold 10", background='#292826',foreground='#F1780e') 
        self.av3Edit = tk.Entry(width = 32, bd=1,bg='#dde')

        self.mediaLabel = tk.Label(win, text='Media',font="Bold 10", background='#292826',foreground='#F1780e') 
        self.mediaEdit = tk.Entry(width = 32, bd=1,bg='#dde')

        self.alunoLabel = tk.Label(win, text='Aluno',font="Bold 10", background='#292826',foreground='#F1780e') 
        self.alunoEdit = tk.Entry(width = 32, bd=1,bg='#dde')
        
        self.discLabel = tk.Label(win, text='Disciplina',font="Bold 10", background='#292826',foreground='#F1780e') 
        self.discEdit = tk.Entry(width = 32, bd=1,bg='#dde')
        #------------
        #Botoes
        #------------
        self.buscaEdit = tk.Entry(width=85, bd=1,bg='#dde')
        self.buscaEdit.insert(0, 'Digite sua Matrica')
        self.buscaEdit.configure(state=DISABLED)
        self.buscaEdit.bind('<Button-1>', self._on_click)
        self.buscaEdit.bind("<Return>",(lambda Event: self.get_Aluno(self.buscaEdit.get())))
        self.btnbusca = tk.Button(win, 
                text='Busca',bg='#dde',command=(lambda : self.get_Aluno(self.buscaEdit.get())), bd=0)

        self.btnCadastrar = tk.Button(win, 
                text = 'Salvar',bg='#dde', width = 7, command=self._on_cadastrar_clicked, bd=1)

        self.btnAlterar = tk.Button(win, 
                text = 'Editar',bg='#dde', width = 7, command=self._on_atualizar_clicked, bd=1)

        self.btnExcluir = tk.Button(win, 
                text = 'Excluir',bg='#dde', width = 7, command=self._on_deletar_clicked, bd=1)

        
        
        self.notaList = ttk.Treeview(win, columns=(1,2,3,4,5,6), show='headings')
        
        self.verscrlbar = ttk.Scrollbar(win,orient="vertical", command=self.notaList.yview)
        self.verscrlbar.pack(side = 'right', fill='x')
        self.notaList.configure(yscrollcommand = self.verscrlbar.set)

        self.notaList.heading(1, text='Aluno')
        self.notaList.heading(2, text='Disciplina')
        self.notaList.heading(3, text='AV 1')
        self.notaList.heading(4, text='AV 2')
        self.notaList.heading(5, text='AV 3')
        self.notaList.heading(6, text='Media')

        self.notaList.column(1, minwidth=0, width=200)
        self.notaList.column(2, minwidth=0, width=100)
        self.notaList.column(3, minwidth=0, width=45)
        self.notaList.column(4, minwidth=0, width=40)
        self.notaList.column(5, minwidth=0, width=40)
        self.notaList.column(6, minwidth=0, width=50)

        self.notaList.pack()
        self.notaList.bind("<<TreeviewSelect>>", self._on_mostrar_clicked)

        #Posicionar os componentes na tela
        self.notaed2Label.place(x=440,y=80)
        self.notaedLabel.place(x=380,y=20)
        self.notaLabel.place(x=440,y=50)

        self.av1Label.place(x=460,y=130)
        self.av1Edit.place(x=530,y=130)
        
        self.av2Label.place(x=460,y=160)
        self.av2Edit.place(x=530,y=160)

        self.av3Label.place(x=460,y=190)
        self.av3Edit.place(x=530,y=190)

        self.mediaLabel.place(x=170,y=160)
        self.mediaEdit.place(x=220,y=160)
        
        self.alunoLabel.place(x=170,y=130)
        self.alunoEdit.place(x=220,y=130)

        self.discLabel.place(x=170,y=190)
        self.discEdit.place(x=220,y=190)

        self.buscaEdit.place(x=295,y=300)
        #--------
        # Botoes
        #--------
        #self.btnlista.place(x=865,y=298)
        self.btnbusca.place(x=820,y=298)
        self.btnCadastrar.place(x=670,y=250)
        self.btnAlterar.place(x=600,y=250)
        self.btnExcluir.place(x=530,y=250)
        self.notaList.place(x=300,y=330)
        self.verscrlbar.place(x=880,y=330, height=230)

        self.carregar_dados_iniciais_treeView()
        #--------
        # Funções
        #--------

    def _on_click(self, event):
        self.buscaEdit.configure(state=NORMAL)
        self.buscaEdit.delete(0, END)
        self.buscaEdit.unbind('<Button-1>',self._on_click)


    def get_Aluno(self,event):
        
            self.notaList.delete(*self.notaList.get_children())
            notas = self.notaCRUD.consultar_por_matricula(self.buscaEdit.get())
            if (len(notas)>0):
                
                item = self.notaList.selection()       
                for item in notas:
                    fk_aluno_id = item[0]
                    fk_disciplina_id = item[1]
                    av1 = item[2]
                    av2 = item[3]
                    av3 = item[4]
                    media = item[5]
                if fk_aluno_id == self.buscaEdit.get():
                    self.notaList.insert('','end',values=(str(fk_aluno_id),fk_disciplina_id,av1,av2,av3,media))
                
            else: notas != self.buscaEdit.get()
            id_aluno = Aluno()
            self.alunoResult = id_aluno.consultar_por_matricula(self.buscaEdit.get())
            lista = id_aluno.consultar_por_matricula(self.buscaEdit.get())
            item = self.notaList.selection()       
            for item in lista:
                            fk_aluno_id = item[1]
                                #deleta os campos prenchidos do formulario
                                #self.alunoEdit.configure(state=NORMAL)
                            self.alunoEdit.delete(0, tk.END)
                            self.alunoEdit.insert(0, fk_aluno_id)
                            #self.alunoEdit.configure(state=DISABLED)
                            self.av1Edit.delete(0, tk.END)
                            self.av2Edit.delete(0, tk.END)
                            self.av3Edit.delete(0, tk.END)
                            self.mediaEdit.delete(0, tk.END)
                            self.buscaEdit.delete(0, tk.END)

                            self.notaList.insert('','end',values=(str(fk_aluno_id),))
                            self.buscaEdit.insert(0, 'Digite sua Matrica')
                            self.buscaEdit.configure(state=DISABLED)
                            self.buscaEdit.bind('<Button-1>', self._on_click)
                        


    def _on_mostrar_clicked(self, event):
            #Seleção do usuario, linha na qual ele clicou
            selection = self.notaList.selection()
            item = self.notaList.item(selection)
            aluno = item["values"][0]
            dis = item["values"][1]
            av1 = item["values"][2]
            av2 = item["values"][3]
            av3   = item["values"][4]
            media = item["values"][5]
           
            self.av1Edit.delete(0, tk.END)
            self.av1Edit.insert(0, av1)
            self.av2Edit.delete(0, tk.END)
            self.av2Edit.insert(0, av2)
            self.av3Edit.delete(0, tk.END)
            self.av3Edit.insert(0, av3)
            self.mediaEdit.delete(0, tk.END)
            self.mediaEdit.insert(0, media)

    def carregar_dados_iniciais_treeView(self):
            self.notaList.delete(*self.notaList.get_children())
            registro = self.notaCRUD.consultar()

            count = 0
            for item in registro:
                fk_aluno_id = item[0]
                fk_disciplina_id = item[1]
                av1 = item[2]
                av2 = item[3]
                av3   = item[4]
                media = item[5]
               

                self.notaList.insert('','end',iid=count,values=(str(fk_aluno_id),fk_disciplina_id,av1,av2,av3,media))
                count = count + 1
            



    def _on_atualizar_clicked(self):
        linha = self.notaList.selection()
      
        if len(linha) != 0:
            fk_aluno_id = self.notaList.item(linha[0])["values"][0]
            fk_disciplina_id = self.notaList
            av1 = self.av1Edit.get()
            av2 = self.av2Edit.get()
            av3 = self.av3Edit.get()
            media = self.mediaEdit.get()
           

            if  self.notaCRUD.atualizar(fk_aluno_id,fk_disciplina_id,av1,av2,av3,media):

                self.notaList.item(self.notaList.focus(), values=(str(fk_aluno_id),av1,av2,av3,media))
                 #remover a seleção
                self.notaList.selection_remove(self.notaList.selection()[0])
                #----------#
                mb.showinfo("Mensagem", "Alteração executada com sucesso.")
                self.av1Edit.delete(0, tk.END)
                self.av2Edit.delete(0, tk.END)
                self.av3Edit.delete(0, tk.END)
                self.mediaEdit.delete(0, tk.END)
               
            else:
                mb.showinfo("Mensagem", "Erro na alteração.")
                self.av1Edit.focus_set()

    
    
    def _on_cadastrar_clicked(self):
        #Recuperar os dados dos campos texto
        fk_aluno_id = self.alunoEdit.get()
        fk_disciplina_id = self.discEdit.get()
        av1 = self.av1Edit.get()
        av2 = self.av2Edit.get()
        av3 = self.av3Edit.get()
        media = self.mediaEdit.get()
        

        #Chamar o cadastrar do aluno.py para cadastrar no banco
        #if (media) !="":
        if self.notaCRUD.cadastrar(fk_aluno_id,fk_disciplina_id,av1,av2,av3,media):
                numeroLinha = len(self.notaList.get_children())
                fk_aluno_id = self.notaCRUD.consultar_ultimo_id()
                
                
                self.notaList.insert('','end',numeroLinha,values=(str(fk_aluno_id),av1,av2,av3,media))
                if (av1+av2)/2>6:
                    media = (av1 + av2 )/2
                elif (av1<av3 and av1<av2):
                    media = (av3+av2)/2
                elif(av1>av2 and av2<av3):
                    media = (av2+av3)/2
                    #Mostrar mensagem para usuário
                    mb.showinfo("Mensagem", "Cadastro executado com sucesso!")
                    
                    #Limpar os campos texto
                    self.mediaEdit.insert(media)
                    self.av1Edit.delete(0,tk.END)
                    self.av2Edit.delete(0, tk.END)
                    self.av3Edit.delete(0, tk.END)
                    self.mediaEdit.delete(0, tk.END)
               
        
        else:
            mb.showinfo("Mensagem", "Erro no cadastro!")
            #Retornando o foco
            self.av1Edit.focus_set()
            self.av2Edit.focus_set()
            self.av3Edit.focus_set()
            self.mediaEdit.focus_set()
           


    def _on_deletar_clicked(self):
        linhaSelecionada = self.notaList.selection()

        if len(linhaSelecionada) != 0:
            id = self.notaList.item(linhaSelecionada[0])["values"][0]

            if  self.notaCRUD.excluir(id):
                self.notaList.delete(linhaSelecionada)
                
                mb.showinfo("Mensagem", "Exclusão executada com sucesso.")
                self.av1Edit.delete(0, tk.END)
                self.av2Edit.delete(0, tk.END)
                self.av3Edit.delete(0, tk.END)
                self.mediaEdit.delete(0, tk.END)
               
            else:
                mb.showinfo("Mensagem", "Erro na exclusão.")
                self.av1Edit.focus_set()
                self.av2Edit.focus_set()
                self.av3Edit.focus_set()
                self.mediaEdit.focus_set()
            



janela = tk.Tk()
principal = Notawin(janela)
janela.title("Cadastro de Aluno")
janela.geometry("950x650+0+0")
janela.configure(background="#292826")
imagem_ = ImageTk.PhotoImage(file="Art1.png")
Label=Label(janela,image=imagem_,bg='#292826',pady=0,).place(x=5,y=0,)
janela.iconbitmap("Artc.ico")
janela.mainloop()