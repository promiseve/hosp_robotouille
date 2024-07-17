(define (problem robotouille)
(:domain robotouille)
(:objects
    patient1 - station
    table1 - station
    table2 - station
    table3 - station
    table4 - station
    aed1 - item
    cpr_kit1 - item
    ventilator1 - item
    medicine1 - item
    robot1 - player
    robot2 - player
    robot3 - player
)
(:init
    (ispatient patient1)
    (istable table1)
    (istable table2)
    (istable table3)
    (istable table4)
    (isaed aed1)
    (isusableforaed aed1)
    (iscpr_kit cpr_kit1)
    (isusableforcpr cpr_kit1)
    (isventilator ventilator1)
    (isusableforventilation ventilator1)
    (ismedicine medicine1)
    (isrobot robot1)
    (isrobot robot2)
    (isrobot robot3)
    (at aed1 patient1)
    (loc robot1 patient1)
    (empty table1)
    (loc robot2 table1)
    (at cpr_kit1 table2)
    (vacant table2)
    (empty table3)
    (vacant table3)
    (at medicine1 table4)
    (loc robot3 table4)
    (nothing robot1)
    (nothing robot2)
    (nothing robot3)
    (selected robot1)
    (on aed1 patient1)
    (clear aed1)
    (on cpr_kit1 table2)
    (clear cpr_kit1)
    (on medicine1 table4)
    (clear medicine1)
    (canmoveitem robot1)    (canmove robot1)    (canmoveitem robot2)    (canmove robot2)    (canmoveitem robot3)    (canmove robot3))
(:goal
   (or
       (and
           (isaeddefibrillated patient1)
           (iscprresuscitated patient1)
           (isventilated patient1)
           (atop aed1 patient1)
           (atop cpr_kit1 patient1)
           (atop ventilator1 patient1)
           (isusedforcpr cpr_kit1)
           (isusedforventilation ventilator1)
           (isusedforaed aed1)
       )
   )
)
