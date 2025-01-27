

# en 0: une valeur qui change entre 0 et 1 toutes les secs
# 8: sec, 16: min, 24: h, 32:jour  40:mois, 48:ans

main: 
    ld x5, 0(x0) # on retient en x5 si on a un 0 ou un 1 

#il faut initialiser à l'heure de base stocké en 56,64,72,80,88,96

    ld x1, 56(x0)
    sd x1, 8(x0)
    ld x1, 64(x0)
    sd x1, 16(x0)
    ld x1, 72(x0)
    sd x1, 24(x0)
    ld x1, 80(x0)
    sd x1, 32(x0)
    ld x1, 88(x0)
    sd x1, 40(x0)
    ld x1, 96(x0)
    sd x1, 48(x0)

# on stock le mod 25 de l'année en x6
    addi x6, x0, 0

verification: # vérifie si on change de seconde
    ld x1, 0(x0)
    bne x5, x1, ajout_seconde 
    jal x0, verification  # 


ajout_seconde: 
    addi x5, x1, 0 
    # si on est à 60s
    ld x1, 8(x0)
    addi  x2, x0, 60  
    beq x2, x1 , ajout_minute 
    addi x1, x1, 1
    sd x1, 8(x0) #on stock les secondes en 8
    jal x0, verification 


ajout_minute:
    #on remet les sec à 0
    sd x0, 8(x0)
    ld x1, 16(x0) 
    addi  x2, x0, 60  
    beq x2, x1 , ajout_heure
    addi x1, x1, 1
    sd x1, 16(x0) #on stock les minutes en 2
    jal x0, verification 

ajout_heure:
    #on remet les minutes à 0
    sd x0, 16(x0)
    ld x1, 24(x0) 
    addi  x2, x0, 24  
    beq x2, x1 , ajout_jour 
    addi x1, x1, 1
    sd x1, 24(x0) #on stock les heures en 3
    jal x0, verification 

ajout_jour:
    #on regarde le mois
    ld x1, 40(x0)
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
    ld x2, 48(x0)
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
    sd x0, 24(x0)
    ld x1, 32(x0)
    addi  x2, x0, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sd x1, 32(x0) #on stock les jours en 4
    jal x0, verification 

ajout_jour_30:
    #on remet les heures à 0
    sd x0, 24(x0)
    ld x1, 32(x0)
    addi  x2, x0, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sd x1, 32(x0) #on stock les jours en 4
    jal x0, verification 

ajout_jour_29:
    #on remet les heures à 0
    sd x0, 24(x0)
    ld x1, 32(x0)
    addi  x2, x0, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sd x1, 32(x0) #on stock les jours en 4
    jal x0, verification 

ajout_jour_28:
    #on remet les heures à 0
    sd x0, 24(x0)
    ld x1, 32(x0)
    addi  x2, x0, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sd x1, 32(x0) #on stock les jours en 4
    jal x0, verification 


ajout_mois:
    #on remet les jours à 1
    addi  x1, x0, 1 
    sd x1, 32(x0)
    ld x1, 40(x0) 
    addi  x2, x0, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sd x1, 40(x0) #on stock les mois en 5
    jal x0, verification 

ajout_ans:
    #on remet les mois à 1
    addi  x1, x0, 1 
    sd x1, 40(x0)
    ld x1, 48(x0) 
    addi x1, x1, 1
    sd x1, 48(x0) #on stock les années en 6
    #on augment le mod 25
    addi x6, x6, 1
    addi  x2, x0, 25
    bne x2, x6, pass
    addi  x6, x0, 0
pass:
    jal x0, verification 
