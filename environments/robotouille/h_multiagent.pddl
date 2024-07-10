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
    robot1 - player
    robot2 - player
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
    (isrobot robot1)
    (isrobot robot2)
    (empty patient1)
    (vacant patient1)
    (at aed1 table1)
    (vacant table1)
    (at cpr_kit1 table2)
    (vacant table2)
    (at ventilator1 table3)
    (vacant table3)
    (empty table4)
    (vacant table4)
    (nothing robot1)
    (nothing robot2)
    (selected robot1)
    (on aed1 table1)
    (clear aed1)
    (on cpr_kit1 table2)
    (clear cpr_kit1)
    (on ventilator1 table3)
    (clear ventilator1)
    (canmove robot1)    (canmove robot2))
(:goal
   (or
       (and
           (isaeddefibrillated patient1)
           (iscprresuscitated patient1)
           (isventilated patient1)
           (on aed1 patient1)
           (on cpr_kit1 patient1)
           (on ventilator1 patient1)
       )
   )
)
