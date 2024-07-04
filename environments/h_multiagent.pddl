(define (problem hospital_robotouille)
(:domain robotouille)
(:objects
    patient1 - station
    table1 - station
    aed_station1 - station
    cpr_station1 - station
    ventilation_station1 - station
    board1 - station
    aed1 - item
    cpr_kit1 - item
    ventilator1 - item
    robot1 - player
    robot2 - player
    robot3 - player
    robot4 - player
    robot5 - player
)
(:init
    (ispatient patient1)
    (istable table1)
    (isaed_station aed_station1)
    (iscpr_station cpr_station1)
    (isventilation_station ventilation_station1)
    (isaed aed1)
    (isusableforaed aed1)
    (iscpr_kit cpr_kit1)
    (isusableforcpr cpr_kit1)
    (isventilator ventilator1)
    (isusableforventilation ventilator1)
    (isrobot robot1)
    (isrobot robot2)
    (isrobot robot3)
    (isrobot robot4)
    (isrobot robot5)
    (at aed1 aed_station1)
    (on aed1 aed_station1)
    (loc robot1 aed_station1)
    (empty cpr_station1)
    (loc robot2 cpr_station1)
    (at cpr_kit1 cpr_station1)
    (vacant cpr_station1)
    (at ventilator1 ventilation_station1)
    (vacant ventilation_station1)
    (loc robot3 table1)
    (loc robot4 ventilation_station1)
    (loc robot5 patient1)
    (nothing robot1)
    (nothing robot2)
    (nothing robot3)
    (nothing robot4)
    (nothing robot5)
    (selected robot1)
    (on aed1 aed_station1)
    (clear aed1)
    (on cpr_kit1 cpr_station1)
    (clear cpr_kit1)
    (on ventilator1 ventilation_station1)
    (clear ventilator1)
    (canuseaed robot1)
    (canmovecprkit robot1)
    (canmoveventilator robot1)
    (canmove robot1)
    (canuseaed robot2)
    (canmovecprkit robot2)
    (canmoveventilator robot2)
    (canmove robot2)
    (canuseaed robot3)
    (canmovecprkit robot3)
    (canmoveventilator robot3)
    (canmove robot3)
    (canuseaed robot4)
    (canmovecprkit robot4)
    (canmoveventilator robot4)
    (canmove robot4)
    (canuseaed robot5)
    (canmovecprkit robot5)
    (canmoveventilator robot5)
    (canmove robot5)
)
(:goal
   (and
       (atop aed1 patient1)
       (atop cpr_kit1 patient1)
       (atop ventilator1 patient1)
   )
)
)