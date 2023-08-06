import numpy as np


def t1(t, T1, M_0, M_inf):
    """Exponential recovery for inversion recovery and saturation recovery T1 Measurements

    .. math::
        f(t) = M_{\infty} - (M_{\infty} - M_0) e^{-t/T_1}

    Args:
        t (array_like): time series
        T_1 (float): T1 value
        M_0 (float): see equation
        M_inf (float): see equation

    Returns:
        ndarray: T1 curve
    """

    return M_inf - (M_inf - M_0) * np.exp(-1.0 * t / T1)


def t2(t, M_0, T2, p=1.0):
    """Calculate stretched or un-stretched (p=1) exponential T2 curve

    .. math::
        f(t) = M_{0} e^{(-(t/T_{2})^{p}}

    Args:
        t (array_like): time series
        M_0 (float): see equation
        T_2 (float): T2 value
        p (float): see equation

    Returns:
        ndarray: T2 curve
    """

    return M_0 * np.exp(-1.0 * (t / T2) ** p)


def general_exp(t, C1, C2, tau):
    """Calculate mono-exponential curve

    .. math::
        f(t) = C1 + C2 e^{-t/tau}

    Args:
        t (array_like): time series
        C1 (float): see equation
        C2 (float): see equation
        tau (float): see equation

    Returns:
        ndarray: mono-exponential curve
    """

    return C1 + C2 * np.exp(-1.0 * t / tau)


def general_biexp(t, C1, C2, tau1, C3, tau2):
    """Calculate bi-exponential curve

    .. math::
        f(t) = C1 + C2 e^{-t/tau1} + C3 e^{-t/tau2}

    Args:
        t (array_like): time series
        C1 (float): see equation
        C2 (float): see equation
        C3 (float): see equation
        tau1 (float): see equation
        tau2 (float): see equation

    Returns:
        ndarray: bi-exponential curve
    """

    return C1 + C2 * np.exp(-1.0 * t / tau1) + C3 * np.exp(-1.0 * t / tau2)


def buildup_function(p, E_max, p_half):
    """Calculate asymptotic buildup curve

    .. math::
        f(p) = 1 + E_{max} * p / (p_{1/2} + p)

    Args:
        p (array): power series
        E_max (float): maximum enhancement
        p_half (float): power at half saturation

    Returns:
        ndarray: buildup curve
    """

    return 1 + E_max * p / (p_half + p)


def ksigma_smax(p, E_max, p_half):
    """Calculate asymptotic buildup curve

    .. math::
        f(p) = E_{max} * p / (p_{1/2} + p)

    Args:
        p (array): power series
        E_max (float): maximum enhancement
        p_half (float): power at half saturation

    Returns:
        ndarray: buildup curve
    """

    return E_max * p / (p_half + p)


def logistic(x, c, x0, L, k):
    """Calculate asymptotic buildup curve

    .. math::
        f(p) =

    Args:
        x (array): x values
        c (float): offset
        x0 (float): x-value of sigmoid's midpoint
        L (float): maximum value
        k (float): logistic growth steepness

    Returns:
        ndarray: buildup curve
    """

    return c + L / (1.0 + np.exp(-1.0 * k * (x - x0)))
