      program driver
c
c  Generic driver routine for claw2
c
c  Author: Randall J. LeVeque
c  Version of March, 1999 --  CLAWPACK Version 4.0
c
c
      implicit double precision (a-h,o-z)

c     # set parameters for maximum array sizes used in declarations
c     # these must be increased for larger problems.
c
c
      parameter (maxmx =   600)
      parameter (maxmy =   600)
      parameter (mwork =  1122232)

      parameter (mbc = 2)
      parameter (meqn = 3)
      parameter (mwaves = 3)
      parameter (maux = 0)   

      dimension    q(1-mbc:maxmx+mbc, 1-mbc:maxmy+mbc, meqn)
c     dimension  aux(1-mbc:maxmx+mbc, 1-mbc:maxmy+mbc, maux)

      dimension mthlim(mwaves)
      dimension work(mwork)

      real etime          ! Declare the type of etime()
      real elapsed(2)     ! For receiving user and system time
      real total

      real elapsed2(2)     ! For receiving user and system time
      real total2

c
c
      total = etime(elapsed)
      call claw2ez(maxmx,maxmy,meqn,mwaves,mbc,maux,mwork,mthlim,
     &		 q,work,aux)
      total2 = etime(elapsed2)
      print *, 'End: total=',total2- total,
     &         ' user=', elapsed2(1)-elapsed(1),
     &         ' system=', elapsed2(2) -elapsed(2)
                      

      stop 
      end
