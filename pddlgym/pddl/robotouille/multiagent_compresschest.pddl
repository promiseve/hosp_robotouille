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
    robot1 - player
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
    (ischestcompressable patient1)
    (iscpr_board cpr_board1)
    (iscpr_boardusuable cpr_board1)
    (isrobot robot1)
    (at aed1 table1)
    (vacant table1)
    (empty patient_legs1)
    (vacant patient_legs1)
    (at patient1 patient_bed_station1)
    (vacant patient_bed_station1)
    (at cpr_board1 table2)
    (loc robot1 table2)
    (nothing robot1)
    (selected robot1)
    (on aed1 table1)
    (clear aed1)
    (on patient1 patient_bed_station1)
    (clear patient1)
    (on cpr_board1 table2)
    (clear cpr_board1)
    (canmove robot1)    (cancompresschest robot1))
(:goal
   (or
       (and
           (ischestcompressed patient1)
       )
   )
)
