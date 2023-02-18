
(define (problem navigation) (:domain navigation7)
  (:objects
    f0-0f - location
	f0-1f - location
	f0-2f - location
	f0-3f - location
	f0-4f - location
	f1-0f - location
	f1-1f - location
	f1-2f - location
	f1-3f - location
	f1-4f - location
	f2-0f - location
	f2-1f - location
	f2-2f - location
	f2-3f - location
	f2-4f - location
	f3-0f - location
	f3-1f - location
	f3-2f - location
	f3-3f - location
	f3-4f - location
	f4-0f - location
	f4-1f - location
	f4-2f - location
	f4-3f - location
	f4-4f - location
	f5-0f - location
	f5-1f - location
	f5-2f - location
	f5-3f - location
	f5-4f - location
	f6-0f - location
	f6-1f - location
	f6-2f - location
	f6-3f - location
	f6-4f - location
	f7-0f - location
	f7-1f - location
	f7-2f - location
	f7-3f - location
	f7-4f - location
	f8-0f - location
	f8-1f - location
	f8-2f - location
	f8-3f - location
	f8-4f - location
	f9-0f - location
	f9-1f - location
	f9-2f - location
	f9-3f - location
	f9-4f - location
  )
  (:init
    (conn f0-1f f0-0f up)
	(conn f0-1f f0-2f down)
	(conn f0-1f f1-1f right)
	(conn f0-2f f0-1f up)
	(conn f0-2f f0-3f down)
	(conn f0-2f f1-2f right)
	(conn f0-3f f0-2f up)
	(conn f0-3f f0-4f down)
	(conn f0-3f f1-3f right)
	(conn f1-1f f1-0f up)
	(conn f1-1f f1-2f down)
	(conn f1-1f f2-1f right)
	(conn f1-1f f0-1f left)
	(conn f1-2f f1-1f up)
	(conn f1-2f f1-3f down)
	(conn f1-2f f2-2f right)
	(conn f1-2f f0-2f left)
	(conn f1-3f f1-2f up)
	(conn f1-3f f1-4f down)
	(conn f1-3f f2-3f right)
	(conn f1-3f f0-3f left)
	(conn f2-1f f2-0f up)
	(conn f2-1f f2-2f down)
	(conn f2-1f f3-1f right)
	(conn f2-1f f1-1f left)
	(conn f2-2f f2-1f up)
	(conn f2-2f f2-3f down)
	(conn f2-2f f3-2f right)
	(conn f2-2f f1-2f left)
	(conn f2-3f f2-2f up)
	(conn f2-3f f2-4f down)
	(conn f2-3f f3-3f right)
	(conn f2-3f f1-3f left)
	(conn f3-1f f3-0f up)
	(conn f3-1f f3-2f down)
	(conn f3-1f f4-1f right)
	(conn f3-1f f2-1f left)
	(conn f3-2f f3-1f up)
	(conn f3-2f f3-3f down)
	(conn f3-2f f4-2f right)
	(conn f3-2f f2-2f left)
	(conn f3-3f f3-2f up)
	(conn f3-3f f3-4f down)
	(conn f3-3f f4-3f right)
	(conn f3-3f f2-3f left)
	(conn f4-1f f4-0f up)
	(conn f4-1f f4-2f down)
	(conn f4-1f f5-1f right)
	(conn f4-1f f3-1f left)
	(conn f4-2f f4-1f up)
	(conn f4-2f f4-3f down)
	(conn f4-2f f5-2f right)
	(conn f4-2f f3-2f left)
	(conn f4-3f f4-2f up)
	(conn f4-3f f4-4f down)
	(conn f4-3f f5-3f right)
	(conn f4-3f f3-3f left)
	(conn f5-1f f5-0f up)
	(conn f5-1f f5-2f down)
	(conn f5-1f f6-1f right)
	(conn f5-1f f4-1f left)
	(conn f5-2f f5-1f up)
	(conn f5-2f f5-3f down)
	(conn f5-2f f6-2f right)
	(conn f5-2f f4-2f left)
	(conn f5-3f f5-2f up)
	(conn f5-3f f5-4f down)
	(conn f5-3f f6-3f right)
	(conn f5-3f f4-3f left)
	(conn f6-1f f6-0f up)
	(conn f6-1f f6-2f down)
	(conn f6-1f f7-1f right)
	(conn f6-1f f5-1f left)
	(conn f6-2f f6-1f up)
	(conn f6-2f f6-3f down)
	(conn f6-2f f7-2f right)
	(conn f6-2f f5-2f left)
	(conn f6-3f f6-2f up)
	(conn f6-3f f6-4f down)
	(conn f6-3f f7-3f right)
	(conn f6-3f f5-3f left)
	(conn f7-1f f7-0f up)
	(conn f7-1f f7-2f down)
	(conn f7-1f f8-1f right)
	(conn f7-1f f6-1f left)
	(conn f7-2f f7-1f up)
	(conn f7-2f f7-3f down)
	(conn f7-2f f8-2f right)
	(conn f7-2f f6-2f left)
	(conn f7-3f f7-2f up)
	(conn f7-3f f7-4f down)
	(conn f7-3f f8-3f right)
	(conn f7-3f f6-3f left)
	(conn f8-1f f8-0f up)
	(conn f8-1f f8-2f down)
	(conn f8-1f f9-1f right)
	(conn f8-1f f7-1f left)
	(conn f8-2f f8-1f up)
	(conn f8-2f f8-3f down)
	(conn f8-2f f9-2f right)
	(conn f8-2f f7-2f left)
	(conn f8-3f f8-2f up)
	(conn f8-3f f8-4f down)
	(conn f8-3f f9-3f right)
	(conn f8-3f f7-3f left)
	(conn f9-1f f9-0f up)
	(conn f9-1f f9-2f down)
	(conn f9-1f f8-1f left)
	(conn f9-2f f9-1f up)
	(conn f9-2f f9-3f down)
	(conn f9-2f f8-2f left)
	(conn f9-3f f9-2f up)
	(conn f9-3f f9-4f down)
	(conn f9-3f f8-3f left)
	(conn f0-4f f0-3f up)
	(conn f0-4f f1-4f right)
	(conn f1-4f f1-3f up)
	(conn f1-4f f2-4f right)
	(conn f1-4f f0-4f left)
	(conn f2-4f f2-3f up)
	(conn f2-4f f3-4f right)
	(conn f2-4f f1-4f left)
	(conn f3-4f f3-3f up)
	(conn f3-4f f4-4f right)
	(conn f3-4f f2-4f left)
	(conn f4-4f f4-3f up)
	(conn f4-4f f5-4f right)
	(conn f4-4f f3-4f left)
	(conn f5-4f f5-3f up)
	(conn f5-4f f6-4f right)
	(conn f5-4f f4-4f left)
	(conn f6-4f f6-3f up)
	(conn f6-4f f7-4f right)
	(conn f6-4f f5-4f left)
	(conn f7-4f f7-3f up)
	(conn f7-4f f8-4f right)
	(conn f7-4f f6-4f left)
	(conn f8-4f f8-3f up)
	(conn f8-4f f9-4f right)
	(conn f8-4f f7-4f left)
	(conn f9-4f f9-3f up)
	(conn f9-4f f8-4f left)
	(conn f0-0f f0-1f down)
	(conn f0-0f f1-0f right)
	(conn f1-0f f1-1f down)
	(conn f1-0f f2-0f right)
	(conn f1-0f f0-0f left)
	(conn f2-0f f2-1f down)
	(conn f2-0f f3-0f right)
	(conn f2-0f f1-0f left)
	(conn f3-0f f3-1f down)
	(conn f3-0f f4-0f right)
	(conn f3-0f f2-0f left)
	(conn f4-0f f4-1f down)
	(conn f4-0f f5-0f right)
	(conn f4-0f f3-0f left)
	(conn f5-0f f5-1f down)
	(conn f5-0f f6-0f right)
	(conn f5-0f f4-0f left)
	(conn f6-0f f6-1f down)
	(conn f6-0f f7-0f right)
	(conn f6-0f f5-0f left)
	(conn f7-0f f7-1f down)
	(conn f7-0f f8-0f right)
	(conn f7-0f f6-0f left)
	(conn f8-0f f8-1f down)
	(conn f8-0f f9-0f right)
	(conn f8-0f f7-0f left)
	(conn f9-0f f9-1f down)
	(conn f9-0f f8-0f left)

    (is-prob f0-1f)
	(is-prob f0-2f)
	(is-prob f0-3f)
	(is-prob f1-1f)
	(is-prob f1-2f)
	(is-prob f1-3f)
	(is-prob f2-1f)
	(is-prob f2-2f)
	(is-prob f2-3f)
	(is-prob f3-1f)
	(is-prob f3-2f)
	(is-prob f3-3f)
	(is-prob f4-1f)
	(is-prob f4-2f)
	(is-prob f4-3f)
	(is-prob f5-1f)
	(is-prob f5-2f)
	(is-prob f5-3f)
	(is-prob f6-1f)
	(is-prob f6-2f)
	(is-prob f6-3f)
	(is-prob f7-1f)
	(is-prob f7-2f)
	(is-prob f7-3f)
	(is-prob f8-1f)
	(is-prob f8-2f)
	(is-prob f8-3f)
	(is-prob f9-1f)
	(is-prob f9-2f)
	(is-prob f9-3f)

    (is-col-0 f0-0f)
    (is-col-0 f0-1f)
    (is-col-0 f0-2f)
    (is-col-0 f0-3f)
    (is-col-0 f0-4f)
    (is-col-1 f1-0f)
    (is-col-1 f1-1f)
    (is-col-1 f1-2f)
    (is-col-1 f1-3f)
    (is-col-1 f1-4f)
    (is-col-2 f2-0f)
    (is-col-2 f2-1f)
    (is-col-2 f2-2f)
    (is-col-2 f2-3f)
    (is-col-2 f2-4f)
    (is-col-3 f3-0f)
    (is-col-3 f3-1f)
    (is-col-3 f3-2f)
    (is-col-3 f3-3f)
    (is-col-3 f3-4f)
    (is-col-4 f4-0f)
    (is-col-4 f4-1f)
    (is-col-4 f4-2f)
    (is-col-4 f4-3f)
    (is-col-4 f4-4f)
    (is-col-5 f5-0f)
    (is-col-5 f5-1f)
    (is-col-5 f5-2f)
    (is-col-5 f5-3f)
    (is-col-5 f5-4f)
    (is-col-6 f6-0f)
    (is-col-6 f6-1f)
    (is-col-6 f6-2f)
    (is-col-6 f6-3f)
    (is-col-6 f6-4f)
    (is-col-7 f7-0f)
    (is-col-7 f7-1f)
    (is-col-7 f7-2f)
    (is-col-7 f7-3f)
    (is-col-7 f7-4f)
    (is-col-8 f8-0f)
    (is-col-8 f8-1f)
    (is-col-8 f8-2f)
    (is-col-8 f8-3f)
    (is-col-8 f8-4f)
    (is-col-9 f9-0f)
    (is-col-9 f9-1f)
    (is-col-9 f9-2f)
    (is-col-9 f9-3f)
    (is-col-9 f9-4f)

    (move down)
    (move left)
    (move right)
    (move up)

    (robot-at f9-4f)
  )
  (:goal (and
    (robot-at f9-0f)))
)
    
