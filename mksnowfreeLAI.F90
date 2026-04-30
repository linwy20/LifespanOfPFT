PROGRAM main

!=======================================================================
! 
! gfortran -mcmodel=large -fbounds-check -g -o mksnowfreeLAI mksnowfreeLAI.F90 -I/usr/include -lnetcdf -lnetcdff
! 
!=======================================================================

USE netcdf
USE omp_lib

IMPLICIT NONE

INTEGER  :: i_omp,num_threads

INTEGER , parameter :: r8 = selected_real_kind(12)
INTEGER , parameter :: xydim = 1200, pfts = 16, mon = 12
INTEGER , parameter :: day = 46

CHARACTER(len=*), parameter :: Title      = "500m land vegetation and surface mapping data"
CHARACTER(len=*), parameter :: Resolution = "15 seconds, 0.0041667 degree, 1200x1200 (lonxlat) regional"
CHARACTER(len=*), parameter :: Coordinate = "Geographic, degrees longitude and latitude"
CHARACTER(len=*), parameter :: Authors    = "Yongjiu Dai group at Sun Yat-sen University"
CHARACTER(len=*), parameter :: Address    = "School of Atmospheric Sciences, Sun Yat-sen University, Zhuhai, China"
CHARACTER(len=*), parameter :: Contact    = "Wanyi Lin (lingy9@mail2.sysu.edu.cn); Hua Yuan (yuanh25@mail.sysu.edu.cn)"
CHARACTER(len=*), parameter :: LAI4G_Source = "Cao et al. 2023, doi: 10.5194/essd-2023-68"

INTEGER , dimension(12, 5) :: idx, wgt
INTEGER , dimension(46)    :: days
INTEGER , dimension(12)    :: mons
INTEGER , dimension(16)    :: pftnum
REAL(r8), dimension(16)    :: laimax, saimin, sairtn, saimin1, saires, pctpft
REAL(r8), dimension(16,12) :: laiini, saiini, saiini1, saiini2, laidiff

! output data
REAL(r8), dimension(1200)            :: lats, lons
REAL(r8), dimension(1200,1200,12)    :: lclai, lcsai
REAL(r8), dimension(1200,1200,16)    :: ppft
REAL(r8), dimension(1200,1200,16,12) :: pftlai, pftsai


CHARACTER (len=255) :: GLC_DIR      = "/stu01/linwy20/MKPFT30m/DomGlc500m/"
CHARACTER (len=255) :: LAI4G_DIR    = "/stu01/linwy20/hard/LAI/LAI4g/reg5x5/"
CHARACTER (len=255) :: RAW_DIR      = "/tera12/yuanhua/mksrf/raw_5x5/"
CHARACTER (len=255) :: PFT500m_DIR  = '/stu01/linwy20/MKPFT30m/PFT500m_16types/'
CHARACTER (len=255) :: LSAI_DIR     = '/stu01/linwy20/MKPFT30m/plant15s_RsPhe/'
CHARACTER (len=255) :: RATIO_DIR    = "/stu01/linwy20/MKPFT30m/mkratio/lutfill_with_nan/"
CHARACTER (len=255) :: snowQC_DIR   = "/stu01/linwy20/PFTLAI/LAIRatioLfsp/snowCover/snowCoverDay5deg/"
CHARACTER (len=255) :: LNMS_DIR     = "/home/yuanhua/tera12/data/CoLMrawdata/landcover/landmask/"
CHARACTER (len=255) :: OUT_DIR    = "/stu01/linwy20/MKPFT30m/plant15s_Snwfr/"

INTEGER :: iyear, argn
CHARACTER (len=4)   :: year     = "2000"
CHARACTER (len=6)   :: csreglat, cereglat, csreglon, cereglon
CHARACTER (len=255) :: filename, reg1, reg2, reg3, reg4

INTEGER  :: reglat, reglon, reglon_, sreglat, sreglon, ereglat, ereglon
LOGICAL  :: fileExists, outExists

CHARACTER (len=255), dimension(16) :: pftname

! input vars
INTEGER        , dimension(4)            :: reg
! RAW data
INTEGER(kind=2), dimension(1200,1200,46) :: laidata
INTEGER(kind=2), dimension(1200,1200,12) :: lai4gdata
REAL(r8)       , dimension(1200,1200,16) :: pctpft500

! PFT data
REAL(r8) :: sumpctpft
REAL(r8) :: lailfsp,lairsmin,lairsmax
REAL(r8), dimension(16)  :: lls

REAL(r8), dimension(12) :: pftlaitmp
INTEGER , dimension(1200,1200,12) :: snowdaydata
INTEGER, dimension(1200,1200,12) :: lclai500, lcsai500
INTEGER, dimension(1200,1200,16,12) :: pftlai500, pftsai500
INTEGER , dimension(12) :: snowday
INTEGER  :: regplaiid, snowdayid, lclaiid, lcsaiid, pctpftid, pftlaiid, pftsaiid

! vars id
INTEGER :: ncid, laiid
INTEGER :: lai4gid
INTEGER :: clai_id, csai_id, dims, &
           lat_dimid, lat_vid, lon_dimid, lon_vid, mon_dimid, &
           mon_vid, pft_dimid, pft_vid, plai_id, psai_id

! vars
INTEGER  :: i, j, imonth, iloop, inx, ipft
REAL(r8), dimension(46) :: lai
REAL(r8), dimension(12) :: laitot

REAL(r8) :: dll, x1, x2, sum_judg



! index of 46 8-day's data
idx(1,:)  = (/ 1,  2,  3,  4,  0/)
idx(2,:)  = (/ 4,  5,  6,  7,  8/)
idx(3,:)  = (/ 8,  9, 10, 11, 12/)
idx(4,:)  = (/12, 13, 14, 15,  0/)
idx(5,:)  = (/16, 17, 18, 19,  0/)
idx(6,:)  = (/19, 20, 21, 22, 23/)
idx(7,:)  = (/23, 24, 25, 26, 27/)
idx(8,:)  = (/27, 28, 29, 30, 31/)
idx(9,:)  = (/31, 32, 33, 34, 35/)
idx(10,:) = (/35, 36, 37, 38,  0/)
idx(11,:) = (/39, 40, 41, 42,  0/)
idx(12,:) = (/42, 43, 44, 45, 46/)

! weights of 8-day's data
wgt(1,:)  = (/8, 8, 8, 7, 0/)
wgt(2,:)  = (/1, 8, 8, 8, 3/)
wgt(3,:)  = (/5, 8, 8, 8, 2/)
wgt(4,:)  = (/6, 8, 8, 8, 0/)
wgt(5,:)  = (/8, 8, 8, 7, 0/)
wgt(6,:)  = (/1, 8, 8, 8, 5/)
wgt(7,:)  = (/3, 8, 8, 8, 4/)
wgt(8,:)  = (/4, 8, 8, 8, 3/)
wgt(9,:)  = (/5, 8, 8, 8, 1/)
wgt(10,:) = (/7, 8, 8, 8, 0/)
wgt(11,:) = (/8, 8, 8, 6, 0/)
wgt(12,:) = (/2, 8, 8, 8, 5/)

DO i=1,46,1
   days(i) = i
ENDDO

DO i=1,12,1
   mons(i) = i
ENDDO

DO i=1,16,1
   pftnum(i) = i-1
ENDDO

!PFT names                                                 !laimax ind  sgdd tbase SAImin minfr
pftname = (/"not_vegetated                           ", &  !  0     0      0   0     0.    0.
            "needleleaf_evergreen_temperate_tree     ", &  !  5     1      0   0     1.    0.7
            "needleleaf_evergreen_boreal_tree        ", &  !  5     2      0   0     1.    0.7
            "needleleaf_deciduous_boreal_tree        ", &  !  5     3    100   2     1.    0.
            "broadleaf_evergreen_tropical_tree       ", &  !  7     4      0   0     1.    0.8
            "broadleaf_evergreen_temperate_tree      ", &  !  7     5      0   0     1.    0.8
            "broadleaf_deciduous_tropical_tree       ", &  !  5     6      0   0     1.    0.
            "broadleaf_deciduous_temperate_tree      ", &  !  5     7    200   5     1.    0.
            "broadleaf_deciduous_boreal_tree         ", &  !  5     8    200   5     1.    0.
            "broadleaf_evergreen_temperate_shrub     ", &  !  4     9      0   0     1.    0.
            "broadleaf_deciduous_temperate_shrub     ", &  !  4    10    100   5     1.    0.
            "broadleaf_deciduous_boreal_shrub        ", &  !  4    11    100   5     1.    0.
            "c3_arctic_grass                         ", &  !  4    12    100   5     1.    0.
            "c3_non-arctic_grass                     ", &  !  4    13    100   5     1.    0.
            "c4_grass                                ", &  !  4    14    100   5     1.    0.
            "c3_crop                                 "/)   !  4    15    100   5     0.1   0.

! values in the table below are from Lawrence et al., 2007 (Table 1)
! with modifications according to Sitch et al., 2003 (Table 1,3)
laimax = (/0, 5, 5, 5, 7, 7, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4/)
saimin = (/0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0.1/) ! PFT SAI min
sairtn = (/0., 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, &
           0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0./) ! PFT SAI Retain

! =================== leaf lifespan ===================
lls = (/1., 4.10, 3.15, 1., 1.72, 2.15, 1., 1., 1., 1.59, 1., 1., 1., 1., 1., 1./)
! =================== leaf lifespan ===================


laiini(:,:) = 0.

! get args from command line
argn = IARGC()
IF (argn > 1) THEN
   CALL getarg(1, year)
   CALL getarg(2, csreglat)
   CALL getarg(3, csreglon)
   CALL getarg(4, cereglat)
   CALL getarg(5, cereglon)
ENDIF
read(year, *) iyear
print*,'year=', year, ', iyear=', iyear

read(csreglat,*) sreglat
read(cereglat,*) ereglat
read(csreglon,*) sreglon
read(cereglon,*) ereglon
print*,'sreglat=', sreglat
print*,'ereglat=', ereglat
print*,'sreglon=', sreglon
print*,'ereglon=', ereglon


! start loop regions
print *, ">>> start looping regions..."
DO reglat = sreglat, ereglat, -5
   DO reglon_ = sreglon, ereglon, 5

      reglon = reglon_
      ! IF lon > 180, revise it to nagative value
      IF (reglon_ >= 180) reglon = reglon_ - 360
      reg(1) = reglat
      reg(2) = reglon
      reg(3) = reglat - 5
      reg(4) = reglon + 5

      ! get region file name and open nc file
      write(reg1, "(i4)") reg(1)
      write(reg2, "(i4)") reg(2)
      write(reg3, "(i4)") reg(3)
      write(reg4, "(i4)") reg(4)

      ! 检查区域是否已经做过
      filename = trim(OUT_DIR)//'RG_' &
               //trim(adjustL(reg1))//'_' &
               //trim(adjustL(reg2))//'_' &
               //trim(adjustL(reg3))//'_' &
               //trim(adjustL(reg4))//'.' &
               //'LSAI500m.'//trim(year)//'.nc'
      inquire (file=filename, exist=outExists)
      print *, ''
      print *, ">>> Checking output file "//trim(filename)//" ..."

      ! 检查未校正数据是否存在
      filename = trim(LSAI_DIR)//trim(year)//'/'//'RG_' &
               //trim(adjustL(reg1))//'_' &
               //trim(adjustL(reg2))//'_' &
               //trim(adjustL(reg3))//'_' &
               //trim(adjustL(reg4))//'.' &
               //'LSAI500m.'//trim(year)//'.nc'
      inquire (file=filename, exist=fileExists)
      print *, ">>> Checking PFT file ", trim(filename), " ..."

      IF (fileExists .and. .not.(outExists)) THEN
         print*, 'Region exist and output dir not appear!'
      ELSE
         print*, 'Region not exist All zero value assumed! Please Check!', &
         'OR file already been created! Please Check!'
         CYCLE
      ENDIF



      ! Read snow cover information from MCD15A2H ExtraQC flag
      filename = trim(snowQC_DIR)//'RG_' &
         //trim(adjustL(reg1))//'_' &
         //trim(adjustL(reg2))//'_' &
         //trim(adjustL(reg3))//'_' &
         //trim(adjustL(reg4))//'.' &
         //'SnowDay.2005.nc'

      inquire (file=filename, exist=fileExists)
      print *, ">>> Checking snowday file ", trim(filename), " ..."

      IF (fileExists) THEN
         CALL check( nf90_open(trim(filename), nf90_nowrite, ncid) )
         CALL check( nf90_inq_varid(ncid, 'snow'   , snowdayid  ) )
         CALL check( nf90_get_var  (ncid, snowdayid, snowdaydata) )
         CALL check( nf90_close(ncid) )
      ELSE
         print*, 'snowday file not exist, snowday=0. Used ./mkplant15s.rsphe. CYCLE'
         CYCLE
      ENDIF


      dll = (reg(4)-reg(2))*1./(xydim*1.)

      DO dims=1,xydim
         lons(dims) = reg(2) + dims*dll - dll/2
         lats(dims) = reg(1) - dims*dll + dll/2
      ENDDO


      ! Raw file 除了LAI，都是气候态数据，所以 2000 以前的，可以固定读某个年份的 Raw file
      IF (iyear < 2000) THEN
         filename = trim(RAW_DIR)//'RG_'&
            //trim(adjustL(reg1))//'_' &
            //trim(adjustL(reg2))//'_' &
            //trim(adjustL(reg3))//'_' &
            //trim(adjustL(reg4))//'.' &
            //'RAW2005.nc'
      ELSE
         filename = trim(RAW_DIR)//'RG_'&
            //trim(adjustL(reg1))//'_' &
            //trim(adjustL(reg2))//'_' &
            //trim(adjustL(reg3))//'_' &
            //trim(adjustL(reg4))//'.' &
            //'RAW'//trim(year)//'.nc'
      ENDIF

      print *, ">>> Processing file ", trim(filename), " ..."
      CALL check( nf90_open(trim(filename), nf90_nowrite, ncid) )

      CALL check( nf90_inq_varid(ncid, 'LAI' , laiid   ) )
      CALL check( nf90_get_var  (ncid, laiid , laidata ) )

      CALL check( nf90_close(ncid) )
      print*, 'raw data read completed'


      ! ======================== 读 LAI 4G ==========================
      IF (iyear < 2004) THEN
         filename = trim(LAI4G_DIR)//'RG_' &
            //trim(adjustL(reg1))//'_' &
            //trim(adjustL(reg2))//'_' &
            //trim(adjustL(reg3))//'_' &
            //trim(adjustL(reg4))//'.LAI4G.' &
            //trim(year)//'.nc'

         print *, ">>> Processing file ", trim(filename), " ..."
         CALL check( nf90_open(trim(filename), nf90_nowrite, ncid) )

         CALL check( nf90_inq_varid(ncid, 'LAI'  , lai4gid  ) )
         CALL check( nf90_get_var  (ncid, lai4gid, lai4gdata) )

         CALL check( nf90_close(ncid) )
         print*, 'LAI4G 500m data read completed'
      ENDIF


      ! ======================= 读 500m PFT =========================
      filename = trim(PFT500m_DIR)//trim(year)//'/'//'RG_' &
         //trim(adjustL(reg1))//'_' &
         //trim(adjustL(reg2))//'_' &
         //trim(adjustL(reg3))//'_' &
         //trim(adjustL(reg4))//'.PFT500m.' &
         //trim(year)//'.nc'
      print *, ">>> Checking "//trim(filename), " ..."
      CALL check( nf90_open(trim(filename), nf90_nowrite, ncid) )

      CALL check( nf90_inq_varid(ncid, 'PCT_PFT'        ,pctpftid    ) )
      CALL check( nf90_get_var  (ncid, pctpftid         ,pctpft500   ) )

      CALL check( nf90_close(ncid) )

      print*, '500m PCT_PFT read completed'


      ! ======================= 读 500m LSAI =========================
      filename = trim(LSAI_DIR)//trim(year)//'/'//'RG_' &
         //trim(adjustL(reg1))//'_' &
         //trim(adjustL(reg2))//'_' &
         //trim(adjustL(reg3))//'_' &
         //trim(adjustL(reg4))//'.LSAI500m.' &
         //trim(year)//'.nc'
      print *, ">>> Checking "//trim(filename), " ..."
      CALL check( nf90_open(trim(filename), nf90_nowrite, ncid) )

      CALL check( nf90_inq_varid(ncid, 'MONTHLY_LC_LAI' , lclaiid    ) )
      CALL check( nf90_get_var  (ncid, lclaiid          , lclai500   ) )

      CALL check( nf90_inq_varid(ncid, 'MONTHLY_LC_SAI' , lcsaiid    ) )
      CALL check( nf90_get_var  (ncid, lcsaiid          , lcsai500   ) )

      CALL check( nf90_inq_varid(ncid, 'MONTHLY_PFT_LAI', pftlaiid   ) )
      CALL check( nf90_get_var  (ncid, pftlaiid         , pftlai500  ) )

      CALL check( nf90_inq_varid(ncid, 'MONTHLY_PFT_SAI', pftsaiid   ) )
      CALL check( nf90_get_var  (ncid, pftsaiid         , pftsai500  ) )

      CALL check( nf90_close(ncid) )

      print*, 'LSAI500m data read completed'


      ppft    (:,:,:)   = pctpft500  ! 读入16类pft的绝对数值 -> ppft
      lclai   (:,:,:)   = lclai500  * 0.1
      lcsai   (:,:,:)   = lcsai500  * 0.1
      pftlai  (:,:,:,:) = pftlai500 * 0.1
      pftsai  (:,:,:,:) = pftsai500 * 0.1

      print*, 'Start to process region: ', reg

      DO j=1,xydim,1
         DO i=1,xydim,1

            IF (sum(pftlai(j,i,:,:))==0 .and. sum(pftsai(j,i,:,:))==0) CYCLE

            ! 2024年10月22日 更新: 增加snow cover信息, 如果雪存在才用lifespan调整
            snowday = snowdaydata(j,i,:)
            IF (sum(snowday)==0) CYCLE ! 12个月都没有雪


            ! Read grid LAI
            ! ------------------------
            IF (iyear>=2004) THEN
               ! covert 8-day lai to monthly lai. loop for each month

               lai(:) = laidata(j,i,:)*0.1_r8
               laitot = (/1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12./)

               DO imonth=1,12,1
                 IF (imonth==1 .or. imonth==4 .or. imonth==5 .or. imonth==10 .or. imonth==11) THEN
                    laitot(imonth) = sum(lai(idx(imonth,1:4))*wgt(imonth,1:4))/ &
                                     sum(wgt(imonth,1:4))  !need check for nan
                 ELSE
                    laitot(imonth) = sum(lai(idx(imonth,:))*wgt(imonth,:))/ &
                                     sum(wgt(imonth,:))  !need check for nan
                 ENDIF
               ENDDO
            
            ELSE
               laitot = lai4gdata(j,i,:)*0.1_r8
            ENDIF


            ! scale to 100% for vegetation area
            sumpctpft = sum(ppft(j,i,:))
            pctpft(:) = ppft(j,i,:)/sumpctpft

            ! initial LAI
            laiini(:,:) = pftlai(j,i,:,:)

            ! IF (j==538 .and. i==1) print*, 'debug 502: laiini = pftlai:', laiini(:,1)
            IF (j==1 .and. i==1) print'(A, 16F8.3)', 'debug 437: June pftlai(j,i,:,6) = ', pftlai(j,i,:,6)

            ! snow-free correction for PFTLAI
            DO ipft=1,pfts,1 
               ! max and min of remote-sensing based pftlai
               lairsmax = maxval(pftlai(j,i,ipft,:))
               lairsmin = minval(pftlai(j,i,ipft,:))

               lailfsp = (1. - 1./lls(ipft))*lairsmax
               IF ( lls(ipft) > 1. .and. lailfsp > lairsmin .and. lairsmax > 0) THEN
                  pftlaitmp(:) = (pftlai(j,i,ipft,:)-lairsmin) / (lairsmax-lairsmin) * (lairsmax - lailfsp) + lailfsp
                  pftlai(j,i,ipft,:) = pftlaitmp(:)
               ENDIF
            ENDDO
            IF (j==1 .and. i==1) print'(A, 16F8.3)', 'debug 451: June pftlai(j,i,:,6) = ', pftlai(j,i,:,6)

            ! calculate SAI
            ! --------------------
            DO ipft=1,pfts,1
               saimin1(ipft) = saimin(ipft)*maxval(laiini(ipft,:))
            ENDDO
            saimin1(2:16)= saimin1(2:16)/laimax(2:16) ! Lawrence2007 eqa(7):scaling of minimum PFT SAI

            saiini (:,:) = 0.
            saiini1(:,:) = saiini(:,:)

            DO iloop=1,12
               saiini1(:,iloop) = saimin(:)
            ENDDO

            ! ----计算 (前一个月的LAI - 后一个月的LAI), 且保证不低于0----
            laiini(:,:) = pftlai(j,i,:,:)
            laidiff(:,1) = laiini(:,12) - laiini(:,1) ! PFT LAI diff: 失去的叶
            DO iloop=1,11,1
               inx = iloop+1
               laidiff(:,inx) = laiini(:,iloop) - laiini(:,inx)
            ENDDO

            WHERE(laidiff<0.) laidiff=0.
            ! ----计算 (前一个月的LAI - 后一个月的LAI), 且保证不低于0----

            iloop = 1
            DO WHILE (iloop<13)
               saires(:) = sairtn*saiini1(:,mod( (iloop+10), 12 ) + 1) ! L.2007 eqa(9):PFT SAI Retention Rate × PFT SAI PREV
               DO inx=1,16
                  x1 = (saires(inx) + laidiff(inx,iloop)*0.5) ! L.2007 eqa(10): 增加系数枯叶保存率=0.5
                  x2 = saimin1(inx)
                  saiini(inx,iloop) = max(x1,x2) !maxval((saires(:)+laidiff(:,imonth)*0.5), saimin1())
               ENDDO
               iloop = iloop + 1

               IF (iloop == 13) THEN
                  sum_judg = abs(sum(saiini-saiini1))
                  IF (sum_judg > 1e-6) THEN
                     iloop  = 1
                     saiini1(:,:) = saiini(:,:)
                  ENDIF
               ENDIF
            ENDDO


            ! max LAI value limited (need more test and check)
            IF (count(laiini>10.)>0) THEN
               ! WHERE (laiini>10.) laiini=10.
               print'(A, 2I3)', 'error : laiini > 10. j, i = ', j, i
               print*, laiini(:,6)
               stop
            ENDIF

            ! output data
            pftlai(j,i,:,:) = laiini(:,:)

            sum_judg = sum(pctpft)
            IF (sum_judg > 0) THEN
               ! IF (j==538 .and. i==1) print*, 'debug607: sum_judg:', sum_judg
               DO iloop=1,12
                  lclai(j,i,iloop) = sum( pctpft(:)*laiini(:,iloop) )
               ENDDO
            ELSE
               ! IF (j==538 .and. i==1) print*, 'debug612: sum_judg:', sum_judg
               lclai(j,i,:) = laitot(:)
            ENDIF

 
            IF (minval(lclai(j,i,:)-laitot(:)) < -1) THEN

               ! IF (j==538 .and. i==1) print*, 'debug693: laitot(:):', laitot(:)

               ! 如果 遥感物候LAI 被重新赋值，积雪校正LAI未被重新赋值，会显示前者的lclai更大，如RG_60_-125, 2005
               lclai(j,i,:) = laitot(:)
               
               IF (abs(sum(pctpft)-1.) > 1e-5) THEN
                  print*, 'ERROR: sumpctpft != 1'
                  STOP
               ENDIF
            ENDIF

            pctpft(:) = ppft(j,i,:)/sumpctpft

            DO ipft=1,16,1
               IF (pctpft(ipft) < 1e-6) THEN
                  laiini(ipft,:) = 0. ! 遥感物候和积雪校正代码已经能保证
                  saiini(ipft,:) = 0.
               ENDIF
            ENDDO

            IF (count(laiini>20) > 0) THEN
               print*, 'check for laiini!'
               STOP
            ENDIF

            ! max SAI value limited
            IF (count(saiini>3) > 0) THEN
               WHERE(saiini>3.) saiini = 3.
            ENDIF

            ! output data
            pftsai(j,i,:,:) = saiini(:,:)

            sum_judg = sum(pctpft)

            IF (sum_judg > 0) THEN
               DO iloop=1,12
                  lcsai(j,i,iloop) = sum( pctpft(:)*saiini(:,iloop) )
               ENDDO
            ELSE
               DO iloop=1,12
                  saiini2(:,iloop) = pctpft(:)*saiini(:,iloop)
               ENDDO

               DO iloop=1,12
                  lcsai(j,i,iloop) = sum(saiini2(:,iloop)) 
               ENDDO
            ENDIF


         ENDDO
      ENDDO

      print*,'max=',maxval(pftlai), 'min=',minval(pftlai)


      ! --------- output lsai -----------
      lclai  = nint(lclai  * 10.0_r8)
      lcsai  = nint(lcsai  * 10.0_r8)
      pftlai = nint(pftlai * 10.0_r8)
      pftsai = nint(pftsai * 10.0_r8)


      filename = trim(OUT_DIR)//'RG_' &
               //trim(adjustL(reg1))//'_' &
               //trim(adjustL(reg2))//'_' &
               //trim(adjustL(reg3))//'_' &
               //trim(adjustL(reg4))//'.' &
               //'LSAI500m.'//trim(year)//'.nc'

      print*, ">>> writing out "//trim(filename)//" ..."
      CALL check( nf90_create(filename, NF90_NETCDF4, ncid) )

      ! define dimensions
      CALL check( nf90_def_dim(ncid, "lat", xydim, lat_dimid) )
      CALL check( nf90_def_dim(ncid, "lon", xydim, lon_dimid) )
      CALL check( nf90_def_dim(ncid, "pft", pfts , pft_dimid) )
      CALL check( nf90_def_dim(ncid, "mon", mon  , mon_dimid) )

      ! define variables
      ! ---------------------------------------
      CALL check( nf90_def_var(ncid, "lat", NF90_FLOAT, lat_dimid, lat_vid, deflate_level=6) )
      CALL check( nf90_def_var(ncid, "lon", NF90_FLOAT, lon_dimid, lon_vid, deflate_level=6) )
      CALL check( nf90_def_var(ncid, "pft", NF90_INT  , pft_dimid, pft_vid, deflate_level=6) )
      CALL check( nf90_def_var(ncid, "mon", NF90_INT  , mon_dimid, mon_vid, deflate_level=6) )

      CALL check( nf90_put_att(ncid, lat_vid, "long_name", "Latitude at grid center" ) )
      CALL check( nf90_put_att(ncid, lat_vid, "units"    , "degrees_north"           ) )
      CALL check( nf90_put_att(ncid, lon_vid, "long_name", "Longitude at grid center") )
      CALL check( nf90_put_att(ncid, lon_vid, "units"    , "degrees_east"            ) )

      CALL check( nf90_put_att(ncid, pft_vid, "long_name", "Index of PFT"                        ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft00"    , "Not Vegetated"                       ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft01"    , "Needleleaf Evergreen Temperate Tree" ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft02"    , "Needleleaf Evergreen Boreal Tree"    ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft03"    , "Needleleaf Deciduous Boreal Tree"    ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft04"    , "Broadleaf Evergreen Tropical Tree"   ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft05"    , "Broadleaf Evergreen Temperate Tree"  ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft06"    , "Broadleaf Deciduous Tropical Tree"   ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft07"    , "Broadleaf Deciduous Temperate Tree"  ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft08"    , "Broadleaf Deciduous Boreal Tree"     ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft09"    , "Broadleaf Evergreen Shrub"           ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft10"    , "Broadleaf Deciduous Temperate Shrub" ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft11"    , "Broadleaf Deciduous Boreal Shrub"    ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft12"    , "C3 Arctic Grass"                     ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft13"    , "C3 Non-arctic Grass"                 ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft14"    , "C4 Grass"                            ) )
      CALL check( nf90_put_att(ncid, pft_vid, "pft15"    , "C3 Crop"                             ) )

      CALL check( nf90_put_att(ncid, mon_vid, "long_name", "Month of year") )
      CALL checK( nf90_put_att(ncid, mon_vid, "units"    , "month"        ) )

      CALL check( nf90_put_var(ncid, lat_vid, lats  ) )
      CALL check( nf90_put_var(ncid, lon_vid, lons  ) )
      CALL check( nf90_put_var(ncid, pft_vid, pftnum) )
      CALL check( nf90_put_var(ncid, mon_vid, mons  ) )

      CALL check( nf90_def_var(ncid, "MONTHLY_LC_LAI" , NF90_UBYTE  , (/lon_dimid, lat_dimid, mon_dimid/), &
         clai_id, deflate_level=6) )
      CALL check( nf90_put_att(ncid, clai_id          , "units"     , "m^2/m^2"    ) )
      CALL check( nf90_put_att(ncid, clai_id          , "scale_factor", 0.1        ) )
      CALL check( nf90_put_att(ncid, clai_id          , "long_name" , "Monthly landcover LAI values") )

      CALL check( nf90_def_var(ncid, "MONTHLY_LC_SAI" , NF90_UBYTE  , (/lon_dimid, lat_dimid, mon_dimid/), &
         csai_id, deflate_level=6) )
      CALL check( nf90_put_att(ncid, csai_id          , "units"     , "m^2/m^2"    ) )
      CALL check( nf90_put_att(ncid, csai_id          , "scale_factor", 0.1        ) )
      CALL check( nf90_put_att(ncid, csai_id          , "long_name" , "Monthly landcover SAI values") )

      CALL check( nf90_def_var(ncid, "MONTHLY_PFT_LAI", NF90_UBYTE  , (/lon_dimid, lat_dimid, pft_dimid, mon_dimid/), &
         plai_id, deflate_level=6) )
      CALL check( nf90_put_att(ncid, plai_id          , "units"     , "m^2/m^2"    ) )
      CALL check( nf90_put_att(ncid, plai_id          , "scale_factor", 0.1        ) )
      CALL check( nf90_put_att(ncid, plai_id          , "long_name" , "Monthly PFT LAI values") )

      CALL check( nf90_def_var(ncid, "MONTHLY_PFT_SAI", NF90_UBYTE  , (/lon_dimid, lat_dimid, pft_dimid, mon_dimid/), &
         psai_id, deflate_level=6) )
      CALL check( nf90_put_att(ncid, psai_id          , "units"     , "m^2/m^2"    ) )
      CALL check( nf90_put_att(ncid, psai_id          , "scale_factor", 0.1        ) )
      CALL check( nf90_put_att(ncid, psai_id          , "long_name" , "Monthly PFT SAI values") )

      ! put vars
      CALL check( nf90_inq_varid(ncid, "MONTHLY_LC_LAI" , clai_id ) )
      CALL check( nf90_put_var  (ncid, clai_id          , lclai   ) )
      CALL check( nf90_inq_varid(ncid, "MONTHLY_LC_SAI" , csai_id ) )
      CALL check( nf90_put_var  (ncid, csai_id          , lcsai   ) )
      CALL check( nf90_inq_varid(ncid, "MONTHLY_PFT_LAI", plai_id ) )
      CALL check( nf90_put_var  (ncid, plai_id          , pftlai  ) )
      CALL check( nf90_inq_varid(ncid, "MONTHLY_PFT_SAI", psai_id ) )
      CALL check( nf90_put_var  (ncid, psai_id          , pftsai  ) )

      CALL check( nf90_put_att(ncid, NF90_GLOBAL, 'Title'     , Title     ) )
      IF (iyear < 2004) THEN
         CALL check( nf90_put_att(ncid, NF90_GLOBAL, 'LAI4G_Source', LAI4G_Source) )
      ENDIF
      CALL check( nf90_put_att(ncid, NF90_GLOBAL, 'Resolution', Resolution) )
      CALL check( nf90_put_att(ncid, NF90_GLOBAL, 'Coordinate', Coordinate) )
      CALL check( nf90_put_att(ncid, NF90_GLOBAL, 'Authors'   , Authors   ) )
      CALL check( nf90_put_att(ncid, NF90_GLOBAL, 'Address'   , Address   ) )
      CALL check( nf90_put_att(ncid, NF90_GLOBAL, 'Contact'   , Contact   ) )

      CALL check( nf90_close(ncid) )


   ENDDO
ENDDO


CONTAINS

   SUBROUTINE check(status)
      INTEGER, intent(in) :: status

      IF (status /= nf90_noerr) THEN
         print *, trim( nf90_strerror(status))
         STOP 2
      ENDIF
   END SUBROUTINE check
END PROGRAM main
