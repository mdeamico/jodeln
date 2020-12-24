import math

def geh(m, c):
    """Calculates the GEH between two hourly traffic volumes.

    See: https://en.wikipedia.org/wiki/GEH_statistic

    Parameters
    ----------
    m : float
        Modeled traffic volume.
    c : float
        Counted traffic volume.

    Returns
    -------
    float
        GEH statistic.
    """
    denominator = (m + c) / 2.0
    if denominator == 0:
        return 0

    numerator = (m - c) * (m - c)
    quotient = numerator / denominator
    
    if quotient < 0:
        return 0
    
    geh = math.sqrt(quotient)
    
    return geh
