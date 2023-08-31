! The module is necessary for the allocated arrays, otherwise f2py will struggle
! to compile. If allocated arrays are unnecessary or not in the original code,
! then the subroutine style after line 43 is sufficient.
module reader
  use iso_c_binding, only: c_double, c_int
  implicit none
  integer, parameter :: dp=kind(0.d0)
  integer :: M,N,R
  integer :: npm
  real(dp) :: Rn,om,al,de,Pr,ax,az,dt,time
  real(dp), allocatable, dimension(:)     :: x,y,z
  real(dp), allocatable, dimension(:,:)   :: Dx,Dy,Dz
  real(dp), allocatable, dimension(:,:,:) :: u,v,w,T
  real(dp), allocatable, dimension(:,:,:) :: uo,vo,wo,To
contains
  subroutine read_file(restart)
    implicit none
    integer,parameter       :: IN_FIELD_UNIT=1000
    character(*),intent(in) :: restart
    open(unit=IN_FIELD_UNIT,file=restart,status='old',form='unformatted')
    read(IN_FIELD_UNIT) M,N,R
    allocate(x(0:M),y(0:N),z(0:R),source=0d0)
    allocate(Dx(0:M,0:M),Dy(0:N,0:N),Dz(0:R,0:R),source=0d0)
    allocate(u(0:M,0:N,0:R),source=0d0)
    allocate(v,w,T,uo,vo,wo,To,source=u)
    read(IN_FIELD_UNIT) Rn,om,al,de,Pr,ax,az,dt,npm,time
    call read_field(M,N,R,IN_FIELD_UNIT,uo)
    call read_field(M,N,R,IN_FIELD_UNIT, u)
    call read_field(M,N,R,IN_FIELD_UNIT,vo)
    call read_field(M,N,R,IN_FIELD_UNIT, v)
    call read_field(M,N,R,IN_FIELD_UNIT,wo)
    call read_field(M,N,R,IN_FIELD_UNIT, w)
    call read_field(M,N,R,IN_FIELD_UNIT,To)
    call read_field(M,N,R,IN_FIELD_UNIT, T)
    close(IN_FIELD_UNIT)
    call cheb(M,ax ,x,Dx)
    call cheb(N,2d0,y,Dy)
    call cheb(R,az ,z,Dz)
    return
  end subroutine read_file
end module reader

subroutine read_field(M,N,R,in_unit,field)
  use iso_c_binding, only: c_double, c_int
  implicit none
  integer, parameter :: dp=kind(0.d0)
  integer,  intent(in)    :: M,N,R
  integer,  intent(in)    :: in_unit
  real(dp), intent(inout) :: field(0:M,0:N,0:R)
  integer :: j,k
  do k = 0,R
    do j = 0,N
      read(in_unit) field(:,j,k)
    end do
  end do
  return
end subroutine read_field

subroutine cheb(L,asp,x,D)
  use iso_c_binding, only: c_double, c_int
  implicit none
  integer, parameter :: dp=kind(0.d0)
  integer,intent(in)                      :: L
  real(dp),intent(in)                     :: asp
  real(dp),dimension(0:L,0:L),intent(out) :: D
  real(dp),intent(out)                    :: x(0:L)
  real(dp),parameter :: pi=4d0*datan(1d0)
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
