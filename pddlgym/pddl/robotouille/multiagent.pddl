(define (problem robotouille)
(:domain robotouille)
(:objects
    table1 - station
    stove1 - station
    table2 - station
    patient_legs1 - station
    patient1 - station
    board1 - station
    table3 - station
    table4 - station
    cpr_kit1 - item
    cpr_stool1 - item
    cpr_board1 - item
    cpr_vent1 - item
    robot1 - player
    robot2 - player
    robot3 - player
    robot4 - player
)
(:init
    (istable table1)
    (isstove stove1)
    (istable table2)
    (ispatient_legs patient_legs1)
    (ispatient patient1)
    (isboard board1)
    (istable table3)
    (istable table4)
    (iscpr_kit cpr_kit1)
    (isusableforcpr cpr_kit1)
    (iscpr_stool cpr_stool1)
    (iscpr_stoolusuable cpr_stool1)
    (iscpr_board cpr_board1)
    (iscpr_boardusuable cpr_board1)
    (iscpr_vent cpr_vent1)
    (isrobot robot1)
    (isrobot robot2)
    (isrobot robot3)
    (isrobot robot4)
    (at cpr_kit1 table1)
    (vacant table1)
    (empty stove1)
    (loc robot1 stove1)
    (at cpr_stool1 table2)
    (vacant table2)
    (empty patient_legs1)
    (vacant patient_legs1)
    (at cpr_board1 patient1)
    (vacant patient1)
    (at cpr_board1 board1)
    (vacant board1)
    (at cpr_vent1 table3)
    (vacant table3)
    (empty table4)
    (loc robot4 table4)
    (nothing robot1)
    (nothing robot2)
    (nothing robot3)
    (nothing robot4)
    (selected robot1)
    (on cpr_kit1 table1)
    (clear cpr_kit1)
    (on cpr_stool1 table2)
    (clear cpr_stool1)
    (on cpr_board1 patient1)
    (clear cpr_board1)
    (on cpr_vent1 table3)
    (clear cpr_vent1)
    (cancook robot1)    (cancut robot1)    (canmoveitem robot1)    (canmove robot1)    (cancook robot2)    (cancut robot2)    (canmoveitem robot2)    (canmove robot2)    (cancook robot3)    (cancut robot3)    (canmoveitem robot3)    (canmove robot3)    (cancook robot4)    (cancut robot4)    (canmoveitem robot4)    (canmove robot4))
(:goal
   (or
       (and
           (iscpr_stoolused cpr_stool1)
           (iscpr_boardused cpr_board1)
           (atop patient_legs1 cpr_board1)
           (isusedforcpr cpr_kit1)
           (iscpr_ventused cpr_vent1)
       )
       (and
           (iscpr_stoolused cpr_stool1)
           (iscpr_boardused cpr_board1)
           (atop patient1 cpr_board1)
           (isusedforcpr cpr_kit1)
           (iscpr_ventused cpr_vent1)
       )
   )
)
