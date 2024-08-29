(define (problem robotouille)
(:domain robotouille)
(:objects
    table1 - station
    patient_legs1 - station
    patient_bed_station1 - station
    table2 - station
    cpr_kit1 - item
    aed1 - item
    patient1 - item
    cpr_board1 - item
    syringe1 - item
    robot1 - player
    robot2 - player
    robot3 - player
    robot4 - player
)
(:init
    (istable table1)
    (ispatient_legs patient_legs1)
    (ispatient_bed_station patient_bed_station1)
    (istable table2)
    (iscpr_kit cpr_kit1)
    (isusableforcpr cpr_kit1)
    (isaed aed1)
    (isusableforaed aed1)
    (ispatient patient1)
    (ispatient patient1)
    (iscpr_board cpr_board1)
    (iscpr_boardusuable cpr_board1)
    (issyringe syringe1)
    (issyringe syringe1)
    (isrobot robot1)
    (isrobot robot2)
    (isrobot robot3)
    (isrobot robot4)
    (at aed1 table1)
    (vacant table1)
    (empty patient_legs1)
    (vacant patient_legs1)
    (at patient1 patient_bed_station1)
    (vacant patient_bed_station1)
    (at cpr_board1 table2)
    (at syringe1 table2)
    (loc robot4 table2)
    (nothing robot1)
    (nothing robot2)
    (nothing robot3)
    (nothing robot4)
    (selected robot1)
    (on aed1 table1)
    (clear aed1)
    (on patient1 patient_bed_station1)
    (clear patient1)
    (on cpr_board1 table2)
    (atop syringe1 cpr_board1)
    (clear syringe1)
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
