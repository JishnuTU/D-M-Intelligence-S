(deftemplate entity
    (slot aid (type STRING))
    (slot latitude (type NUMBER))
    (slot longitude (type NUMBER))
    (slot quantity (type NUMBER))
)

(deftemplate allies
  (slot username(type STRING))
  (slot foraid(type STRING))
  (slot action (type STRING))
  (slot quantity (type NUMBER))
)

(deffunction computeservice
      (?a ?b)
      (/ (* ?a ?b) 100 )
)

(deftemplate disaster
    (slot hazard (type STRING))
    (slot latitude (type NUMBER))
    (slot longitude (type NUMBER))
    (slot span (type NUMBER))
)

(defrule invoke1
    ?addr1 <- (entity (aid ?d1) (latitude ?d2) (longitude ?d3) (quantity ?d4))
        =>
        (python-call invoke_entity ?d1 ?d2 ?d3 ?d4)
        (retract ?addr1)
)

(defrule invoke2
  ?addr2 <- (allies (username ?nm) (foraid ?fd) (action "Alert") (quantity ?q))
  =>
  (python-call invoke_useralert ?nm ?fd ?q)
  (retract ?addr2)
)

(defrule invoke3
  ?addr3 <- (allies (username ?nm) (foraid ?fd) (action "Allocate") (quantity ?qt))
  =>
  (python-call invoke_user_allocate ?nm ?fd ?qt)
  (retract ?addr3)
)
(defrule invoke4
  ?addr7 <- (allies (username ?nm) (foraid ?) (action "Allocated") (quantity ?))
            (DeallocateAll)
  =>
  (python-call invoke_user_deallocate ?nm)
  (retract ?addr7)
)

(defrule message
  ?addr4 <- (Message ?m)
  =>
  (python-call invoke_message ?m)
  (retract ?addr4)
)

(defrule display1
       (disaster (hazard ?d1) (latitude ?d2) (longitude ?d3) (span ?d4))
       =>
       (python-call display_disaster ?d1 ?d2 ?d3 ?d4))

(defrule requirement1
         (disaster (hazard "Earthquake"|"Flood"|"Tsunami") (latitude ?lat) (longitude ?long) (span ?pop))
         =>
         (assert (entity (aid "Volunteer")
                         (latitude ?lat)
                         (longitude ?long)
                         (quantity (computeservice ?pop 15))))
         (assert (entity (aid "Transport-Human")
                         (latitude ?lat)
                         (longitude ?long)
                         (quantity 0)))
         (assert (entity (aid "Accommodation")
                         (latitude ?lat)
                         (longitude ?long)
                         (quantity 0)))
         (assert (entity (aid "Hospital")
                         (latitude ?lat)
                         (longitude ?long)
                         (quantity 1)))
         (assert (check_prone_area ?lat ?long))
)

(defrule requirement2
         (disaster (hazard "Fire") (latitude ?lat) (longitude ?long) (span ?pop))
         =>
         (assert (entity (aid "Volunteer")
                         (latitude ?lat)
                         (longitude ?long)
                         (quantity 0)))
         (assert (entity (aid "Transport-Human")
                         (latitude ?lat)
                         (longitude ?long)
                         (quantity 0)))
         (assert (entity (aid "Accommodation")
                         (latitude ?lat)
                         (longitude ?long)
                         (quantity 0)))
         (assert (entity (aid "Hospital")
                         (latitude ?lat)
                         (longitude ?long)
                         (quantity 1)))
        (assert (entity (aid "FireEngine")
                        (latitude ?lat)
                        (longitude ?long)
                        (quantity 1)))
)

(defrule requirement3
         (disaster (hazard "Accident") (latitude ?lat) (longitude ?long) (span ?pop))
         =>
         (assert (entity (aid "Ambulance")
                         (latitude ?lat)
                         (longitude ?long)
                         (quantity 1)))
         (assert (entity (aid "Hospital")
                         (latitude ?lat)
                         (longitude ?long)
                         (quantity 0)))

)

(defrule requirement4
         (disaster (hazard "Cyclone") (latitude ?lat) (longitude ?long) (span ?pop))
         =>
         (assert (entity (aid "Volunteer")
                          (latitude ?lat)
                          (longitude ?long)
                          (quantity 0)))
         (assert (entity (aid "Transport-Human")
                          (latitude ?lat)
                          (longitude ?long)
                          (quantity 0)))
         (assert (entity (aid "Accommodation")
                          (latitude ?lat)
                          (longitude ?long)
                          (quantity 0)))
)

(defrule requirement5
         (disaster (hazard "Explosion") (latitude ?lat) (longitude ?long) (span ?pop))
         =>
         (assert (entity (aid "Hospital")
                          (latitude ?lat)
                          (longitude ?long)
                          (quantity 1)))
         (assert (entity (aid "Fireengine")
                          (latitude ?lat)
                          (longitude ?long)
                          (quantity 1)))
         (assert (entity (aid "Ambulance")
                          (latitude ?lat)
                          (longitude ?long)
                          (quantity 1)))
)

(defrule requirement6
         (disaster (hazard "FactoryLeak") (latitude ?lat) (longitude ?long) (span ?pop))
         =>
         (assert (disaster (hazard "displace")
                          (latitude ?lat)
                          (longitude ?long)
                          (span ?pop)))
         (assert (entity (aid "Volunteer")
                          (latitude ?lat)
                          (longitude ?long)
                          (quantity 0)))
)

(defrule displacement
  (disaster (hazard "displace") (latitude ?lat) (longitude ?long) (span ?pop))
  =>
  (assert (entity (aid "Transport-Human")
                  (latitude ?lat)
                  (longitude ?long)
                  (quantity ?pop)))
  (assert (entity (aid "Accommodation")
                  (latitude ?lat)
                  (longitude ?long)
                  (quantity ?pop)))
)

(defrule pronearea
  ?addr6 <-  (check_prone_area ?lat ?long)
  =>
    (python-call invoke_pronearea ?lat ?long)
    (retract ?addr6)
)

(defrule AlertPronearea
  ?addr5 <- (allies (username ?nm) (foraid "ProneArea") (action "AlertArea") (quantity ?d4) )
  =>
  (python-call invoke_alert_area ?nm ?d4)
  (retract ?addr5)
)
