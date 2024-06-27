(define (problem robotouille)
(:domain robotouille)
(:objects
    stove1 - station
    table1 - station
    board1 - station
    board2 - station
    table2 - station
    board3 - station
    table3 - station
    table4 - station
    stove2 - station
    stove3 - station
    board4 - station
    stove4 - station
    topbun1 - item
    patty1 - item
    bottombun1 - item
    cheese1 - item
    lettuce1 - item
    topbun2 - item
    lettuce2 - item
    patty2 - item
    robot1 - player
)
(:init
    (isstove stove1)
    (istable table1)
    (isboard board1)
    (isboard board2)
    (istable table2)
    (isboard board3)
    (istable table3)
    (istable table4)
    (isstove stove2)
    (isstove stove3)
    (isboard board4)
    (isstove stove4)
    (istopbun topbun1)
    (ispatty patty1)
    (iscookable patty1)
    (isbottombun bottombun1)
    (ischeese cheese1)
    (islettuce lettuce1)
    (iscuttable lettuce1)
    (istopbun topbun2)
    (islettuce lettuce2)
    (iscuttable lettuce2)
    (ispatty patty2)
    (iscookable patty2)
    (isrobot robot1)
    (empty stove1)
    (vacant stove1)
    (at topbun1 table1)
    (vacant table1)
    (at patty1 board1)
    (loc robot1 board1)
    (at bottombun1 board2)
    (vacant board2)
    (at cheese1 table2)
    (vacant table2)
    (at lettuce1 board3)
    (vacant board3)
    (at topbun2 table3)
    (vacant table3)
    (at lettuce2 table4)
    (vacant table4)
    (at patty2 stove2)
    (vacant stove2)
    (empty stove3)
    (vacant stove3)
    (empty board4)
    (vacant board4)
    (empty stove4)
    (vacant stove4)
    (nothing robot1)
    (selected robot1)
    (on topbun1 table1)
    (clear topbun1)
    (on patty1 board1)
    (clear patty1)
    (on bottombun1 board2)
    (clear bottombun1)
    (on cheese1 table2)
    (clear cheese1)
    (on lettuce1 board3)
    (clear lettuce1)
    (on topbun2 table3)
    (clear topbun2)
    (on lettuce2 table4)
    (clear lettuce2)
    (on patty2 stove2)
    (clear patty2)
    (cancook robot1)    (cancut robot1)    (canmoveitem robot1)    (canmove robot1))
(:goal
   (or
       (and
           (iscut lettuce1)
           (atop topbun1 lettuce1)
           (iscooked patty1)
           (atop lettuce1 patty1)
           (atop patty1 bottombun1)
       )
       (and
           (iscut lettuce1)
           (atop topbun1 lettuce1)
           (iscooked patty2)
           (atop lettuce1 patty2)
           (atop patty2 bottombun1)
       )
       (and
           (iscut lettuce1)
           (atop topbun2 lettuce1)
           (iscooked patty1)
           (atop lettuce1 patty1)
           (atop patty1 bottombun1)
       )
       (and
           (iscut lettuce1)
           (atop topbun2 lettuce1)
           (iscooked patty2)
           (atop lettuce1 patty2)
           (atop patty2 bottombun1)
       )
       (and
           (iscut lettuce2)
           (atop topbun1 lettuce2)
           (iscooked patty1)
           (atop lettuce2 patty1)
           (atop patty1 bottombun1)
       )
       (and
           (iscut lettuce2)
           (atop topbun1 lettuce2)
           (iscooked patty2)
           (atop lettuce2 patty2)
           (atop patty2 bottombun1)
       )
       (and
           (iscut lettuce2)
           (atop topbun2 lettuce2)
           (iscooked patty1)
           (atop lettuce2 patty1)
           (atop patty1 bottombun1)
       )
       (and
           (iscut lettuce2)
           (atop topbun2 lettuce2)
           (iscooked patty2)
           (atop lettuce2 patty2)
           (atop patty2 bottombun1)
       )
   )
)
