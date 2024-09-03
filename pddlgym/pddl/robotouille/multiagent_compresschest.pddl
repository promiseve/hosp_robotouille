(define (problem robotouille)
(:domain robotouille)
(:objects
    patient_legs1 - station
    patient_bed_station1 - station
    table1 - station
    patient1 - item
    robot1 - player
)
(:init
    (ispatient_legs patient_legs1)
    (ispatient_bed_station patient_bed_station1)
    (istable table1)
    (ispatient patient1)
    (ispatient patient1)
    (ischestcompressable patient1)
    (isrobot robot1)
<<<<<<< HEAD
=======
    (at aed1 table1)
    (vacant table1)
>>>>>>> b09d059ba24caf8e0bedaa1d16e1c1de90ee93b0
    (empty patient_legs1)
    (vacant patient_legs1)
    (at patient1 patient_bed_station1)
    (vacant patient_bed_station1)
<<<<<<< HEAD
    (empty table1)
    (loc robot1 table1)
=======
    (at cpr_board1 table2)
    (loc robot1 table2)
>>>>>>> b09d059ba24caf8e0bedaa1d16e1c1de90ee93b0
    (nothing robot1)
    (selected robot1)
    (on patient1 patient_bed_station1)
    (clear patient1)
<<<<<<< HEAD
=======
    (on cpr_board1 table2)
    (clear cpr_board1)
>>>>>>> b09d059ba24caf8e0bedaa1d16e1c1de90ee93b0
    (canmove robot1)    (cancompresschest robot1))
(:goal
   (or
       (and
           (ischestcompressed patient1)
       )
   )
)
