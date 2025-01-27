.global main
.text

# en 0: une valeur qui change entre 0 et 1 toutes les secs
# 8: sec, 16: min, 24: h, 32:jour  40:mois, 48:ans

main: 

#On commence à 0 pour le chronomètre
    li x1, 0
    sw x1, 8(x0)
    li x1, 0
    sw x1, 16(x0)
    li x1, 0
    sw x1, 24(x0)
    li x1, 0
    sw x1, 32(x0)
    li x1, 0
    sw x1, 40(x0)
    li x1, 0
    sw x1, 48(x0)

# on stock le mod 25 de l'année en x6
    li x6 0

verification: # boucle principale
    jal verification  


ajout_seconde: 
    addi x5, x1, 0 
    # si on est à 60s
    lw x1, 8(x0)
    li x2, 60  
    beq x2, x1 , ajout_minute 
    addi x1, x1, 1
    sw x1, 8(x0) #on stock les secondes en 8
    jal verification 


ajout_minute:
    #on remet les sec à 0
    sw x0, 8(x0)
    lw x1, 16(x0) 
    li x2, 60  
    beq x2, x1 , ajout_heure
    addi x1, x1, 1
    sw x1, 16(x0) #on stock les minutes en 2
    jal verification 

ajout_heure:
    #on remet les minutes à 0
    sw x0, 16(x0)
    lw x1, 24(x0) 
    li x2, 24  
    beq x2, x1 , ajout_jour 
    addi x1, x1, 1
    sw x1, 24(x0) #on stock les heures en 3
    jal verification 

ajout_jour:
    #on regarde le mois
    lw x1, 40(x0)
    li x2, 1 
    beq x2, x1, ajout_jour_31 
    li x2, 3 
    beq x2, x1, ajout_jour_31 
    li x2, 5 
    beq x2, x1, ajout_jour_31 
    li x2, 7
    beq x2, x1, ajout_jour_31 
    li x2, 8
    beq x2, x1, ajout_jour_31 
    li x2, 10 
    beq x2, x1, ajout_jour_31 
    li x2, 12 
    beq x2, x1, ajout_jour_31 
    li x2, 4
    beq x2, x1, ajout_jour_30
    li x2, 6
    beq x2, x1, ajout_jour_30
    li x2, 9
    beq x2, x1, ajout_jour_30
    li x2, 11
    beq x2, x1, ajout_jour_30
    #si c'est 2 il faut regarder l'année mod 4
    lw x2, 48(x0)
    andi x1, x2, 3 # si x1 = 0 l'année est 0 mod 4 
    andi x2, x2, 7 # si x2 = 0 l'année est 0 mod 8
    beq x1, x0, div_par_4
    
    jal ajout_jour_28  

div_par_4:
    beq x6, x0, div_par_100
    jal ajout_jour_29  

div_par_100:
    beq x2, x0, ajout_jour_29
    jal ajout_jour_28  

ajout_jour_31:
    #on remet les heures à 0
    sw x0, 24(x0)
    lw x1, 32(x0)
    li x2, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sw x1, 32(x0) #on stock les jours en 4
    jal verification 

ajout_jour_30:
    #on remet les heures à 0
    sw x0, 24(x0)
    lw x1, 32(x0)
    li x2, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sw x1, 32(x0) #on stock les jours en 4
    jal verification 

ajout_jour_29:
    #on remet les heures à 0
    sw x0, 24(x0)
    lw x1, 32(x0)
    li x2, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sw x1, 32(x0) #on stock les jours en 4
    jal verification 

ajout_jour_28:
    #on remet les heures à 0
    sw x0, 24(x0)
    lw x1, 32(x0)
    li x2, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sw x1, 32(x0) #on stock les jours en 4
    jal verification 


ajout_mois:
    #on remet les jours à 1
    li x1, 1 
    sw x1, 32(x0)
    lw x1, 40(x0) 
    li x2, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sw x1, 40(x0) #on stock les mois en 5
    jal verification 

ajout_ans:
    #on remet les mois à 1
    li x1, 1 
    sw x1, 40(x0)
    lw x1, 48(x0) 
    addi x1, x1, 1
    sw x1, 48(x0) #on stock les années en 6
    #on augment le mod 25
    addi x6, x6, 1
    li x2, 25
    bne x2, x6, pass
    li x6, 0
pass:
    jal verification 



ajout_seconde: 
    addi x5, x1, 0 
    # si on est à 60s
    lw x1, 8(x0)
    li x2, 60  
    beq x2, x1 , ajout_minute 
    addi x1, x1, 1
    sw x1, 8(x0) #on stock les secondes en 8
    jal verification 


ajout_minute:
    #on remet les sec à 0
    sw x0, 8(x0)
    lw x1, 16(x0) 
    li x2, 60  
    beq x2, x1 , ajout_heure
    addi x1, x1, 1
    sw x1, 16(x0) #on stock les minutes en 2
    jal verification 

ajout_heure:
    #on remet les minutes à 0
    sw x0, 16(x0)
    lw x1, 24(x0) 
    li x2, 24  
    beq x2, x1 , ajout_jour 
    addi x1, x1, 1
    sw x1, 24(x0) #on stock les heures en 3
    jal verification 

ajout_jour:
    #on regarde le mois
    lw x1, 40(x0)
    li x2, 1 
    beq x2, x1, ajout_jour_31 
    li x2, 3 
    beq x2, x1, ajout_jour_31 
    li x2, 5 
    beq x2, x1, ajout_jour_31 
    li x2, 7
    beq x2, x1, ajout_jour_31 
    li x2, 8
    beq x2, x1, ajout_jour_31 
    li x2, 10 
    beq x2, x1, ajout_jour_31 
    li x2, 12 
    beq x2, x1, ajout_jour_31 
    li x2, 4
    beq x2, x1, ajout_jour_30
    li x2, 6
    beq x2, x1, ajout_jour_30
    li x2, 9
    beq x2, x1, ajout_jour_30
    li x2, 11
    beq x2, x1, ajout_jour_30
    #si c'est 2 il faut regarder l'année mod 4
    lw x2, 48(x0)
    andi x2, x2, 3 # si x2 = 0 l'année est 0 mod 4 donc 29 jours
    beq x2, x0, ajout_jour_29
    jal ajout_jour_28  

ajout_jour_31:
    #on remet les heures à 0
    sw x0, 24(x0)
    lw x1, 32(x0)
    li x2, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sw x1, 32(x0) #on stock les jours en 4
    jal verification 

ajout_jour_30:
    #on remet les heures à 0
    sw x0, 24(x0)
    lw x1, 32(x0)
    li x2, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sw x1, 32(x0) #on stock les jours en 4
    jal verification 

ajout_jour_29:
    #on remet les heures à 0
    sw x0, 24(x0)
    lw x1, 32(x0)
    li x2, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sw x1, 32(x0) #on stock les jours en 4
    jal verification 

ajout_jour_28:
    #on remet les heures à 0
    sw x0, 24(x0)
    lw x1, 32(x0)
    li x2, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sw x1, 32(x0) #on stock les jours en 4
    jal verification 

ajout_mois:
    #on remet les jours à 1
    li x1, 1 
    sw x1, 32(x0)
    lw x1, 40(x0) 
    li x2, 31
    beq x2, x1 , ajout_mois
    addi x1, x1, 1
    sw x1, 40(x0) #on stock les mois en 5
    jal verification 

ajout_ans:
    #on remet les mois à 1
    li x1, 1 
    sw x1, 40(x0)
    lw x1, 48(x0) 
    addi x1, x1, 1
    sw x1, 48(x0) #on stock les années en 6
    jal verification 
