# Start coding here... 
import numpy as np
import pandas as pd

def encodeFormat(pos, lemme, imm, taille):
    new_pos = ""
    pos = str(pos)
    # 'ABR', -> abreviation
    # 'ADJ', -> adjectif (need to separate plu. and sing.)
    # 'ADV', -> adverbe
    # 'DET:ART', -> determinants articles
    # 'DET:POS', -> determinants possessifs
    # 'INT', -> interjection? eg euh
    # 'KON', -> conjonction? eg ou et
    # 'NAM', -> pays??
    # 'NOM', -> nom
    # 'NUM', -> numero
    # 'PRO:DEM', -> pronoms démonstratifs
    # 'PRO:IND', -> pronoms indéfinis
    # 'PRO:PER', -> pronoms personnels
    # 'PRO:POS', -> pronoms possessifs
    # 'PRO:REL', -> pronoms relatifs
    # 'PRP', -> prepositions
    # 'PRP:det', -> determinant contractes (eg des) consider as determinants
    # 'PUN',-> ??
    # 'VER:cond', -> verbe
    
    # unknown pos => PRP (preposition?), NAM, KON, INT (interdit?), NUM, PUN, remove nan?
    # sing vs plu adj.
    # will have to deal with PRO and PRO:PER in delattre function
    if pos == 'NOM':
        if imm == lemme:
            new_pos = "NOM_SING"
        else:
            new_pos = "NOM_PLU"
    elif pos == 'ADJ':
        if imm == lemme:
            new_pos = "ADJ_SING"
        else:
            new_pos = "ADJ_PLU"
    elif 'VER' in pos:
        new_pos = "VER"
    elif pos == 'PRP': # is PRP:det preposition??
        if taille == "mono":
            new_pos = "PRP_mono"
        else:
            new_pos = "PRP_poly"   
    elif pos == 'ADV': # is PRP:det preposition??
        if taille == "mono":
            new_pos = "ADV_mono"
        else:
            new_pos = "ADV_poly" 
    elif pos == 'KON': # is PRP:det preposition??
        if taille == "mono":
            new_pos = "KON_mono"
        else:
            new_pos = "KON_poly" 
    else:
        new_pos = pos
    return new_pos
    

def encodeFormatSimp(pos, lemme, imm):
    new_pos = ""
    pos = str(pos)
    #PRP:det in determinatifs
    #account for all adj as adj here
    if 'DET' in pos or 'det' in pos:
        new_pos = "DET"
    elif 'DET' in pos or 'det' in pos:
        new_pos = "DET"
    elif 'PRO' in pos or 'pro' in pos:
        new_pos = "PRO"
    else:
        new_pos = pos
    return new_pos


def delattre(row):
    liaison = "tbd"
    CD_lemme = row['CD_lemme']
    CG_lemme = row['CG_lemme']
    CG_imm = row['CG_imm']
    CD_imm = row['CD_imm']
    taille = row['taille']
    CD_pos_simp = encodeFormatSimp(row['CD_pos'], CD_lemme, CD_imm)
    CG_pos_simp = encodeFormatSimp(row['CG_pos'], CD_lemme, CD_imm)
    CD_pos_encoded = encodeFormat(row['CD_pos'], CD_lemme, CD_imm, taille)
    CG_pos_encoded = encodeFormat(row['CG_pos'], CG_lemme, CG_imm, taille)
    invariables = ['PRP', 'ADV', 'KON']
    
    # fix, make speciales its own function iterating through list seeing if each is in CG_full or CD_full
    CG_full = ' '.join(list(str(row['CG_full']).split(" "))[-2:] + [str(CD_imm)])
    CD_full = ' '.join([str(CG_imm)] + list(str(row['CD_full']).split(" "))[-2:])
    
    #make fix for OBG:
    # per + per + ver and ver + pers + pers
    # c'est (impersonnel) + [ask about impersonnel part]
    # il est (impersonnel) + [yet to implement]
    obligatoires_pos = [["DET:ART", "NOM_SING"], ["DET:ART", "NOM_PLU"], ["PRP:det", "NOM_SING"], ["PRP:det", "NOM_PLU"]] + [["PRO:PER", "VER"], ["VER", "PRO:PER"]]
                            
    obligatoires_pos_simp = [["DET", "PRO"], ["DET", "ADJ"], ["ADJ", "NOM"], ["NUM", "NOM"]]
    #incorporate accents into this list. also make sure caps are correct in data, else capitalize all vvv
    obligatoires_speciales = ["les Champs-Elysees", "les Etats-Unis", "comment allez-vous", "Mesdames et Messieurs", "un fait accompli", "un guet-apens", "un pied a terre", "pieds et poings lies", "ses faits et gestes", "monts et merveilles", "ponts et chaussees", "arts et metiers", "il etait une fois", "le pont aux anes", "de mieux en mieux", "de plus en plus", "de moins en moins", "de point en point", "du tout au tout", "de temps en temps", "de temps a autre", "de fond en comble", "de haut en bas", "de but en blanc", "d'un bout a l'autre", "tant et plus", "tout a coup", "tout a l'heure", "tout a fait", "tout au plus", "tout au moins", "tout au long", "mot a mot", "dos a dos", "pas a pas", "vis-a-vis", "petit a petit", "pot au feu", "pot aux roses", "pot au lait", "pot a eau", "sous-entendu", "sous-officier", "a bras ouverts", "avant-hier", "un pis aller", "accent aigu", "le cas echeant", "nuit et jour", "en temps utile"]
    
    
    facultatives_pos = [["NOM_PLU", "ADJ_PLU"], ["NOM_PLU", "VER"], ["NOM_PLU"]] #nom_plu +invariables?
    interdites_pos = [["NOM_SING", "ADJ_SING"], ["NOM_SING", "VER"]]
    interdites_speciales = ["nez a nez", "riz au lait", "pot a tabac", "pot a beurre", "chaud et froid", "a tort et a travers", "du Nord au Midi", "de part en part", "une fois ou l'autre", "au doigt et a l'oeil"]
    interdites_droites = ["oui", "un", "huit", "onze"]
    # save all types in list and loop over them to assign each to facultatives
    if [CG_pos_encoded, CD_pos_encoded] in obligatoires_pos or [CG_pos_simp, CD_pos_simp] in obligatoires_pos_simp or CG_imm.capitalize() == "C'EST" or CG_full.capitalize() == "IL EST" or (CG_pos_encoded == "PRP_mono") or (CG_pos_encoded == "ADV_mono") or (CG_full in obligatoires_speciales) or (CD_full in obligatoires_speciales):
        liaison = 'OBLIGATOIRES'
    elif [CG_pos_encoded, CD_pos_encoded] in facultatives_pos or (CG_pos_simp == "PRO" and CG_pos_encoded != 'PRO:PER') or CG_pos_encoded == 'PRP_poly' or CG_pos_encoded == 'ADV_poly' or CG_pos_encoded == 'KON_mono' or (CG_pos_encoded == 'NOM_PLU' and CD_pos_simp in invariables) or (CG_pos_encoded == "ADJ_PLU" and CD_pos_simp in invariables) or (CG_pos_simp == 'PRO' and CD_pos_simp in invariables) or (CG_pos_encoded == 'VER' and CD_pos_simp in invariables) or (CG_pos_encoded == 'ADV_poly' and CD_pos_simp in invariables) or CG_pos_encoded == "VER":
        liaison = 'FACULTATIVES'
    elif [CG_pos_encoded, CD_pos_encoded] in interdites_pos or (CG_pos_encoded == 'NOM_PLU' and CD_pos_simp in invariables) or CG_pos_encoded == 'NAM' or (CG_imm == 'on' and row['CD_pos'] == "VER:ppre")or (CG_imm == 'ils' and row['CD_pos'] == "VER:ppre") or (CG_imm == 'elles' and row['CD_pos'] == "VER:ppre") or CG_imm == 'et' or CG_pos_simp == 'ADV' or CD_lemme in interdites_droites or CG_pos_encoded == 'KON_poly' or (CG_pos_encoded == 'NOM_SING' and CD_pos_simp in invariables) or (CG_pos_encoded == 'ADJ_SING' and CD_pos_simp in invariables) or (CG_full in interdites_speciales) or (CD_full in interdites_speciales):
        liaison = 'INTERDITES'
    else:
        liaison = 'na'
    
    return liaison

