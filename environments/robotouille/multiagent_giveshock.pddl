(define (problem robotouille)
(:domain robotouille)
(:objects
    hospital_cart_left1 - station
    patient_legs1 - station
    patient_bed_station1 - station
    hospital_cart_right1 - station
    table1 - station
    aed1 - item
    patient1 - item
    pump1 - item
    cpr_board1 - item
    robot1 - player
)
(:init
    (ishospital_cart_left hospital_cart_left1)
    (ispatient_legs patient_legs1)
    (ispatient_bed_station patient_bed_station1)
    (ishospital_cart_right hospital_cart_right1)
    (istable table1)
    (isaed aed1)
    (isusableforaed aed1)
    (ispatient patient1)
    (ispatient patient1)
    (ischestcompressable patient1)
    (ispump pump1)
    (ispumpusable pump1)
    (iscpr_board cpr_board1)
    (iscpr_board cpr_board1)
    (isrobot robot1)
    (at aed1 hospital_cart_left1)
    (vacant hospital_cart_left1)
    (empty patient_legs1)
    (vacant patient_legs1)
    (at patient1 patient_bed_station1)
    (vacant patient_bed_station1)
    (at pump1 hospital_cart_right1)
    (vacant hospital_cart_right1)
    (at cpr_board1 table1)
    (loc robot1 table1)
    (nothing robot1)
    (selected robot1)
    (on aed1 hospital_cart_left1)
    (clear aed1)
    (on patient1 patient_bed_station1)
    (clear patient1)
    (on pump1 hospital_cart_right1)
    (clear pump1)
    (on cpr_board1 table1)
    (clear cpr_board1)
    (canmoveitem robot1)    (canmove robot1)    (cancompresschest robot1)    (cangiverescuebreaths robot1)    (cangiveshock robot1))
(:goal
   (or
       (and
           (isusedforaed aed1)
           (ispumpused pump1)
           (isshocked patient1)
       )
   )
)
