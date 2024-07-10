(define (problem robotouille)
(:domain robotouille)
(:objects
    patient1 - station
    aed_station1 - station
    cpr_station1 - station
    ventilation_station1 - station
    table1 - station
    aed1 - item
    cpr_kit1 - item
    ventilator1 - item
    robot1 - player
    robot2 - player
)
(:init
    (ispatient patient1)
    (isaed_station aed_station1)
    (iscpr_station cpr_station1)
    (isventilation_station ventilation_station1)
    (istable table1)
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
    (at aed1 aed_station1)
    (vacant aed_station1)
    (at cpr_kit1 cpr_station1)
    (vacant cpr_station1)
    (at ventilator1 ventilation_station1)
    (vacant ventilation_station1)
    (empty table1)
    (vacant table1)
    (nothing robot1)
    (nothing robot2)
    (selected robot1)
    (on aed1 aed_station1)
    (clear aed1)
    (on cpr_kit1 cpr_station1)
    (clear cpr_kit1)
    (on ventilator1 ventilation_station1)
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
