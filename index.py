from tkinter import *
import cv2 # type: ignore

# FUNÇÃO DE CENTRALIZAR JANELA
def centralizar(janelaTk):
    janelaTk.update_idletasks()

    width = janelaTk.winfo_width()
    frm_width = janelaTk.winfo_rootx() - janelaTk.winfo_x()
    janelaTk_width = width + 2 * frm_width

    height = janelaTk.winfo_height()
    titlebar_height = janelaTk.winfo_rooty() - janelaTk.winfo_y()
    janelaTk_height = height + titlebar_height + frm_width

    x = janelaTk.winfo_screenwidth() // 2 - janelaTk_width // 2
    y = janelaTk.winfo_screenheight() // 2 - janelaTk_height // 2

    janelaTk.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    janelaTk.deiconify()

def capturar():
    # PROPRIEDADES JANELAS WEBCAM
    janelaSemFiltro = "WEBCAM SEM DETECÇAO"
    janelaComFiltro = "WEBCAM COM DETECÇAO"
    cv2.namedWindow(janelaSemFiltro)
    cv2.namedWindow(janelaComFiltro)
    
    # OBJETO PARA CAPTURA DE VÍDEO
    video = cv2.VideoCapture(0)
    primeiroFrame = cv2.cvtColor(video.read()[1], cv2.COLOR_RGB2GRAY)
    segundoFrame = primeiroFrame
    terceiroFrame = primeiroFrame
    while(True): 
        # OBJETO DE FRAME DA WEBCAM
        ret, frame = video.read() 
        terceiroFrame = segundoFrame
        segundoFrame = primeiroFrame
        
        # INICIALIZAR JANELAS
        primeiroFrame = cv2.cvtColor(video.read()[1], cv2.COLOR_RGB2GRAY)
        
        # CALCULO DE DIFERENÇA ENTRE FRAMES
        diferenca1 = cv2.absdiff(terceiroFrame, segundoFrame)
        diferenca2 = cv2.absdiff(segundoFrame, primeiroFrame)
        diferencaFinal = cv2.bitwise_and(diferenca1,diferenca2)
        arg1,diferencaFinal = cv2.threshold(diferencaFinal, 60, 255, cv2.THRESH_BINARY)
         
        cv2.imshow(janelaComFiltro, diferencaFinal)
        cv2.imshow(janelaSemFiltro, frame)
        
        # TECLA PARA FINALIZAR EVENTO DE WEBCAM E REMOVER JANELA DA WEBCAM
        k=cv2.waitKey(30) & 0xFF
        if k == 27: 
            video.release()
            cv2.destroyWindow(janelaSemFiltro)
            cv2.destroyWindow(janelaComFiltro)   
            break

# OBJETO JANELA
janelaTk = Tk ()
        
# PROPRIEDADES DA JANELA
janelaTk.title('Projeto')
janelaTk.geometry('500x500+0+0')
bg='gray'
janelaTk['bg']=bg

label = Label(janelaTk, text = "Para Desligar a Detecção de Movimento Pressione 'Esc'.", bg=bg)
label.place(x=90, y=10, width=300, height=50)
bt = Button(janelaTk, width=30, text="Ligar Detector de Movimento", bg='red', activebackground='red', command=capturar)
bt.pack(side=RIGHT, padx=150, pady=150);

# CENTRALIZAR JANELA 
centralizar(janelaTk)

janelaTk.mainloop()
