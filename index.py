from tkinter import *
import cv2 
import numpy as np


#FUNÇÃO LIMIAR
def limiar(img):   
  img_res = np.zeros(img.shape)
  limiar = 30
  
  for x in range(img.shape[0]):
    for y in range(img.shape[1]):
      if img[x,y] > limiar:
        img_res[x,y] = 255
      else:
        img_res[x,y] = 0
  return img_res


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
    janelaSemFiltro = "WEBCAM SEM DETECCAO"
    janelaComFiltro = "WEBCAM COM DETECCAO"
    cv2.namedWindow(janelaSemFiltro)
    cv2.namedWindow(janelaComFiltro)
    
    # OBJETO PARA CAPTURA DE VÍDEO
    video = cv2.VideoCapture(0)
    primeiroFrame = cv2.cvtColor(video.read()[1], cv2.COLOR_RGB2GRAY)
    segundoFrame = primeiroFrame
    terceiroFrame = primeiroFrame
    while(True): 
        # OBJETO DE FRAME DA WEBCAM
        arg1, frame = video.read() 
        terceiroFrame = segundoFrame
        segundoFrame = primeiroFrame
        
        # INICIALIZAR JANELAS
        primeiroFrame = cv2.cvtColor(video.read()[1], cv2.COLOR_RGB2GRAY)
        
        # CALCULO DE DIFERENÇA ENTRE FRAMES
        diferenca1 = cv2.absdiff(terceiroFrame, segundoFrame)
        diferenca2 = cv2.absdiff(segundoFrame, primeiroFrame)
        diferencaFinal = cv2.bitwise_and(diferenca1,diferenca2)
        
        diferencaFinal = limiar(diferencaFinal)
        imgDeContorno = diferencaFinal.astype(np.uint8)
        achandoContorno,aux = cv2.findContours(image = imgDeContorno, mode = cv2.RETR_TREE, method =cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image = frame, contours = achandoContorno, contourIdx = -1, color = (255,150,0), thickness = 3, lineType = cv2.LINE_AA)
        
        cv2.imshow(janelaComFiltro, diferencaFinal)
        cv2.imshow(janelaSemFiltro, frame)
        
        # TECLA PARA FINALIZAR EVENTO DE WEBCAM E REMOVER JANELA DA WEBCAM
        k=cv2.waitKey(30) & 0xFF
        if k == 27: 
            video.release()
            cv2.destroyWindow(janelaSemFiltro)
            cv2.destroyWindow(janelaComFiltro)   
            break

def capturarCor():
  camera = cv2.VideoCapture(0)
  while True:
    # OBJETO PARA CAPTURA DE VÍDEO
    arg1, frame = camera.read()
    
    # CONVERTE O FRAME PARA HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # MASCARA PARA CAPTURAR O INTERVALO DO CÓDIGO HSV, EM MÍNIMO E MÁXIMO
    mascara = cv2.inRange(hsv, (23, 59, 119), (54, 255, 255))

    # BUSCAR CONTORNO
    contorno = cv2.findContours(mascara, cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    if len(contorno) > 0:
        
      # DESENHAR CIRCULO EM VOLTA DO OBJETO IDENTIFICADO
      c = max(contorno, key=cv2.contourArea)
      ((x, y), radius) = cv2.minEnclosingCircle(c)
      cv2.circle(frame, (int(x), int(y)),
      int(radius), (0, 255, 217), 2)
          
    cv2.imshow("Frame", frame)
    
    # TECLA PARA FINALIZAR EVENTO DE WEBCAM E REMOVER JANELA DA WEBCAM
    k=cv2.waitKey(30) & 0xFF
    if k == 27: 
        camera.release()
        cv2.destroyAllWindows()
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
bt = Button(janelaTk, width=30, text="Ligar Detector de Movimento", bg='white', activebackground='white', command=capturar)
bt.pack(side=RIGHT, padx=150, pady=150)

bt2 = Button(janelaTk, width=27, text="Ligar Detector de Cor", bg='white', activebackground='white', command=capturarCor)
bt2.place(x=150, y=300) 

# CENTRALIZAR JANELA 
centralizar(janelaTk)

janelaTk.mainloop()
