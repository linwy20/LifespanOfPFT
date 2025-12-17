PROGRAM main

! This file presents key LAI correction process.
                                             
pftname = (/"not_vegetated                           ", &
            "needleleaf_evergreen_temperate_tree     ", &
            "needleleaf_evergreen_boreal_tree        ", &
            "needleleaf_deciduous_boreal_tree        ", &
            "broadleaf_evergreen_tropical_tree       ", &
            "broadleaf_evergreen_temperate_tree      ", &
            "broadleaf_deciduous_tropical_tree       ", &
            "broadleaf_deciduous_temperate_tree      ", &
            "broadleaf_deciduous_boreal_tree         ", &
            "broadleaf_evergreen_temperate_shrub     ", &
            "broadleaf_deciduous_temperate_shrub     ", &
            "broadleaf_deciduous_boreal_shrub        ", &
            "c3_arctic_grass                         ", &
            "c3_non-arctic_grass                     ", &
            "c4_grass                                ", &
            "c3_crop                                 "/) 

lls = (/1., 4.10, 3.15, 1., 1.72, 2.15, 1., 1., 1., 1.59, 1., 1., 1., 1., 1., 1./)


DO ipft=1,pfts,1 
   IF (SUM(snowtimes)==0) CYCLE

   ! max and min of remote-sensing based pftlai
   lairsmax = MAXVAL(pftlai(j,i,ipft,:))
   lairsmin = MINVAL(pftlai(j,i,ipft,:))

   lailfsp = (1. - 1./lls(ipft))*lairsmax
   IF ( lls(ipft) > 1. .and. lailfsp > lairsmin .and. lairsmax > 0) THEN
      pftlaitmp(:) = (pftlai(j,i,ipft,:)-lairsmin) / (lairsmax-lairsmin) * (lairsmax - lailfsp) + lailfsp
      pftlai(j,i,ipft,:) = pftlaitmp(:)
   ENDIF
ENDDO

sum_judg = SUM(pctpft)
IF (sum_judg > 0) THEN
   DO iloop=1,12
      lclai(j,i,iloop) = SUM( pctpft(:)*pftlai(j,i,:,iloop) )
   ENDDO
ELSE
   lclai(j,i,:) = laitot(:)
ENDIF

END PROGRAM main
