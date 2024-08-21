(define (problem robotouille)
(:domain robotouille)
(:objects
    table1 - station
    stove1 - station
    table2 - station
    patient_legs1 - station
    patient1 - station
    table3 - station
    board1 - station
    table4 - station
    cpr_kit1 - item
    aed1 - item
    cpr_board1 - item
    bottombun1 - item
    topbun1 - item
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
    (istable table3)
    (isboard board1)
    (istable table4)
    (iscpr_kit cpr_kit1)
    (isusableforcpr cpr_kit1)
    (isaed aed1)
    (isusableforaed aed1)
    (iscpr_board cpr_board1)
    (iscpr_boardusuable cpr_board1)
    (isbottombun bottombun1)
    (istopbun topbun1)
    (isrobot robot1)
    (isrobot robot2)
    (isrobot robot3)
    (isrobot robot4)
    (at cpr_kit1 table1)
    (loc robot1 table1)
    (empty stove1)
    (loc robot2 stove1)
    (at aed1 table2)
    (vacant table2)
    (empty patient_legs1)
    (vacant patient_legs1)
    (empty patient1)
    (vacant patient1)
    (at bottombun1 table3)
    (vacant table3)
    (empty board1)
    (vacant board1)
    (at topbun1 table4)
    (loc robot3 table4)
    (loc robot4 table4)
    (nothing robot1)
    (nothing robot2)
    (nothing robot3)
    (nothing robot4)
    (selected robot1)
    (on cpr_kit1 table1)
    (clear cpr_kit1)
    (on aed1 table2)
    (clear aed1)
    (on bottombun1 table3)
    (clear bottombun1)
    (on topbun1 table4)
    (clear topbun1)
    (cancook robot1)    (cancut robot1)    (canmoveitem robot1)    (canmove robot1)    (cancook robot2)    (cancut robot2)    (canmoveitem robot2)    (canmove robot2)    (cancook robot3)    (cancut robot3)    (canmoveitem robot3)    (canmove robot3)    (cancook robot4)    (cancut robot4)    (canmoveitem robot4)    (canmove robot4))
(:goal
   (or
       (and
           (isusedforaed aed1)
           (atop topbun1 aed1)
           (isusedforcpr cpr_kit1)
           (atop aed1 cpr_kit1)
           (atop cpr_kit1 bottombun1)
       )
   )
)
