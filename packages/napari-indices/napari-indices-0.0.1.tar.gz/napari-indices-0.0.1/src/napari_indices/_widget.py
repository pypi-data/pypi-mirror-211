"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QMainWindow
from napari.types import ImageData, LabelsData
#import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
import spectral
from napari import Viewer, layers
from napari.utils.notifications import show_info
#from napari_plugin_engine import napari_hook_implementation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtCore, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure



if TYPE_CHECKING:
    import napari




class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class ExampleQWidget(QMainWindow):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.cord1 = napari_viewer.layers['Shapes'].data[0]
        self.cord2 = napari_viewer.layers['Shapes'].data[1] 

        # Images de différents indices de végétation
        self.ndvi = napari_viewer.layers["NDVI"].data
        self.tcari = napari_viewer.layers["TCARI"].data
        self.npci = napari_viewer.layers["NPCI"].data
        self.sgi = napari_viewer.layers["SGI"].data
        self.ndgi = napari_viewer.layers["NDGI"].data
        
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        
        self.btn = QPushButton("Click me!")
        self.btn.clicked.connect(self.update_plot)
        layout.addWidget(self.btn)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()
        
    def update_plot(self):
        
        # Liste des images 
        I = [self.ndvi, self.tcari, self.npci, self.sgi, self.ndgi]

        # new data is plotted 
        self.sc.axes.cla()

        # Coordonnées limites de la région 1
        x1 = int(self.cord1[0][2])
        x2 = int(self.cord1[1][2])
        y1 = int(self.cord1[0][1])
        y2 = int(self.cord1[2][1])

        # Coordonnées limites de la région 2
        x3 = int(self.cord2[0][2])
        x4 = int(self.cord2[1][2])
        y3 = int(self.cord2[0][1])
        y4 = int(self.cord2[2][1])

        ratio = []
        indices_vegetation = ["NDVI", "TCARI", "NPCI", "SGI", "NDGI"]
        best_indice = None

        # Boucle pour calculer le RF de toutes les images
        for i, img in enumerate(I):
            region1 = img[y1:y2, x1:x2]
            region2 = img[y3:y4, x3:x4]
            
            # Valeurs moyennes
            mean1 = np.mean(region1)
            mean2 = np.mean(region2)
            
            # Écart type
            std1 = np.std(region1)
            std2 = np.std(region2)

            # Ratio de Fischer 
            RF = ((mean1 - mean2) ** 2) / (std1 ** 2 + std2 ** 2)
            ratio.append(RF)

            # Mise à jour de l'image correspondante au meilleur ratio de Fischer
            if best_indice is None or RF > ratio[best_indice]:
                best_indice = i
                best_region1 = region1
                best_region2 = region2

        RF_max = np.round(max(ratio), 2)
        best_indice = indices_vegetation[best_indice]

        self.sc.axes.hist(best_region1.flatten(), bins=50, color='blue', alpha=0.5, label='Région 1')
        self.sc.axes.hist(best_region2.flatten(), bins=50, color='green', alpha=0.5, label='Région 2')
        self.sc.axes.set_title(f"Histogrammes des deux régions.\nLe meilleur indice de végétation est: {best_indice} et son ratio de Fisher est: {RF_max}")
        #plt.legend()
        #plt.xlabel("Valeurs")
        #plt.ylabel("Fréquence")
        #plt.show()
            
       
        # canvas gets updated by redrawing (if this line is omitted, nothing gets updated
        self.sc.draw()





def indices(file):
    # Ouvrir le fichier
    img = tiff.imread(file)
    
     # Charger les informations sur les longueurs d'onde
    header = spectral.envi.read_envi_header(r'C:\Users\EMMANUELLA\Documents\vert_emmanuella_8600_us_2x_2023-04-25T153039_corr_rad.hdr')
    wavelengths = header['wavelength']
    
    # Nombre de bandes et dimensions de l'image
    b, h, w = img.shape
    
    # Affichage de toutes les bandes avec leurs longueurs d'onde
    for i in range(b):
       plt.imshow(img[i], cmap='gray')
       plt.title(f"Bande {i+1} - Longueur d'onde : {wavelengths[i]} nm")
       plt.axis('off')
       plt.show()
    
    # Demander à l'utilisateur de choisir les bandes
    while True:
       red_band = int(input("Sélectionnez la bande rouge (indice entre 1 et %d) : " % b))
       if red_band < 1 or red_band > b:
           print("Bande invalide. Veuillez réessayer.")
           continue
       else:
           break
   
    while True:
       nir_band = int(input("Sélectionnez la bande proche infra-rouge (indice entre 1 et %d) : " % b))
       if nir_band < 1 or nir_band > b:
           print("Bande invalide. Veuillez réessayer.")
           continue
       else:
           break
   
    while True:
       green_band = int(input("Sélectionnez la bande verte (indice entre 1 et %d) : " % b))
       if green_band < 1 or green_band > b:
           print("Bande invalide. Veuillez réessayer.")
           continue
       else:
           break
   
    while True:
       blue_band = int(input("Sélectionnez la bande bleue (indice entre 1 et %d) : " % b))
       if blue_band < 1 or blue_band > b:
           print("Bande invalide. Veuillez réessayer.")
           continue
       else:
           break
   
    # Extraire les bandes sélectionnées
    red = img[red_band - 1]
    nir = img[nir_band - 1]
    green = img[green_band - 1]
    blue = img[blue_band-1]
    
    # Demander à l'utilisateur de choisir un indice
    while True:
        indice = input("Choisissez un indice (NDVI, TCARI, NPCI, SGI, NDGI) : ")
        if indice not in ["NDVI", "TCARI", "NPCI", "SGI"]:
            print("Indice invalide. Veuillez réessayer.")
            continue
        else:
            break
    
    # Calculer et afficher l'indice choisi
    if indice == "NDVI":
        ndvi = calculate_ndvi(red, nir)
        return ndvi
    elif indice == "TCARI":
        tcari = calculate_tcari(red, green, blue)
        return tcari
    elif indice == "NPCI":
        npci = calculate_npci(red, green)
        return npci
    elif indice == "SGI":
        sgi = calculate_sgi(nir, red)
        return sgi
    elif indice == "NDGI":
        ndgi = calculate_ndgi(green, red)
        return ndgi

def calculate_ndvi(red, nir, image_viewer):
    # Calculer la NDVI
    ndvi = (nir - red) / (nir + red)
    
    # Retourner l'image de la NDVI
    return image_viewer.add_image(ndvi, name="NDVI")

def calculate_tcari(red, green, blue, image_viewer):
    # Calculer le TCARI
    tcari = 3 * ((red - green) - 0.2 * (red - blue))
    
    # Retourner l'image du TCARI
    return image_viewer.add_image(tcari, name="TCARI")

def calculate_npci(red, green,image_viewer):
    # Calculer le NPCI
    npci = (green - red) / (green + red)

    # Retourner l'image du NPCI
    return image_viewer.add_image(npci, name="NPCI")

def calculate_sgi(red, nir, image_viewer):
    # Calculer la SGI
    sgi = nir / red

    # Retourner l'image de la SGI
    return image_viewer.add_image(sgi, name="SGI")

def calculate_ndgi(green, red, image_viewer):
    # Calculer la NGVI
    ndgi = (green - red) / (green + red)
    
    # Retourner l'image de la NDGI
    return image_viewer.add_image(ndgi, name="NDGI")

@magic_factory(call_button="Run", dropdown = {"choices":["NDVI","TCARI","NPCI","SGI","NDGI"]})
def calculate_indice(image_layer: ImageData, image_viewer: Viewer, dropdown="NDVI", red_band: int = 0, nir_band: int = 0, green_band:int = 0, blue_band: int = 0) -> ImageData:
    
    ndvi = None
    tcari = None
    npci = None
    sgi= None
    ndgi = None

    if red_band == 0 or nir_band == 0 or blue_band == 0 or green_band == 0:
        print("select correct band")
    
    else:
        red = image_layer[red_band - 1,:,:]
        nir = image_layer[nir_band - 1,:,:]
        green = image_layer[green_band - 1,:,:]
        blue = image_layer[blue_band - 1,:,:]

    if dropdown == "NDVI":
        return calculate_ndvi(red, nir,image_viewer)
    if dropdown == "TCARI":
        return calculate_tcari(red, green, blue, image_viewer)
    if dropdown == "NPCI":
        return calculate_npci (red, green, image_viewer)
    if dropdown == "SGI":
        return calculate_sgi (nir, red, image_viewer)
    if dropdown == "NDGI":
        return calculate_ndgi (green, red, image_viewer)

    

"""    
@magic_factory(call_button="Run")
def ratio_fischer(image_viewer: Viewer):
    cord1 = image_viewer.layers["Shapes"].data[0] #cooordonnées de la région 1
    cord2 = image_viewer.layers["Shapes"].data[1] #cooordonnées de la région 2
    
    # images de différents indices de végétations
    ndvi = image_viewer.layers["NDVI"].data
    tcari = image_viewer.layers["TCARI"].data
    npci = image_viewer.layers["NPCI"].data

    # Liste des images 
    I=[ndvi, tcari,npci]

    #cooordonnées limites de la région 1
    x1 = int(cord1[0][2])
    x2 = int(cord1[1][2])
    y1 = int(cord1[0][1])
    y2 = int(cord1[2][1])


    #cooordonnées limites de la région 2
    x3 = int(cord2[0][2])
    x4 = int(cord2[1][2])
    y3 = int(cord2[0][1])
    y4 = int(cord2[2][1])

    ratio=[]
    indices_vegetation = ["NDVI", "TCARI", "NPCI"]
    best_indice = None

    # boucle pour calculer le RF de toutes les images
    for i, img in enumerate(I):
        region1 = img[y1:y2, x1:x2]
        region2 = img[y3:y4, x3:x4]
        
        # Valeurs moyennes
        mean1 = np.mean(region1)
        mean2 = np.mean(region2)
        
        # Ecart type
        std1 = np.std(region1)
        std2 = np.std(region2)

        # Ratio de Fischer 
        RF=((mean1-mean2)**2)/(std1**2+std2**2)
        ratio.append(RF)

        # Mise à jour de l'image correspondante au meilleur ratio de Fischer
        if best_indice is None or RF > ratio[best_indice]:
            best_indice = i
            best_region1 = region1
            best_region2 = region2

    RF_max = np.round(max(ratio), 2)
    best_indice = indices_vegetation[best_indice]

    # Création d'une nouvelle figure pour l'histogramme
    plt.figure()

    # Affichage de l'histogramme des deux régions du meilleur indice de végétation
    plt.hist(best_region1.flatten(), bins=50, color='blue', alpha=0.5, label='Région 1')
    plt.hist(best_region2.flatten(), bins=50, color='green', alpha=0.5, label='Région 2')
    plt.title("Histogrammes des deux régions")
    plt.legend()
    plt.xlabel("Valeurs")
    plt.ylabel("Fréquence")
    plt.show()
    
    show_info(f"Le meilleur indice de végétation est: {best_indice} et son ratio de Fisher est: {RF_max}" )

    return RF_max, best_indice"""