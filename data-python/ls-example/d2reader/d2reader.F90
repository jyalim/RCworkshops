! The module is necessary for the allocated arrays, otherwise f2py will struggle
! to compile. If allocated arrays are unnecessary or not in the original code,
! then the subroutine style after line 43 is sufficient.
module reader
  use iso_c_binding, only: c_double, c_int
  implicit none
  integer, parameter :: dp=kind(0.d0)
  integer  :: M,N
  integer  :: npm,npsteps
  real(dp) :: gam,Rn,Pr,asp,theta_deg,dt,time
  real(dp) :: omega,alpha_deg,rdt
  real(dp), allocatable, dimension(:)   :: x,y
  real(dp), allocatable, dimension(:,:) :: Dx,Dy
  real(dp), allocatable, dimension(:,:) :: u,v,T
  real(dp), allocatable, dimension(:,:) :: uo,vo,To
contains
  subroutine read_tilt_file(restart)
    implicit none
    integer,parameter       :: IN_FIELD_UNIT=1000
    character(*),intent(in) :: restart
    if ( allocated(x) ) call dealloc_arrays()
    open(unit=IN_FIELD_UNIT,file=restart,status='old',form='unformatted')
    read(IN_FIELD_UNIT) M,N
      allocate(x(0:M),y(0:N),source=0d0)
      allocate(Dx(0:M,0:M),Dy(0:N,0:N),source=0d0)
      allocate(u(0:M,0:N),source=0d0)
      allocate(v,T,uo,vo,To,source=u)
    read(IN_FIELD_UNIT) gam,Rn,Pr,asp,theta_deg,dt,time,npm
    call read_field(M,N,IN_FIELD_UNIT,uo)
    call read_field(M,N,IN_FIELD_UNIT, u)
    call read_field(M,N,IN_FIELD_UNIT,vo)
    call read_field(M,N,IN_FIELD_UNIT, v)
    call read_field(M,N,IN_FIELD_UNIT,To)
    call read_field(M,N,IN_FIELD_UNIT, T)
    close(IN_FIELD_UNIT)
    call cheb(M,asp,x,Dx)
    call cheb(N,2d0,y,Dy)
    return
  end subroutine read_tilt_file

  subroutine read_wobl_file(restart)
    implicit none
    integer,parameter       :: IN_FIELD_UNIT=1001
    character(*),intent(in) :: restart
    if ( allocated(x) ) call dealloc_arrays()
    open(unit=IN_FIELD_UNIT,file=restart,status='old',form='unformatted')
    read(IN_FIELD_UNIT) M,N
    allocate(x(0:M),y(0:N),source=0d0)
    allocate(Dx(0:M,0:M),Dy(0:N,0:N),source=0d0)
    allocate(u(0:M,0:N),source=0d0)
    allocate(v,T,uo,vo,To,source=u)
    read(IN_FIELD_UNIT) gam,Rn,Pr,asp,theta_deg,omega,alpha_deg,rdt,time,npsteps
    call read_field(M,N,IN_FIELD_UNIT,uo)
    call read_field(M,N,IN_FIELD_UNIT, u)
    call read_field(M,N,IN_FIELD_UNIT,vo)
    call read_field(M,N,IN_FIELD_UNIT, v)
    call read_field(M,N,IN_FIELD_UNIT,To)
    call read_field(M,N,IN_FIELD_UNIT, T)
    close(IN_FIELD_UNIT)
    call cheb(M,asp,x,Dx)
    call cheb(N,2d0,y,Dy)
    return
  end subroutine read_wobl_file

  subroutine write_wobl_file(restart)
    implicit none
    integer,parameter       :: OUT_FIELD_UNIT=1002
    character(*),intent(in) :: restart
    open(unit=OUT_FIELD_UNIT,file=restart,form='unformatted')
    write(OUT_FIELD_UNIT) M,N
    write(OUT_FIELD_UNIT) gam,Rn,Pr,asp,theta_deg,omega,alpha_deg,rdt,time,npsteps
    call write_field(M,N,OUT_FIELD_UNIT,uo)
    call write_field(M,N,OUT_FIELD_UNIT, u)
    call write_field(M,N,OUT_FIELD_UNIT,vo)
    call write_field(M,N,OUT_FIELD_UNIT, v)
    call write_field(M,N,OUT_FIELD_UNIT,To)
    call write_field(M,N,OUT_FIELD_UNIT, T)
    close(OUT_FIELD_UNIT)
    return
  end subroutine write_wobl_file

  subroutine dealloc_arrays()
    implicit none
    deallocate(x,y)
    deallocate(Dx,Dy)
    deallocate(u,v,T,uo,vo,To)
    return
  end subroutine dealloc_arrays
end module reader

subroutine read_field(M,N,in_unit,field)
  use iso_c_binding, only: c_double, c_int
  implicit none
  integer, parameter :: dp=kind(0.d0)
  integer,  intent(in)    :: M,N
  integer,  intent(in)    :: in_unit
  real(dp), intent(inout) :: field(0:M,0:N)
  integer :: k
  read(in_unit) (field(:,k),k=0,N)
  return
end subroutine read_field

subroutine write_field(M,N,out_unit,field)
  use iso_c_binding, only: c_double, c_int
  implicit none
  integer, parameter :: dp=kind(0.d0)
  integer,  intent(in)    :: M,N
  integer,  intent(in)    :: out_unit
  real(dp), intent(inout) :: field(0:M,0:N)
  integer :: k
  write(out_unit) (field(:,k),k=0,N)
  return
end subroutine write_field

subroutine cheb(L,asp,x,D)
  use iso_c_binding, only: c_double, c_int
  implicit none
  integer, parameter :: dp=kind(0.d0)
  real(dp),parameter :: pi=4d0*datan(1d0)
  integer,intent(in)                      :: L
  real(dp),intent(in)                     :: asp
  real(dp),dimension(0:L,0:L),intent(out) :: D
  real(dp),intent(out)                    :: x(0:L)
  real(dp) :: c(0:L),ic(0:L),dXI(0:L,0:L),sDT(0:L)
  integer  :: k
  ! = Zero initialization =============================================
  c=0d0; ic=0d0; D=0d0
  sDT = 0d0; dXI = 0d0
  ! = Compute domain, x ===============================================
  forall(k=0:L) x(k) = dcos(pi/L*k)
  ! = Compute derivative operator, D ==================================
  ! - Get barycentric weights, c --------------------------------------
  c=1d0; c(0)=2d0 ; c(L)=2d0;
  do k=1,L,2
    c(k) = -c(k)
  end do
  ! - Get inverse barycentric weights, ic -----------------------------
  ic = 1d0/c
  ! - compute dX + I --------------------------------------------------
  do k = 0,L
    ! - Get spatial metric (antisymmetric) ----------------------------
    dXI(:,k) = x - x(k)
    ! - Add identity to spatial metric --------------------------------
    dXI(k,k) = 1d0
  end do
  ! - compute first pass of D -----------------------------------------
  do k = 0,L
    D(:,k) = (c(:)*ic(k)) / dXI(:,k)
  end do
  ! - sum along the rows of current D transpose (columns of D) --------
  sDT = sum(D,2)
  ! - Update diagonal of D with SDT result ----------------------------
  do k = 0,L
    D(k,k) = D(k,k) - sDT(k)
  end do
  x = x / asp
  D = D * asp
  return
end subroutine cheb

subroutine partials(    M,     N,    &
                        x,     y,    &
                       Dx,    Dy,    &
                        u,     v, T, &
                     dudx,  dudy,    & 
                     dvdx,  dvdy,    &
                     dTdx,  dTdy,    &
                   d2Tdxx,d2Tdyy,    &
                       vorticity     &
  )
  use iso_c_binding, only: c_double, c_int
  implicit none
  integer, parameter   :: dp=kind(0.d0)
  integer,intent(in)                      :: M,N
  real(dp),intent(in)                     :: x(0:M)
  real(dp),intent(in)                     :: y(0:N)
  real(dp),dimension(0:M,0:N),intent(in)  :: T,u,v
  real(dp),dimension(0:M,0:M),intent(in)  :: Dx
  real(dp),dimension(0:N,0:N),intent(in)  :: Dy
  real(dp),dimension(0:M,0:N),intent(out) :: dudx,dudy
  real(dp),dimension(0:M,0:N),intent(out) :: dvdx,dvdy
  real(dp),dimension(0:M,0:N),intent(out) :: dTdx,dTdy
  real(dp),dimension(0:M,0:N),intent(out) :: d2Tdxx,d2Tdyy
  real(dp),dimension(0:M,0:N),intent(out) :: vorticity
  dudx   = 0d0; dudy   = 0d0
  dvdx   = 0d0; dvdy   = 0d0
  dTdx   = 0d0; dTdy   = 0d0
  d2Tdxx = 0d0; d2Tdyy = 0d0

  call compute_grad(M,N,Dx,Dy,T,dTdx,dTdy)
  call compute_grad(M,N,Dx,Dy,u,dudx,dudy)
  call compute_grad(M,N,Dx,Dy,v,dvdx,dvdy)

  call dgemm('n','n',M+1,N+1,M+1,1d0,Dx,M+1,dTdx,M+1,0d0,d2Tdxx,M+1)
  call dgemm('n','T',M+1,N+1,N+1,1d0,dTdy,M+1,Dy,N+1,0d0,d2Tdyy,M+1)

  vorticity = dvdx - dudy
  return
end subroutine partials

subroutine compute_grad(M,N,Dx,Dy,field,gradx,grady)
  use iso_c_binding, only: c_double, c_int
  implicit none
  integer, parameter   :: dp=kind(0.d0)
  integer, intent(in)  :: M,N
  real(dp), intent(in) :: Dx(0:M,0:M)
  real(dp), intent(in) :: Dy(0:N,0:N)
  real(dp), intent(in) :: field(0:M,0:N)
  real(dp), dimension(0:M,0:N), intent(out) :: gradx, grady
  !- x derivative -----------------------------------------------------------------
  call dgemm('n','n',M+1,N+1,M+1,1d0,Dx,M+1,field,M+1,0d0,gradx,M+1)
  !- y derivative -----------------------------------------------------------------
  call dgemm('n','T',M+1,N+1,N+1,1d0,field,M+1,Dy,N+1,0d0,grady,M+1)
  return
end subroutine compute_grad
