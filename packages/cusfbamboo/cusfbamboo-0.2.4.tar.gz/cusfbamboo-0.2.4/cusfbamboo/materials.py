"""
Classes for representing solid materials, fluids and transport properties. Also contains some useful pre-defined materials.

References *need to get solid materials references
- [1] - CoolProp, http://coolprop.org/
"""

# Classes
class Material:
    """Class used to specify a material and its properties. For calculating temperatures, only 'k' must be defined. For stresses, you also need E, alpha, and poisson.

    Args:
        k (float): Thermal conductivity (W/m/K)
        
    Keyword Args:
        E (float): Young's modulus (Pa)
        alpha (float): Thermal expansion coefficient (strain/K)
        poisson (float): Poisson's ratio
    """
    def __init__(self, k, **kwargs):
        self.k = k                  

        if "E" in kwargs:
            self.E = kwargs["E"]
        else:
            self.E = float("NaN")

        if "alpha" in kwargs:
            self.alpha = kwargs["alpha"]
        else:
            self.alpha = float("NaN")

        if "poisson" in kwargs:
            self.poisson = kwargs["poisson"]
        else:
            self.poisson = float("NaN")

class TransportProperties:
    def __init__(self, Pr, mu, k, cp = None, rho = None, gamma_coolant = None):
        """
        Container for specifying your transport properties. Each input can either be a function of temperature (K) and pressure (Pa) in that order, e.g. mu(T, p). Otherwise they can be constant floats.

        Args:
            Pr (float or callable): Prandtl number.
            mu (float or callable): Absolute viscosity (Pa s).
            k (float or callable): Thermal conductivity (W/m/K).
            cp (float or callable, optional): Isobaric specific heat capacity (J/kg/K) - only required for coolants.
            rho (float or callable, optional): Density (kg/m^3) - only required for coolants.
            gamma_coolant (float or callable, optional): Ratio of specific heats (cp/cv) for a compressible coolant. If this is submitted, it is assumed that this object represents a compressible coolant.
        
        Attributes:
            compressible_coolant (bool): Whether or not this TransportProperties object represents a compressible coolant.
        """

        self.type = type
        self._Pr = Pr
        self._mu = mu
        self._k = k
        self._rho = rho
        self._cp = cp
        self._gamma_coolant = gamma_coolant

        if gamma_coolant is None:
            self.compressible_coolant = False
        else:
            self.compressible_coolant = True

    def Pr(self, T, p):
        """Prandtl number.

        Args:
            T (float): Temperature (K)
            p (float): Pressure (Pa)

        Returns:
            float: Prandtl number
        """
        if callable(self._Pr):
            return self._Pr(T, p)
        
        else:
            return self._Pr

    def mu(self, T, p):
        """Absolute viscosity (Pa s)

        Args:
            T (float): Temperature (K)
            p (float): Pressure (Pa)

        Returns:
            float: Absolute viscosity (Pa s)
        """
        if callable(self._mu):
            return self._mu(T, p)
        
        else:
            return self._mu

    def k(self, T, p):
        """Thermal conductivity (W/m/K)

        Args:
            T (float): Temperature (K)
            p (float): Pressure (Pa)

        Returns:
            float: Thermal conductivity (W/m/K)
        """
        if callable(self._k):
            return self._k(T, p)
        
        else:
            return self._k

    def rho(self, T, p):
        """Density (kg/m^3)
        Args:
            T (float): Temperature (K)
            p (float): Pressure (Pa)
        Returns:
            float: Density (kg/m^3)
        """
        if self._rho is None:
            raise ValueError("TransportProperties object does not have its density 'rho' defined. If you tried to use this TransportProperties object for a coolant, you need to specify the 'rho' input.")

        if callable(self._rho):
            return self._rho(T, p)
        
        else:
            return self._rho

    def cp(self, T, p):
        """Isobaric specific heat capacity (J/kg/K)

        Args:
            T (float): Temperature (K)
            p (float): Pressure (Pa)

        Returns:
            float: Isobaric specific heat capacity (J/kg/K)
        """

        if self._cp is None:
            raise ValueError("TransportProperties object does not have its isobaric specific heat capacity 'cp' defined. If you tried to use this TransportProperties object for a coolant, you need to specify the 'cp' input.")

        if callable(self._cp):
            return self._cp(T, p)
        
        else:
            return self._cp

    def gamma_coolant(self, T, p):
        """Ratio of specific heat capacities for a compressible coolant.

        Args:
            T (float): Temperature (K)
            p (float): Pressure (Pa)

        Returns:
            float: Ratio of specific heat capacities (cp/cv).
        """

        if self._gamma_coolant is None:
            raise ValueError("TransportProperties object does not have its compressibgle coolant gamma 'gamma_coolant' defined.")

        if callable(self._gamma_coolant):
            return self._gamma_coolant(T, p)
        
        else:
            return self._gamma_coolant

class NucleateBoiling:
    def __init__(self, vapour_transport, liquid_transport, sigma, h_fg, C_sf):
        """Class for representing the information needed to model nucleate boiling. Not currently used.

        Args:
            vapour_transport (TransportProperties): The transport properties of the vapour phase.
            liquid_transport (TransportProperties): The transport properties of the liquid phase.
            sigma (callable): Surface tension of the liquid-vapour interface (N/m), as a function of temperature (K) and pressure (Pa) in the form sigma(T,p).
            h_fg (callable): Enthalpy between vapour and liquid phases, as a function of pressure (Pa). h_fg = h_g - h_f. (J/kg/K)
            C_sf (float): Surface-fluid coefficient. Will be different for different material + fluid combinations. Some examples are available in References [4] and [6] given in bamboo.circuit.py.
        """

        raise ValueError("NucleateBoiling class is not yet implemented")
    

# Solids
CopperC106 = Material(E = 117e9, poisson = 0.34, alpha = 16.9e-6, k = 391.2)
StainlessSteel304 = Material(E = 193e9, poisson = 0.29, alpha = 16e-6, k = 14.0)
Graphite = Material(E = float('NaN'), poisson = float('NaN'), alpha = float('NaN'), k = 63.81001)

# Fluids
Water = TransportProperties(Pr = 6.159, mu = 0.89307e-3, k = 0.60627, cp = 4181.38, rho =  997.085)         # Water at 298 K and 1 bar [1]
Ethanol = TransportProperties(Pr = 16.152, mu = 1.0855e-3, k = 0.163526, cp = 2433.31, rho = 785.26)        # Ethanol at 298 K and 1 bar [1]
CO2 = TransportProperties(mu = 3.74e-5, k =  0.0737, Pr = 0.72)                                             # Representative values for CO2 gas


