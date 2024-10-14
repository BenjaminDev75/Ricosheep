import fltk

#=======================================JEU======================================

def charger(fichier):
    """
    Charge le fichier du niveau séléctioné en renvoyant un couple de liste
    (moutons,plateau).
    
    :Paramètre moutons: Position des moutons 
    :Paramètre plateau: Taille du plateau, position des buissons et des herbes
    :Type: int
    """
    G = []
    moutons = []
    valide = "BG"
    f = open(fichier)
    lignes = f.readlines()
    for i in range(len(lignes)):
        lignes[i] = lignes[i].replace("\n", "")
    for i in range(len(lignes)):
        gtemp = []
        for j in range (len(lignes[i])):
            charact = lignes[i][j]
            if charact == "S":
                moutons.append((i,j))
            if charact in valide:
                gtemp.append(charact)
            elif charact == '_' or 'S':
                gtemp.append(None)
            else:
                return None
        G.append(gtemp)
    return moutons ,G


def deplacer(plateau2, moutons, direct):
    """
    Deplace le mouton dans la direction voulu par l'utilisateur
    
    :Paramètre moutons: Position des moutons 
    :Paramètre plateau: Taille du plateau, position des buissons et des herbes
    :Paramètre direct: Direction choisi
    :Type: int,str
    """
    plateau = []
    for a in plateau2:
        plateau.append(a.copy())
    newsheep = []
    if direct == "Right":
        for lmout, colmout in moutons:
            ligneact = plateau[lmout]
            moutons = 0
            coltemp = colmout
            while ligneact[coltemp] == "S":
                coltemp -= 1
                moutons += 1
            colmout += 1
            while colmout < len(ligneact) and ligneact[colmout] != "B":
                if ligneact[colmout] == "S":
                    moutons += 1
                colmout += 1
            colmout -= 1
            newsheep.append((lmout, colmout - moutons))
            ligneact[colmout - moutons] = "S"

        return newsheep

    if direct == "Left":
        for lmout, colmout in moutons:
            moutons = 0
            coltemp = colmout
            while plateau[lmout][coltemp] == "S":
                coltemp += 1
                moutons += 1
            colmout -= 1
            while colmout >= 0 and plateau[lmout][colmout] != "B":
                if plateau[lmout][colmout] == "S":
                    moutons += 1
                colmout -= 1
            colmout += 1
            newsheep.append((lmout, colmout + moutons))
            plateau[lmout][colmout + moutons] = "S"

        return newsheep

    if direct == "Down":
        for lmout, colmout in moutons:
            moutons = 0
            moutemp = lmout
            while plateau[moutemp][colmout] == "S":
                moutemp -= 1
                moutons += 1
            lmout += 1
            while lmout < len(plateau) and plateau[lmout][colmout] != "B":
                if plateau[lmout][colmout] == "S":
                    moutons += 1
                lmout += 1
            lmout -= 1
            newsheep.append((lmout - moutons, colmout))
            plateau[lmout - moutons][colmout] = "S"
 
        return newsheep
            
    if direct == "Up":
        for lmout, colmout in moutons:
            moutons = 0
            moutemp = lmout
            while plateau[moutemp][colmout] == "S":
                moutemp += 1
                moutons += 1
            lmout -= 1
            while lmout >= 0 and plateau[lmout][colmout] != "B":
                if plateau[lmout][colmout] == "S":
                    moutons += 1
                lmout -= 1
            lmout += 1
            newsheep.append((lmout + moutons, colmout))
            plateau[lmout + moutons][colmout] = "S"

        return newsheep

def victoire2(plateau,moutons):
    """
    Détecte si le joueur a gagné ou non en vérifiant si un mouton est présent dans chaque herbe
    
    :Paramètre moutons: Position des moutons 
    :Paramètre plateau: Taille du plateau, position des buissons et des herbes
    :Type: int
    """
    for a in range(len(plateau)): 
        for i in range( len(plateau[a])):

            if plateau[a][i] == 'G':
                nb_S = 0
                for mout in moutons:
                    if mout != (a, i):
                        nb_S += 1
                if nb_S == len(moutons):
                    return False            
    return True

def moutstr (moutons):
    moustr = ""
    for a in moutons:
        moustr += str(a)
    moustr = moustr.replace("(","").replace(")","").replace(",","").replace(" ","")
    return moustr

def victoireliste (plateau,moutlist):
    """
    Verifie si il existe une combinaison gagnable dans la partie en cours
    
    :Paramètre moutons: Position des moutons 
    :Paramètre plateau: Taille du plateau, position des buissons et des herbes
    :Type: int
    """
    
    ct = 0
    for a in plateau:
        nb = a.count("G")
        ct+= nb
    for moutons in moutlist:
        cpt = 0
        for mout in moutons:
            lin, col = mout
            if plateau[lin][col] == "G":
                cpt+= 1
        if cpt == ct:
            return moutstr(moutons)
    return False

def solvmin(plateau, moutons):
    """
    Solveur du jeu, affiche la solution au joueur dans le terminal
    :Paramètre plateau: Taille du plateau, position des buissons et des herbes
    :Paramètre moutons: Position des moutons 
    :Type: int
    """
    
    Lmouv = {moutstr(moutons) : ""}
    Lmoutprec = [moutons]
    mouv = ["Left","Right","Up","Down"]
    test = victoireliste(plateau,Lmoutprec)
    while test == False:
        Lmout = []
        for mou in Lmoutprec:
            for dir in mouv:
                nvmout =deplacer(plateau,mou,dir)
                strmout = moutstr(nvmout)
                if strmout not in Lmouv.keys():
                    Lmout.append(nvmout)
                    Lmouv[strmout] = Lmouv[moutstr(mou)] + " " + dir
        if Lmout == []:
            return None
        Lmoutprec = Lmout
        test = victoireliste(plateau,Lmoutprec)
    chemin = Lmouv[test].split(" ")
    chemin.pop(0)
    return chemin

def grille(moutons,plateau):
    """
    Création du plateau et affichage graphique de celui-ci
    
    :Paramètre moutons: Position des moutons 
    :Paramètre plateau: Taille du plateau, position des buissons et des herbes
    :Type: int
    """
    
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            fltk.rectangle(j*100,i*100,(j+1)*100,(i+1)*100)
            if plateau[i][j] == None:
                fltk.rectangle(j*100,i*100,(j+1)*100,(i+1)*100)
            if (i,j) in moutons:
                fltk.image((j+0.5)*100,(i+0.5)*100,'media\sheep.png')
            if plateau[i][j] == 'G':
                fltk.image((j+0.5)*100,(i+0.4)*100,'media\grass.png',ancrage='center')
            if plateau[i][j] == 'B':
                fltk.image((j+0.5)*100,(i+0.5)*100,'media\\bush.png')
    return

def resolution(fenx,feny,plateau):
    """
    Change la résolution de la fenêtre en fonction du plateau
    
    :Paramètre fenx: Taille de fenêtre
    :Paramètre feny: Taille de fenêtre
    :Paramètre plateau: Niveau choisi
    :Type: int
    """
    feny = len(plateau)
    fenx = len(plateau[0])
    return fenx*100, feny*100

#================================================================================





#====================================GRAPHIQUE===================================


def niveau(fenx,h=5.5,l=0.5,niv=1):
    
    feny = int( fenx / (16/9))
    police="Calibri"
    taille = feny // 14
    maps = ["Map 1", "Map 2", "Map 3", "Wide 1", "Wide 2", "Wide 3", "Wide 4", "Big 1", "Big 2", "Big 3", "Huge", "One Sheep", "One Sheep 2", "One Grass"]
    fltk.texte(fenx * l, 2 * feny // h, maps[niv],
            police="Calibri", couleur="black",
            ancrage='center', taille = taille, tag = "niv")

    longueur, hauteur = fltk.taille_texte(('Niveau '+str(niv+1)), police, taille)
    fltk.rectangle(fenx * (l-0.1) - fenx * 0.045 , 1.95 * feny // h - fenx * 0.03,
              fenx * (l+0.1) + fenx * 0.045, 2.05 * feny // h + fenx * 0.03,
              couleur="black", epaisseur = fenx/(fenx/2))

def bouton_plus(fenx,h=5.5,l=0.7):
    """
    Création du bouton "+"
    Utilisation: Choisir le niveau suivant dans le menu choix du niveau 
    
    :Paramètre fenx: Taille de fenêtre
    :Type: int
    """
    feny = int( fenx / (16/9))
    chaine = '>'
    police="Calibri"
    taille = feny // 14
    fltk.texte(fenx * l, 2 * feny // h, chaine,
            police="Calibri", couleur="black",
            ancrage='center', taille = taille )
    
    longueur, hauteur = fltk.taille_texte(chaine, police, taille)
    fltk.rectangle(fenx * l - fenx * 0.03 , 2 * feny // h - fenx * 0.03,
            fenx * l + fenx * 0.03, 2 * feny // h + fenx * 0.03,
            couleur="black", epaisseur = fenx/(fenx/2))

def bouton_moins(fenx,h=5.5,l=0.3):
    """
    Création du bouton "-"
    Utilisation: Choisir le niveau précédent dans le menu choix du niveau
    
    :Paramètre fenx: Taille de fenêtre
    :Type: int
    """
    feny = int( fenx / (16/9))
    chaine = '<'
    police="Calibri"
    taille = feny // 14
    fltk.texte(fenx * l, 2 * feny // h, chaine,
            police="Calibri", couleur="black",
            ancrage='center', taille = taille )
    
    longueur, hauteur = fltk.taille_texte(chaine, police, taille)
    fltk.rectangle(fenx * l - fenx * 0.03 , 2 * feny // h - fenx * 0.03,
            fenx * l + fenx * 0.03, 2 * feny // h + fenx * 0.03,
            couleur="black", epaisseur = fenx/(fenx/2))

def start(fenx):
    """
    Boutton qui sert à lancer le jeu une fois le niveau choisie
    
    :Paramètre fenx: Taille de fenêtre
    :Type: int
    """
    feny = fenx / (16/9)
    moity = feny/3.7
    moitx = fenx/2
    cranx = fenx/80
    crany = feny/80
    chaine = "Start"
    police = "Calibri"
    taille = int((cranx*5))
    fltk.texte(moitx, moity - crany*10 , chaine,
          police=police, taille=taille, couleur="black",
          ancrage='center')

def fen_princ(fenx):
    """
    Affichage du boutton "Play" au lancement du jeu 
    
    :Paramètre fenx: Taille de fenêtre
    :Type: int
    """
    feny = fenx / (16/9)
    moity = feny/2
    moitx = fenx/2
    cranx = fenx/80
    crany = feny/80
    chaine = "Play"
    police = "Calibri"
    taille = int((cranx*5))
    fltk.texte(moitx, moity - crany*10 , chaine,
          police=police, taille=taille, couleur="black",
          ancrage='center')
    
    longueur, hauteur = fltk.taille_texte(chaine, police, taille)
    fltk.rectangle(moitx - longueur//2 - cranx*2,moity - crany*12 - hauteur//2,
                   moitx + longueur//2 + cranx*2, moity - crany*8 + hauteur//2,
                   couleur="black", epaisseur = fenx/(fenx/3))

def affiche_victoire(fenx):
    """
    Affiche le message "You Win" si le joueur a gagné la partie
    
    :Paramètre fenx: Taille de fenêtre
    :Type: int
    """
    feny = fenx / (16/9)
    moity = feny/2
    moitx = fenx/2
    cranx = fenx/80
    crany = feny/80
    fltk.texte(moitx, moity - crany*10 , "You Win",
          police="Calibri", taille=int((cranx*5)), couleur="black",
          ancrage='center')
    
    longueur, hauteur = fltk.taille_texte("You Win", "Calibri", int((cranx*5)))
    fltk.rectangle(moitx - longueur//2 - cranx*2,moity - crany*12 - hauteur//2,
                   moitx + longueur//2 + cranx*2, moity - crany*8 + hauteur//2,
                   couleur="black", epaisseur = fenx/(fenx/3))
    
    moity = feny/0.8
    moitx = fenx/2
    
    fltk.texte(moitx, moity - crany*10 , "Espace pour le prochain niveau",
          police="Calibri", taille=int((cranx*3)), couleur="black",
          ancrage='center')
    
    longueur2, hauteur2 = fltk.taille_texte("Espace pour le prochain niveau",
                                          "Calibri", int((cranx*3)))
    fltk.rectangle(moitx - longueur2//2 - cranx*2,moity - crany*12 - hauteur2//2,
                   moitx + longueur2//2 + cranx*2, moity - crany*8 + hauteur2//2,
                   couleur="black", epaisseur = fenx/(fenx/3))


def menu_start(fenx,niv):
    """
    Fonction qui affiche le menu du choix de niveau
    
    :Paramètre fenx: Taille de fenêtre
    :Paramètre niv: Numéro du niveau
    :Type: int
    """
    feny = fenx / (16/9)
    niveau(fenx,5.5,0.5,niv)
    bouton_moins(fenx)
    bouton_plus(fenx)
    start(fenx)

#================================================================================