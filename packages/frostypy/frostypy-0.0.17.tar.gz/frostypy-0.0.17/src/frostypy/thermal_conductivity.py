# -*- coding: utf-8 -*-
"""
.. contents:: :local:

Thermal Conductivity
--------------------
.. autofunction:: Lee
.. autofunction:: Ostin
.. autofunction:: Yonko
"""

__all__ = ['Lee', 'Ostin', 'Yonko']

def Lee(rho_f):
    r'''Calculates the frost thermal conductivity, k_f, according to the Lee et. al
    correlation () for a flat plate, which is valid for: ???
               Ta = 21  [C],
        1.3 <= V  < 5.3 [m/s],
        7.5 <= w  < 15  [g/kg_a],
        -30 <= Tp < -5  [C],
        0   <= t  < 200 [min]

    ..math::
        k_f = 0.132 + 3.13*10^-4*rho_f + 1.6*10**-7 * rho_f**2

    Parameters
    ----------
    rho_f : float 
        Frost density [kg/m^3]
    
    Returns
    -------
    k_f : Frost Thermal Conductivity [J/kg*K]
    
    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] K.S. Lee, T.H. Lee, W.S. Kim, Heat and Mass Transfer of parallel plate
    heat exchanger under frosting condition, Kor. J. Air-Cond. Refrig. Eng. 6(2)
    (1994) 155-165
    '''         
    return 0.132 + 3.13*10^-4*rho_f + 1.6*10**-7 * rho_f**2


def Ostin(rho_f):
    r'''Calculates the frost thermal conductivity, k_f, according to the Ostin
    & Andersson correlation for parallel plates, which is valid for: 
        20  <= Ta <= 21    [C],
                V  = 3     [m/s],
        4.6 <= w  <= 10.50 [g/kg_a],
        -20 <= Tp <= -7    [C],
        0   <= t  <= 300   [min]

    ..math::
        k_f = -8.71*10**-3 +4.39*10**-4 * rho_f + 1.05*10**-6*rho_f**2

    Parameters
    ----------
    rho_f : float 
        Frost density [kg/m^3]
    
    Returns
    -------
    k_f : Frost Thermal Conductivity [J/kg*K]
    
    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] Ostin R, Anderson S. Frost growth parameters in a forced air stream.
    Int J Heat Mass Transfer 1991;14(4/5):1009-17
    '''
    return -8.71*10**-3 +4.39*10**-4 * rho_f + 1.05*10**-6*rho_f**2


def Yonko(rho_f):
    r'''Calculates the frost thermal conductivity, k_f, according to the Yonko
    & Sepsy correlation (1967) for a flat plate, which is valid for: 
               Ta = 21  [C],
        1.3 <= V  < 5.3 [m/s],
        7.5 <= w  < 15  [g/kg_a],
        -30 <= Tp < -5  [C],
        0   <= t  < 200 [min]

    ..math::
        k_f = 0.014 + 0.00668*rho_f + 0.0001759*rho_f**2

    Parameters
    ----------
    rho_f : float 
        Frost density [kg/m^3]
    
    Returns
    -------
    k_f : Frost Thermal Conductivity [J/kg*K]
    
    Examples
    --------
    >>>
    
    References
    ----------
    ..[1] Yonko JD, Sepsy CF. An investigation of the thermal conductivity of 
    frost while forming on a flat horizontal plate. ASHRAE Transactions 1967;73(2):1.1-1.11
    '''
    return 0.014 + 0.00668*rho_f + 0.0001759*rho_f**2