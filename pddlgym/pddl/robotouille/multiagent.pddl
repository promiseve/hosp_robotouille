(define (problem robotouille)
(:domain robotouille)
(:objects
    hospital_cart_left1 - station
    table1 - station
    patient_legs1 - station
    patient_bed_station1 - station
    hospital_cart_right1 - station
    table2 - station
    cpr_kit1 - item
    pump1 - item
    aed1 - item
    patient1 - item
    syringe1 - item
    cpr_board1 - item
    robot1 - player
    robot2 - player
    robot3 - player
    robot4 - player
)
(:init
    (ishospital_cart_left hospital_cart_left1)
    (istable table1)
    (ispatient_legs patient_legs1)
    (ispatient_bed_station patient_bed_station1)
    (ishospital_cart_right hospital_cart_right1)
    (istable table2)
    (iscpr_kit cpr_kit1)
    (isusableforcpr cpr_kit1)
    (ispump pump1)
    (isaed aed1)
    (isusableforaed aed1)
    (ispatient patient1)
    (ispatient patient1)
    (issyringe syringe1)
    (iscpr_board cpr_board1)
    (iscpr_boardusuable cpr_board1)
    (isrobot robot1)
    (isrobot robot2)
    (isrobot robot3)
    (isrobot robot4)
    (at pump1 hospital_cart_left1)
    (vacant hospital_cart_left1)
    (at aed1 table1)
    (vacant table1)
    (empty patient_legs1)
    (vacant patient_legs1)
    (at patient1 patient_bed_station1)
    (vacant patient_bed_station1)
    (at syringe1 hospital_cart_right1)
    (loc robot3 hospital_cart_right1)
    (at cpr_board1 table2)
    (loc robot4 table2)
    (nothing robot1)
    (nothing robot2)
    (nothing robot3)
    (nothing robot4)
    (selected robot1)
    (on pump1 hospital_cart_left1)
    (clear pump1)
    (on aed1 table1)
    (clear aed1)
    (on patient1 patient_bed_station1)
    (clear patient1)
    (on syringe1 hospital_cart_right1)
    (clear syringe1)
    (on cpr_board1 table2)
    (clear cpr_board1)
    (cancook robot1)    (cancut robot1)    (canmoveitem robot1)    (canmove robot1)    (cancook robot2)    (cancut robot2)    (canmoveitem robot2)    (canmove robot2)    (cancook robot3)    (cancut robot3)    (canmoveitem robot3)    (canmove robot3)    (cancook robot4)    (cancut robot4)    (canmoveitem robot4)    (canmove robot4))
(:goal
   (or
       (and
           (isusedforaed aed1)
           (atop cpr_board1 aed1)
           (isusedforcpr cpr_kit1)
           (atop aed1 cpr_kit1)
       )
   )
)
