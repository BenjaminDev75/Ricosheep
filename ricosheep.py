import fltk
import fonction

fenx = 1080
feny = fenx /(16/9)

fltk.cree_fenetre(fenx, feny, frequence=60)

fonction.fen_princ(fenx)
Play = True
Retour = True
Choix = True
Start = True
Game = True
Reload = True
Next = True 
Annuler = True
Solu = True
niv = 0

histmout = []

move = ["Left","Up","Down","Right"]
menu = ["Escape","r","R","space","s","S"]
maps = ["D:\Document\Projet_Ricosheep\maps\square\map1.txt","maps\square\map2.txt","maps\square\map3.txt","maps\wide\wide1.txt",
        "maps\wide\wide2.txt","maps\wide\wide3.txt","maps\wide\wide4.txt","maps/big/big1.txt","maps/big/big2.txt",
        "maps/big/big3.txt","maps/big\huge.txt","maps/theme\one_sheep.txt","maps/theme\one_sheep2.txt","maps/theme\onegrass.txt"]

while True:
    ev = fltk.donne_ev()
    tev = fltk.type_ev(ev)

    moity = feny/2
    moitx = fenx/2
    moityplay = feny/3.7
    cranx = fenx/80
    crany = feny/80
    longplay, hautplay = fltk.taille_texte("Play", "Calibri", 
                                           int((cranx*5))) 
    longplay2, hautplay2 = fltk.taille_texte("Play", "Calibri", 
                                                 int((cranx*5)))
    if tev == 'ClicGauche':
        if Play :
            if moitx - longplay//2 - cranx*5 < fltk.abscisse(ev) < moitx + longplay//2 + cranx*5 and moity - crany*12 - hautplay//2< fltk.ordonnee(ev) < moity - crany*8 + hautplay//2:           
                fltk.efface_tout()
                fonction.menu_start(fenx,niv)
                Start = False
                Choix = False
                Retour = True
                Reload = True
 
        if not Choix:
            if fenx * 0.3 - fenx * 0.03  < fltk.abscisse(ev) < fenx * 0.3 + fenx * 0.03 and  2 * feny // 5.5 - fenx * 0.03 < fltk.ordonnee(ev) < 2 * feny // 5.5 + fenx * 0.03:
                if niv > 0:
                    niv -= 1
                fltk.efface("niv")
                fonction.niveau(fenx,5.5,0.5,niv)
    
            if fenx * 0.7 - fenx * 0.03 < fltk.abscisse(ev) < fenx * 0.7 + fenx * 0.03 and  2 * feny // 5.5 - fenx * 0.03 < fltk.ordonnee(ev) < 2 * feny // 5.5 + fenx * 0.03:
                if niv < 13:
                    niv += 1
                fltk.efface("niv")
                fonction.niveau(fenx,5.5,0.5,niv)

        if not Start :
            if moitx - longplay2 //2 - cranx*2 <fltk.abscisse(ev)< moitx + longplay2//2 + cranx*2 and moityplay - crany*12 - hautplay2//2 <fltk.ordonnee(ev)< moityplay - crany*8 + hautplay2//2 :        
                fltk.ferme_fenetre()
                moutons,plateau = fonction.charger(maps[niv])
                histmout = [moutons]
                fenx,feny= fonction.resolution(fenx,feny,plateau)
                fltk.cree_fenetre(fenx,feny)
                fltk.efface_tout()
                fonction.grille(moutons,plateau)
                Play = False
                Retour = False
                Choix = True
                Start = True
                Game = False
                Reload = False
                Next = True
                Annuler = False
                Solu = False

    if not Game:   
        if tev == "Touche" and fltk.touche(ev) in move:
            fltk.efface_tout()
            moutons = fonction.deplacer(plateau,moutons,fltk.touche(ev))
            fonction.grille(moutons,plateau)
            fonction.victoire2(plateau,moutons)
            fonction.solvmin(plateau,moutons)
            if moutons not in histmout:
                histmout.append(moutons)
            if fonction.victoire2(plateau,moutons) == True:
                fonction.affiche_victoire(fenx)
                Play = False
                Retour = False 
                Choix = True
                Reload = True
                Next = False
                Game = True
                Annuler = True

    if not Retour:
        if tev == "Touche" and fltk.touche(ev) in menu:
            if fltk.touche(ev) == "Escape":
                fltk.ferme_fenetre()
                fenx = 1080
                feny = fenx /(16/9)
                fltk.cree_fenetre(fenx, feny, frequence=60)
                fonction.menu_start(fenx,niv)
                Play = True
                Retour = True
                Choix = False
                Start = False
                Reload = True

    if not Reload:
        if tev == 'Touche' and fltk.touche(ev) in menu:
            if fltk.touche(ev) == "r" or fltk.touche(ev) == "R":
                fltk.efface_tout()
                moutons,plateau = fonction.charger(maps[niv])
                fonction.grille(moutons,plateau)
                Play = False

    if not Annuler:
        if tev == 'Touche' and fltk.touche(ev) == "BackSpace":
            if len(histmout) > 1:
                histmout.pop()
                moutons = histmout[-1]
                fltk.efface_tout()
                fonction.grille(moutons,plateau)

    if not Next:
        if tev == 'Touche' and fltk.touche(ev) in menu:
            if fltk.touche(ev) == 'space':
                niv +=1
                if niv < 14:
                    fltk.ferme_fenetre()
                    moutons,plateau = fonction.charger(maps[niv])
                    histmout = [moutons]
                    fenx,feny= fonction.resolution(fenx,feny,plateau)
                    fltk.cree_fenetre(fenx,feny)  
                    fltk.efface_tout()
                    fonction.grille(moutons,plateau)
                    Play = False
                    Choix = True
                    Reload = False
                    Game = False
                    Annuler = False
                    Next = True
                else:
                    fltk.ferme_fenetre()
                    fenx = 1080
                    feny = fenx /(16/9)
                    niv = 0
                    fltk.cree_fenetre(fenx, feny, frequence=60)
                    fonction.menu_start(fenx,niv)
                    Play = False
                    Start = False
                    Reload = True
                    Choix = False
                    Game = True
                    Next = True
                    Annuler= True

    if not Solu:
        if tev == 'Touche' and fltk.touche(ev) in menu:
            if fltk.touche(ev) == "s" or fltk.touche(ev) == "S":
                print(fonction.solvmin(plateau,moutons))

    if tev == 'Quitte':
        break
    fltk.mise_a_jour()

fltk.ferme_fenetre()