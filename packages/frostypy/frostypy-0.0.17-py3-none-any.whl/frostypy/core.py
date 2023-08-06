# -*- coding: utf-8 -*-
"""
.. contents:: :local:

Dimensionless Numbers
---------------------
.. autofunction:: Properites
.. autofunction:: Fourier
.. autofunction:: Hatta
.. autofunction:: Jakob
.. autofunction:: Lewis
.. autofunction:: Nusselt
.. autofunction:: Reynolds
.. autofunction:: Sherwood

Dimensions
----------
.. autofunction:: thermal_conductivity

"""

import numpy
import CoolProp as cp
import warnings


__all__ = ['Fourier', 'Hatta', 'Jakob', 'Lewis', 'Nusselt', 'Reynolds', 'Sherwood']


def Properties(T, P=101325, fluid='air'):
    r'''Calculates fluid properties of air at atmospheric conditions using CoolProp

    Parameters
    ----------
    T : float
        Temperature [K]
    P : float (optional)
        Pressure [Pa] (Default = 101325 Pa)
    fluid : string
        fluid type (Default = 'air')
    
    Returns
    -------
    rho   : Density [-]
    mu    : Dynamic Viscosity []
    nu    : Kinematic Viscosity []
    c     : Specific Heat []
    K     : Thermal Conductivity []
    alpha : Thermal Diffusivity []

    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    '''      
    rho = cp.CoolProp.PropsSI('D', 'T', T, 'P', P, fluid) # [kg/m##3]
    mu  = cp.CoolProp.PropsSI('V', 'T', T, 'P', P, fluid) #
    nu  = mu /rho
    c_p = cp.CoolProp.PropsSI('C', 'T', T, 'P', P, fluid) #
    k   = cp.CoolProp.PropsSI('L', 'T', T, 'P', P, fluid) #
    alpha = thermal_diffusivity(k, rho, c_p)
    return rho, mu, nu, c_p, k, alpha


def Fourier(alpha_a, t, L):
    r'''Calculates the Fourier number 

    ..math::
        (a + b)^2 = a^2 + 2ab + b^2
        

    Parameters
    ----------
    alpha_a : float
        Thermal Diffusivity [m^2/s]
    t   : float
        Time [s]
    L : float
        plate length [m]
    
    Returns
    -------
    Fo : Fourier number [-]

    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    '''   
    return (alpha_a * t) / (L**2)


def Jakob(cp, i_sv, Tsat_a, T_w, omega_a, omega_sat_w):
    r'''Calculates the Jakob number 

    ..math::
        \lambda = \frac(Cp/isv) * (Tsat_a - T_w)/(omega_a - omega_sat_w)

    Parameters
    ----------
    i_sv : float
        Latent heat of sublimation [J/kg]
    Cp   : float
        Specific heat of dry air [J/kg*K] 
    Tsat_a : float
        Saturation temperature of air [C]
    T_w  : float
        Plate surface temperature [C]
    omega_a  : float
        Humidity Ratio [kg_vapor/kg_total]
    omega_sat_w : float
        Humidity ratio @ Tsat
    
    Returns
    -------
    rho : Density of frost (kg/m^3)

    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    '''        
    return (cp/i_sv) * (Tsat_a - T_w)/(omega_a - omega_sat_w)


def Lewis(D, alpha):
    r'''Calculates the Lewis number
    ..math::
        Le = D / alpha

    Parameters
    ---------   
    D : float
        Diffusion coefficient of water-vapor in the air (m^2/s)
    alpha  : float
        Thermal diffusivity of air (m^2/s)
    
    Returns
    -------
    Ha : Hatta number (-)


    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    '''      
    return D/alpha


def Hatta(x_s, lamb, t, epsilon, D):
    r'''Calculates the Hatta number
    ..math::
        \rho_f = 207*exp(0.266*T_f - 0.0615*T_w)

    Parameters
    ---------   
    x_s     : float
           Frost thickness (m)
    lamb    : float
        Desublimation Coefficient (1/s)
    t       : float
        Time (s)
    epsilon : float
        Porosity (-)
    D       : float
        Diffusivity of water vapor in air (m^2/s)
    
    Returns
    -------
    Ha : Hatta number (-)


    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    '''  
    return x_s* numpy.sqrt((lamb * t) / (epsilon * D))
    

def Nusselt(h, L, k_a):
    r'''Calculates the Nusselt number
    ..math::
        Nu = h * L / k_a

    Parameters
    ---------   
    h   : float
        Heat transfer coefficient [W/m^2*s]
    L   : float
        Plate length [m]
    k_a : float
        Thermal conductivity of Air [W/mK]
    
    Returns
    -------
    Nu : Nusselt number (-)

    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    '''      
    return h*L / k_a
    

def Reynolds(V, L, nu):
    r'''Calculates the Reynolds number
    ..math::
        Re = V*L/nu

    Parameters
    ---------   
    V   : float
        Air Velocity [m/s]
    L   : float
        Plate length [m]
    nu : float
        Dynamic Viscosity [m^2/s]
    
    Returns
    -------
    Re : Reynolds number (-)

    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    ''' 
    return (V*L) / nu
    

def Sherwood(h_m, L, rho_a, D_a):
    r'''Calculates the Sherwood number
    ..math::
        Sh = h_m * L / rho_a * D_a

    Parameters
    ---------   
    h_m  : float
        Mass transfer coefficient [kg/m^2*s]
    L    : float
        Plate length [m]
    rho_a  : float
        Density of Air [kg/m^3]
    D_a : float
        Mass Diffusionn Coefficient [m^2/s]
    
    Returns
    -------
    Sh : Sherwood number (-)


    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    '''  
    return (h_m * L) / (rho_a * D_a)

def dimensionless_time(k, t, rho, Cp, l):
    r'''Calculates the dimensionless time constant
    ..math::
        \tau = (k*t) / (rho*Cp*l**2)

    Parameters
    ---------   
    k  : float
        Thermal conductivity [W/m^2*K]
    t   : float
        Time [s]
    rho : float
        Density [kg/m^3]
    Cp : float
        Specific heat [J/kg*K]
    l  : float
        Plate length [m]
    
    Returns
    -------
    tau : dimensionless time constant (-)


    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    '''      
    return (k*t) / (rho*Cp*l**2)


def dimensionless_temperature(T_a, T_w):
    r'''Calculates the dimensionless temperature
    ..math::
        

    Parameters
    ---------   
    T_a  : float
        Air Temperature [K]
    T_w  : float
        Wall Temperature [K]

    
    Returns
    -------
    T : dimensionless temperature (-)


    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    ''' 
    
    T_tp = 273.16 # triple point of water [K]
    return (T_a - T_tp) / (T_a - T_w)

# Dimensional
def thermal_diffusivity(k, rho, Cp):
    r'''Calculates thermal diffusivity or `alpha` for a fluid with the given
    parameters.

    .. math::
        \alpha = \frac{k}{\rho Cp}

    Parameters
    ----------
    k : float
        Thermal conductivity, [W/m/K]
    rho : float
        Density, [kg/m^3]
    Cp : float
        Heat capacity, [J/kg/K]

    Returns
    -------
    alpha : float
        Thermal diffusivity, [m^2/s]

    Notes
    -----

    Examples
    --------
    >>> thermal_diffusivity(k=0.02, rho=1., Cp=1000.)
    2e-05

    References
    ----------
    .. [1] Blevins, Robert D. Applied Fluid Dynamics Handbook. New York, N.Y.:
       Van Nostrand Reinhold Co., 1984.
    '''
    return k/(rho*Cp)


def saturation_pressure(T, fluid = 'air'):
    p_sat = cp.CoolProp.PropsSI('P', 'Q', 0, 'T', T, fluid)
    return p_sat


def partial_pressure(RH, p_sat):
    return (RH/100)*p_sat


def humidity_ratio(p_va, p_atm = 101325):
    return (0.62198*p_va)/(p_atm - p_va)


def validity_range_check(t_w = 0, t_w_low = 0, t_w_upp = 0,
                         t_a = 0, t_a_low = 0, t_a_upp = 0,
                         w_a = 0, w_a_low = 0, w_a_upp = 0,
                         v = 0, v_low = 0, v_upp = 0,
                         rho_f = 0, rho_f_low = 0, rho_f_upp = 0,
                         rho_i = 0, rho_i_low = 0, rho_i_upp = 0,
                         rho_a = 0, rho_a_low = 0, rho_a_upp = 0):

    '''
    Checks the validity range of parameters according to inputs
    '''
    
    if(t_w != 0 and t_w < t_w_low or t_w > t_w_upp):
        warnings.warn('t_w is extrapoled')
    elif(t_a != 0 and t_a < t_a_low or t_a > t_a_upp):
        warnings.warn('t_a is extrapoled')
    elif(w_a != 0 and w_a < w_a_low or w_a > w_a_upp):
        warnings.warn('w_a is extrapoled')
    elif(v != 0 and v < v_low or v > v_upp):
        warnings.warn('v is extrapoled')
    elif(rho_f != 0 and rho_f < rho_f_low or rho_f > rho_f_upp):
        warnings.warn('rho_f is outside range')
    elif(rho_i != 0 and rho_i < rho_i_low or rho_i > rho_i_upp):
        warnings.warn('rho_i is outside range')
    elif(rho_a != 0 and rho_a < rho_a_low or rho_a > rho_a_upp):
        warnings.warn('rho_a is outside range')