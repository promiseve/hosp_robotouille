;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;           Robotouille!!!          ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain robotouille)
    (:requirements :strips :typing :disjunctive-preconditions)
    (:types station player item)
    (:predicates
        ; Identity Predicates
        (istable ?s - station)
        (isstove ?s - station)
        (isboard ?s - station)
        (isfryer ?s - station)
        (ispatient ?s - item)
        (isaed_station ?s - station)
        (iscpr_station ?s - station)
        (isventilation_station ?s - station)
        (ispatient_bed_station ?s - station)
        (ishospital_cart_left ?s - station)
        (ishospital_cart_right ?s - station)
        (ispatient_legs ?s - station)      
        (isrobot ?p - player)
        (isnurse ?p - player)
        (istopbun ?i - item)
        (isbottombun ?i - item)
        (isbread ?i - item)
        (islettuce ?i - item)
        (isonion ?i - item)
        (istomato ?i - item)
        (iscuttable ?i - item)
        (iscut ?i - item)
        (ispatty ?i - item)
        (ischicken ?i - item)
        (iscookable ?i - item)
        (iscooked ?i - item)
        (ischeese ?i - item)
        (isfryable ?i - item)
        (isfryableifcut ?i - item)
        (isfried ?i - item)
        (ispotato ?i - item)
        (isusableforcpr ?i - item)
        (isusedforcpr ?i - item)
        (isusedforaed ?i - item)
        (isventilator ?i - item)
        (isusableforventilation ?i - item)
        (isusedforventilation ?i - item)
        (isusableforaed ?i - item)
        (ismedicine ?i - item)
        (isaed ?i - item)
        (iscpr_kit ?i - item)
        (iscpr_stool ?i - item)
        (iscpr_stoolusuable ?i - item)
        (iscpr_stoolused ?i - item)
        (iscpr_board ?i - item)
        (iscpr_boardused ?i - item)
        (iscpr_boardusuable ?i - item)
        (ischestcompressable ?i - item)
        (ischestcompressed ?i - item)
        (isrbifchestcompressed ?i - item) 
        (iseligibletoreceiverescuebreaths ?i - item)
        (isrescuebreathed ?i - item)
        (istreated ?i - item)
        (issyringe ?i - item)
        (issyringeusable ?i - item)
        (issyringeused ?i - item)
        (ispump ?i - item)
        (ispumpusable ?i - item)
        (ispumpused ?i - item)
        (isshocked ?i - item)

        ; State Predicates
        (loc ?p - player ?s - station)
        (at ?i - item ?s - station)
        (nothing ?p - player)
        (empty ?s - station)
        (on ?i - item ?s - station)
        (vacant ?s - station)
        (clear ?i - item)
        (atop ?i1 - item ?i2 - item)
        (has ?p - player ?i - item)
        (selected ?p - player)
        (cancook ?p - player)
        (cancut ?p - player)
        (canmoveitem ?p - player)
        (canmove ?p - player)
        (canfry ?p - player)
        (canfrycut ?p - player)
        (cangivemedicine ?p - player)
        (cancompresschest ?p - player)
        (cangiverescuebreaths ?p - player)
        (cangiveshock ?p - player)
    )

    ; ACTIONS
    ; Deliver shock
    (:action giveshock
        :parameters (?p - player ?i1 - item ?i2 - item ?i3 - item ?i4 - item ?s - station)
        :precondition (and
            (ispatient_bed_station ?s)
            (ispatient ?i1)
            (isaed ?i2)
            (ispump ?i3)
            (iscpr_board ?i4)
            (isrescuebreathed ?i1)
            (on ?i4 ?s)
            (at ?i4 ?s)
            (atop ?i3 ?i1)
            (atop ?i2 ?i3)            
            (loc ?p ?s)
            (selected ?p)
            (cangiveshock ?p)
        )
        :effect (and
            (isshocked ?i1)
        )
    )

    ; Insert Syringe into the patient,; Make the nurse player place a medicine item on top the patient station
    (:action givemedicine
        :parameters (?p - player ?i1 - item ?i2 - item ?i3 - item ?i4 - item ?i5 - item ?s - station)
        :precondition (and
            (ispatient_bed_station ?s)
            (ispatient ?i1)
            (isaed ?i2)
            (ispump ?i3)
            (iscpr_board ?i4)
            (ismedicine ?i5)
            (isshocked ?i1)
            (on ?i4 ?s)
            (at ?i4 ?s)
            (atop ?i3 ?i1)
            (atop ?i2 ?i3)
            (atop ?i5 ?i2) ;medicine is on the AED
            (loc ?p ?s)
            (selected ?p)
            (cangivemedicine ?p)
        )
        :effect (and
            (istreated ?i1)
        )
    )

    ; Move the player from station 1 to station 2
    (:action move
        :parameters (?p - player ?s1 - station ?s2 - station)
        :precondition (and
            (loc ?p ?s1)
            (selected ?p)
            (canmove ?p)
        )
        :effect (and
            (loc ?p ?s2)
            (vacant ?s1)
            (not (loc ?p ?s1))
            (not (vacant ?s2))
        )
    )

    ; Make the player pick up an item from a station
    (:action pick-up
        :parameters (?p - player ?i - item ?s - station)
        :precondition (and
            (nothing ?p)
            (on ?i ?s)
            (loc ?p ?s)
            (clear ?i)
            (selected ?p)
            (canmoveitem ?p)
        )
        :effect (and
            (has ?p ?i)
            (empty ?s)
            (not (nothing ?p))
            (not (at ?i ?s))
            (not (clear ?i))
            (not (on ?i ?s))
        )
    )

    ; Make the player place an item on a station
    (:action place
        :parameters (?p - player ?i - item ?s - station)
        :precondition (and
            (has ?p ?i)
            (loc ?p ?s)
            (empty ?s)
            (selected ?p)
            (canmoveitem ?p)
        )
        :effect (and
            (nothing ?p)
            (at ?i ?s)
            (clear ?i)
            (on ?i ?s)
            (not (has ?p ?i))
            (not (empty ?s))
        )
    )


    ; Make the player cook a cookable item on a stove
    (:action cook
        :parameters (?p - player ?i - item ?s - station)
        :precondition (and
            (isstove ?s)
            (iscookable ?i)
            (on ?i ?s)
            (loc ?p ?s)
            (clear ?i)
            (selected ?p)
            (cancook ?p)
        )
        :effect (and
            (iscooked ?i)
        )
    )

    ;Make the player compress patient's chest
    (:action compresschest
        :parameters (?p - player ?i - item ?s - station)
        :precondition (and
            (ispatient_bed_station ?s)
            (ispatient ?i) 
            (ischestcompressable ?i)
            (on ?i ?s)
            (loc ?p ?s)
            (clear ?i)
            (selected ?p)
            (cancompresschest ?p)
            (not (ischestcompressed ?i))
        )
        :effect (and
            (ischestcompressed ?i)
        )
    )

    ;Make the player give patient rescue breaths
    (:action giverescuebreaths
        :parameters (?p - player ?i - item ?s - station)
        :precondition (and
            (ispatient_bed_station ?s)
            (ispatient ?i) 
            (ischestcompressed ?i)  ; Typically, rescue breaths follow chest compressions
            (on ?i ?s)
            (loc ?p ?s)
            (clear ?i)
            (selected ?p)
            (cangiverescuebreaths ?p)
        )
        :effect (and
            (isrescuebreathed ?i)
        )
    )

    ; Make the player fry a fryable item in a fryer
    (:action fry
        :parameters (?p - player ?i - item ?s - station)
        :precondition (and
            (isfryer ?s)
            (isfryable ?i)
            (on ?i ?s)
            (loc ?p ?s)
            (clear ?i)
            (selected ?p)
            (canfry ?p)
        )
        :effect (and
            (isfried ?i)
        )
    )

    ; Make the player fry an item that is only fryable if cut, in a fryer
    (:action fry_cut_item
        :parameters (?p - player ?i - item ?s - station)
        :precondition (and
            (isfryer ?s)
            (isfryableifcut ?i)
            (iscut ?i)
            (on ?i ?s)
            (loc ?p ?s)
            (clear ?i)
            (selected ?p)
            (canfrycut ?p)
        )
        :effect (and
            (isfried ?i)
        )
    )

    ; Make the player stack an item on top of another item at a station
    (:action stack
        :parameters (?p - player ?i1 - item ?i2 - item ?s - station)
        :precondition (and
            (has ?p ?i1)
            (clear ?i2)
            (loc ?p ?s)
            (at ?i2 ?s)
            (selected ?p)
            (canmoveitem ?p)
        )
        :effect (and
            (nothing ?p)
            (at ?i1 ?s)
            (atop ?i1 ?i2)
            (clear ?i1)
            (not (clear ?i2))
            (not (has ?p ?i1))
        )
    )
    ; Make the player stack an item under another item at a station
    (:action stackunder
        :parameters (?p - player ?i1 - item ?i2 - item ?s - station)
        :precondition (and
            (has ?p ?i1)
            (loc ?p ?s)
            (on ?i2 ?s)
            (selected ?p)
            (canmoveitem ?p)
        )
        :effect (and
            (nothing ?p)
            (at ?i1 ?s)
            (on ?i1 ?s)
            (atop ?i2 ?i1)
            (not (on ?i2 ?s))
            (not (has ?p ?i1))
        )
    )
    
    ; Make the player cut a cuttable item on a cutting board
    (:action cut
        :parameters (?p - player ?i - item ?s - station)
        :precondition (and
            (isboard ?s)
            (iscuttable ?i)
            (on ?i ?s)
            (loc ?p ?s)
            (clear ?i)
            (selected ?p)
            (cancut ?p)
        )
        :effect (and
            (iscut ?i)
        )
    )

    ; Make the player unstack an item from another item at a station
    (:action unstack
        :parameters (?p - player ?i1 - item ?i2 - item ?s - station)
        :precondition (and
            (nothing ?p)
            (clear ?i1)
            (atop ?i1 ?i2)
            (loc ?p ?s)
            (at ?i1 ?s)
            (at ?i2 ?s)
            (selected ?p)
            (canmoveitem ?p)
        )
        :effect (and
            (has ?p ?i1)
            (clear ?i2)
            (not (nothing ?p))
            (not (clear ?i1))
            (not (atop ?i1 ?i2))
            (not (at ?i1 ?s))
        )
    )

    ; Change player selection
    (:action select
        :parameters (?p1 - player ?p2 - player)
        :precondition (and
            (selected ?p1)
            (not  (selected ?p2))
        )
        :effect (and
            (not (selected ?p1))
            (selected ?p2)
        )
    )
)