(define (problem robotouille)
(:domain robotouille)
(:objects
    hospital_cart_left1 - station
    patient_legs1 - station
    patient_bed_station1 - station
    hospital_cart_right1 - station
    table1 - station
    table2 - station
    aed1 - item
    patient1 - item
    pump1 - item
    cpr_board1 - item
    syringe1 - item
    robot1 - player
    robot2 - player
    robot3 - player
    robot4 - player
)
(:init
    (ishospital_cart_left hospital_cart_left1)
    (ispatient_legs patient_legs1)
    (ispatient_bed_station patient_bed_station1)
    (ishospital_cart_right hospital_cart_right1)
    (istable table1)
    (istable table2)
    (isaed aed1)
    (isusableforaed aed1)
    (ispatient patient1)
    (ispatient patient1)
    (ischestcompressable patient1)
    (ispump pump1)
    (ispumpusable pump1)
    (iscpr_board cpr_board1)
    (iscpr_board cpr_board1)
    (issyringe syringe1)
    (issyringeusable syringe1)
    (isrobot robot1)
    (isrobot robot2)
    (isrobot robot3)
    (isrobot robot4)
    (at aed1 hospital_cart_left1)
    (loc robot1 hospital_cart_left1)
    (empty patient_legs1)
    (vacant patient_legs1)
    (at patient1 patient_bed_station1)
    (vacant patient_bed_station1)
    (at pump1 hospital_cart_right1)
    (loc robot2 hospital_cart_right1)
    (at cpr_board1 table1)
    (loc robot4 table1)
    (at syringe1 table2)
    (loc robot3 table2)
    (nothing robot1)
    (nothing robot2)
    (nothing robot3)
    (nothing robot4)
    (selected robot1)
    (on aed1 hospital_cart_left1)
    (clear aed1)
    (on patient1 patient_bed_station1)
    (clear patient1)
    (on pump1 hospital_cart_right1)
    (clear pump1)
    (on cpr_board1 table1)
    (clear cpr_board1)
    (on syringe1 table2)
    (clear syringe1)
    (cancook robot1)    (cancut robot1)    (canmoveitem robot1)    (canmove robot1)    (cancook robot2)    (cancut robot2)    (canmoveitem robot2)    (canmove robot2)    (cancook robot3)    (cancut robot3)    (canmoveitem robot3)    (canmove robot3)    (canmoveitem robot4)    (canmove robot4)    (cancompresschest robot4)    (cangiverescuebreaths robot4)    (cangiveshock robot4)    (cangivemedicine robot4))
(:goal
   (or
       (and
           (istreated patient1)
       )
   )
)
