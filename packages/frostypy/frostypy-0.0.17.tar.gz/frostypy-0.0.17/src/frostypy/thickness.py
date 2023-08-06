# -*- coding: utf-8 -*-
"""
.. contents:: :local:

Frost Thickness
---------------
.. autofunction:: Cremers_free
.. autofunction:: Cremers
.. autofunction:: Hermes_2012
.. autofunction:: Lee
.. autofunction:: Okoroafor
.. autofunction:: Schneider
.. autofunction:: Sengupta
.. autofunction:: Yang
"""

__all__ = ['Cremers_free', 'Cremers', 'Hermes_2012', 'Lee', 'Okoroafor', 
           'Schneider', 'Sengupta', 'Yang']

def Cremers_free(Tf, Tp, t):
    r'''Calculates the frost thickness, z, according to the Cremers & Mehra correlation
    for a tube, which is valid for: 
        Ta = 24 [C]
        Free convection
        9.2 <= w   <= 15 [g/kg_a],
        45  <= psi <= 90 [%], 

    ..math::
        y_f = 0.20*t*(Tf - Tp)**0.4

    Parameters
    ----------
    Tf : float 
        Frost Temperature [K]
    Tp : float
        Cold Plate Surface [K]
    t : float
        time [s]
    
    Returns
    -------
    y_f : Frost Thickness [m]
    
    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] (insert here)

    '''    
    return 0.20*t*(Tf - Tp)**0.4


def Cremers(Tf, Tp, t):
    r'''Calculates the frost thickness according to the Cremers & Mehra correlation
    for a tube, which is valid for: 
        -90 <= Tp  <= -60 [C],
        0   <= t   <= 600 [min],
        34  <= psi <= 53  [%], 

    ..math::
        y_f = 0.12*t*(Tf - Tp)**0.43

    Parameters
    ----------
    Tf : float 
        Frost Temperature [K]
    Tp : float
        Cold Plate Surface [K]
    t : float
        time [s]
    
    Returns
    -------
    y_f : Frost Thickness [m]
    
    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] Cremers CJ, Mehra VK. Frost formation on vertical cylinders in free
    convection. ASME Journal of Heat Transfer 1908;104(1):3-7

    '''    
    return 0.12*t*(Tf - Tp)**0.43


def Hermes_2012():
    r'''Calculates the frost thickness according to Hermes et. al (2012) correlation
    for a flat plate, which is valid for:
        5.3    <= a1*(Ta-Tw) <= 8.5    [C]
        0.0057 <=   wa-ww    <= 0.0090 [kg_v/kg_a]
                      Re     <= 3*10^7 [-]
        29.3   <=     Nu     <= 40.6   [-]
        82     <=   rho_f    <= 318    [kg/m^3]
        0      <=      t     <= 120    [min]
        
    ..math:

    Parameters
    ----------
    Ta : float
        Air Temperature [C]
    Tw : float
        Plate Temperature [C]
    Tm : float
        Melting-point Temperature of water-ice [C]
    Tf : float
        Frost Temperature [C]
    pv : float
        Partial vapor pressure of the air [-]        
    psat : float
        Vapor pressure of saturated air [%]
    psatf : float
        Vapor pressure of saturated air at the frost surface temperature [-]
    kice : float
        Ice thermal conductivity (kJ/kg*K)
    pice : float
        Ice density (kg/m^3)
    isv : float
        
    t : float
        Time [s]
    
    Returns
    -------
    rho : Frost density [kg/m^3]

    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] Hermes, C.J., 2012. An analytical solution to the problem of frost growth
    and densification on flat surfaces. Int. J. Heat Mass Transf. 55 (23-24), 7346-7351.

    '''
    
    return 


def Lee():
    r'''Calculates the frost thickness, z, according to the Lee (1997) correlation
    for a flat plate, which is valid for:
                Tw     = -15   [C],
                Ta     = 25    [C], 
        50   <= RH    <= 80    [%],
        6000 <= Re    <= 50000 [-],
        50   <= rho_f <= 400   [kg/m^3],
        0    <= t     <= 120   [min]
        
    ..math::
        

    Parameters
    ----------
    Ta : float
        Air Temperature [C]
    Tw : float
        Plate Temperature [C]
    Tm : float
        Melting-point Temperature of water-ice [C]
    Tf : float
        Frost Temperature [C]
    pv : float
        Partial vapor pressure of the air [-]        
    psat : float
        Vapor pressure of saturated air [%]
    psatf : float
        Vapor pressure of saturated air at the frost surface temperature [-]
    kice : float
        Ice thermal conductivity (kJ/kg*K)
    pice : float
        Ice density (kg/m^3)
    isv : float
        
    t : float
        Time [s]
    
    Returns
    -------
    rho : Frost density [kg/m^3]

    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] Lee, K.-S., Kim, W.-S. Lee, T.-H., 1997. A one-dimensional model for 
    frost formation on a cold surface. Int. J. Heat Mass Transf. 40, 4359-4365.

    '''
    return 3


def Okoroafor(b0, b1, t, n):
    return b0 + b1*t**n


def Schneider(Tf, Tm, Tw, k_i, hsub, rho_i, t, p, pfsat, psat):
    r'''Calculates the frost thickness, z, according to Schneider et. al (1978) correlation
    for a flat plate, which is valid for:
        -30  <= Tw <= -5    [C],
        5    <= Ta <= 15    [C], 
        96   <= RH <- 99    [%],
        4000 <= Re <= 32000 [-],
        60   <= t  <= 480   [min]
        
    ..math::
    

    Parameters
    ----------
    Ta : float
        Air Temperature [C]
    Tw : float
        Plate Temperature [C]
    Tm : float
        Melting-point Temperature of water-ice [C]
    Tf : float
        Frost Temperature [C]
    pv : float
        Partial vapor pressure of the air [-]        
    psat : float
        Vapor pressure of saturated air [%]
    psatf : float
        Vapor pressure of saturated air at the frost surface temperature [-]
    kice : float
        Ice thermal conductivity (kJ/kg*K)
    pice : float
        Ice density (kg/m^3)
    isv : float
        
    t : float
        Time [s]
    
    Returns
    -------
    z : Frost thickness [m]

    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] Schneider, H.W., 1978. Equation of the growth rate of frost forming on
    cooled surfaces. Int. J. Heat Mass Trasnfer. 21 (8), 1019-1024.

    '''  
    Ft = 1 + 0.052 * ((Tf - Tm) / (Tm - Tw))
    return (0.465 * ((k_i * (Tf - Tw))/ (hsub * rho_i))**0.5 * (t/3600)**-0.03 
         * (Tf - Tm)**0.01 * ((p-pfsat) / (psat - pfsat))**0.25 * Ft)


def Sengupta(d, Re, Pr, w, Fo):
    r'''Calculates the frost thickness according to the Sengupta et al. correlation
    for a cylinder in cross-flow, which is valid for: 
                Ta = 29   [C]
        1.5  <= V <= 4.4  [m/s]
        10.0 <= w <= 20.0 [g/kg_a]
        
    ..math::
        y_f = 0.84 * d * Re**-0.15 * Pr**0.65 * (1+w)**0.71 * Fo**0.11

    Parameters
    ----------
    d : float 
        cylinder diameter [m]
    Re : float
        Reynolds number [-]
    Pr : float
        Prandtl number [-]
    w : float
        Relative Humidity [%]
    Fo : float
        Fourier number [-]
    
    Returns
    -------
    y_f : Frost Thickness [m]
    
    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] Segupta S, Sherif SA, Wong KV. Empirical heat transfer and frost thickness
    correlations during frost deposition on a cylinder in cross-flow in the 
    transient regime. Int J Energy Research 1998;615-24.
    '''    
    return 0.84 * d * Re**-0.15 * Pr**0.65 * (1+w)**0.71 * Fo**0.11


def Yang(Re, Fo, w, Ta, Ttp, Tp, L):
    r'''Calculates the frost thickness according to the Yang et al. correlation
    for a flat plate, which is valid for: 
               Ta = 21  [C],
        1.3 <= V  < 5.3 [m/s],
        7.5 <= w  < 15  [g/kg_a],
        -30 <= Tp < -5  [C],
        0   <= t  < 200 [min]
        
    ..math::
        y_f = 2.878 * (Re**0.193) * (Fo**0.573) * (w**1.738) * (T**-1.029)

    Parameters
    ----------
    Re : float
        Reynolds number [-]  
    Fo : float
        Fourier number [-]
    w : float
        Absolute humidity [kg_w/kg_air]
    Ta : float
        Air temperature [C]
    Tp : float
        Plate temperature [C]
    Ttp : float
        Triple point of water [C]
    L : float
        plate length [m]
    
    Returns
    -------
    y_f : Frost Thickness [m]
    
    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] Yang, D.-K., Lee, K-S., 2004. Dimensionless correlations of frost
    properties on a cold plate. Int J. Refrigeration 27 (1), 89-96.
    '''  
    Tstar = (Ta - Ttp) / (Ta - Tp)
    y_fstar = 2.878 * (Re**0.193) * (Fo**0.573) * (w**1.738) * (Tstar**-1.029)
    return y_fstar * L 