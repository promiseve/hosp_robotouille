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
<<<<<<< HEAD
    (ischestcompressed patient1)
=======
    (ischestcompressable patient1)
    (iseligibletoreceiverescuebreaths patient1)
>>>>>>> b09d059ba24caf8e0bedaa1d16e1c1de90ee93b0
    (isrobot robot1)
    (empty patient_legs1)
    (vacant patient_legs1)
    (at patient1 patient_bed_station1)
    (vacant patient_bed_station1)
    (empty table1)
    (loc robot1 table1)
    (nothing robot1)
    (selected robot1)
    (on patient1 patient_bed_station1)
    (clear patient1)
    (canmove robot1)    (cangiverescuebreaths robot1))
(:goal
   (or
       (and
<<<<<<< HEAD
           (isrescuebreathed patient1)
=======
           (isrescuebreathed patient_legs1)
       )
       (and
           (isrescuebreathed patient_bed_station1)
>>>>>>> b09d059ba24caf8e0bedaa1d16e1c1de90ee93b0
       )
   )
)
