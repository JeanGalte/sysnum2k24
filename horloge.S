main: 
    gtck x5 # on retient en x5 si on a un 0 ou un 1 

# on stock le mod 25 de l'année en x6
#il faut l'initialiser

    addi x6, x0, 0 
    gyear x1 
    addi x2, x0, 25 
compte_mod25:
    addi x6, x6, 1
    addi x1, x1, -1
    bne x6, x2, passe_25
    addi x6, x0, 0
passe_25:
    beq x1, x0, fin_25
    jal x0, compte_mod25
fin_25:

verification: # vérifie si on change de seconde
    gtck x1
    bne x5, x1, ajout_seconde 
    jal x0, verification  

ajout_seconde: 
    addi x5, x1, 0 
    # si on est à 60s
    gsec x1
    addi  x2, x0, 60  
    beq x2, x1 , ajout_minute 
    addi x1, x1, 1
    ssec x1 
    jal x0, verification 


ajout_minute:
    #on remet les sec à 0
    ssec x0
    gmin x1
    addi  x2, x0, 60  
    beq x2, x1 , ajout_heure
    addi x1, x1, 1
    smin x1 
    jal x0, verification 

ajout_heure:
    #on remet les minutes à 0
    smin x0
    ghour x1 
    addi  x2, x0, 24  
    beq x2, x1 , ajout_jour 
    addi x1, x1, 1
    shour x1 
    jal x0, verification 

ajout_jour:
    #on regarde le mois
    gmon x1
    addi  x2, x0, 1 
    beq x2, x1, ajout_jour_31 
    addi  x2,x0, 3 
    beq x2, x1, ajout_jour_31 
    addi  x2, x0, 5 
    beq x2, x1, ajout_jour_31 
    addi  x2, x0, 7
    beq x2, x1, ajout_jour_31 
    addi  x2, x0, 8
    beq x2, x1, ajout_jour_31 
    addi  x2, x0, 10 
    beq x2, x1, ajout_jour_31 
    addi  x2, x0, 12 
    beq x2, x1, ajout_jour_31 
    addi  x2, x0, 4
    beq x2, x1, ajout_jour_30
    addi  x2, x0, 6
    beq x2, x1, ajout_jour_30
    addi  x2, x0, 9
    beq x2, x1, ajout_jour_30
    addi  x2, x0, 11
    beq x2, x1, ajout_jour_30
    #si c'est 2 il faut regarder l'année mod 4
    gyear x2
    andi x1, x2, 3 # si x1 = 0 l'année est 0 mod 4 
    andi x2, x2, 7 # si x2 = 0 l'année est 0 mod 8
    beq x1, x0, div_par_4
    
    jal x0, ajout_jour_28  

div_par_4:
    beq x6, x0, div_par_100
    jal x0, ajout_jour_29  

div_par_100:
    beq x2, x0, ajout_jour_29
    jal x0, ajout_jour_28  

ajout_jour_31:
    #on remet les heures à 0
    shour x0
    gday x1
    addi  x2, x0, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sday x1
    jal x0, verification 

ajout_jour_30:
    #on remet les heures à 0
    shour x0
    gday x1
    addi  x2, x0, 30
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sday x1
    jal x0, verification 

ajout_jour_29:
    #on remet les heures à 0
    shour x0
    gday x1
    addi  x2, x0, 29
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sday x1
    jal x0, verification 

ajout_jour_28:
    #on remet les heures à 0
    shour x0
    gday x1
    addi  x2, x0, 28
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sday x1
    jal x0, verification 

ajout_mois:
    #on remet les jours à 1
    addi  x1, x0, 1 
    sday x1
    gmon x1
    addi  x2, x0, 13
    beq x2, x1 , ajout_ans
    addi x1, x1, 1
    smon x1
    jal x0, verification 

ajout_ans:
    #on remet les mois à 1
    addi  x1, x0, 1 
    smon x1
    gyear x1
    addi x1, x1, 1
    syear x1 #on stock les années en 6
    #on augment le mod 25
    addi x6, x6, 1
    addi  x2, x0, 25
    bne x2, x6, pass
    addi  x6, x0, 0
pass:
    jal x0, verification 
