import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib.pyplot as plt

class IC50Predictor:
    """IC50 predictor class
    
    Attributes:
        concentrations (list or array-like) contains the log-scale concentration values
        responses (list or array-like) contains the responses values between [0, 1]
        method (char) represents the method used for IC50 calculation
        ic50 (float) represents calculated IC50 value
        fitted_params (dict) contains all the parameters besides `ic50`
    """
    
    def __init__(self, 
                 concentrations, 
                 responses, 
                 is_log = False):
        """IC50Predictor initialization
        
        Parameters
        ----------
        concentrations : {list, array-like}, 
            Measured concentrations, if in log scale then set `is_log=True`.
        responses : {list, array-like}, 
            Measured responses, with range in 0-100%. The values below 0 and above 100 will be trimed to 0-100 range. 
            The response values will then be converted in [0,1] range.
        is_log: bool, default=False
            When True, the `concentrations` will be transformed to log scale using 10 as base and multiplied by -1.
        
        Returns
        -------
        self: An IC50Predictor object.
        """
        
        concentrations = np.array(concentrations)
        responses = np.array(responses)
        if len(concentrations) != len(responses):
            raise ValueError(f"The number of concentrations does not match the number of responses.")
        if any(concentrations<0):
            raise ValueError(f"The concentrations cannot be negative.")
        responses[responses < 0] = 0
        responses[responses > 100] = 100
        self.concentrations = np.array(concentrations if is_log else np.log10(concentrations))
        self.responses = np.array(responses)/100   
        self.method = None
        self.ic50 = None
        self.fitted_params = None
        
    @property
    def version(self):
        return "0.0.99"
    
    def __repr__(self):
        return f"IC50 Predictor with {len(self.concentrations)} data points and IC50 of {self.ic50}"

    def _fit_linear_interpolation(self) -> dict:
        """Calculate IC50/pIC50 using linear interpolation.
        
        Returns
        -------
        A dict with `ic50`, `slope` and other values.
        
        Raises
        ------
        ValueError
            if unable to determine IC50 due to insufficient data points.
        """
        
        sorted_data = sorted(zip(self.concentrations, self.responses))
        
        for i in range(len(sorted_data) - 1):
            concentration1, response1 = sorted_data[i]
            concentration2, response2 = sorted_data[i + 1]
            
            if response2 >= 0.5 and response1 <= 0.5:
                slope = (response2 - response1) / (concentration2 - concentration1)
                ic50 = concentration1 + (0.5 - response1) / slope

                return {'ic50':ic50, 'slope':slope, 
                        'concentration1':concentration1, 
                        'concentration2':concentration2, 
                        'response1':response1, 
                        'response2':response2} 

        raise ValueError("Unable to determine IC50. Insufficient data points.")   

        
    def _fit_linear_regression(self) -> dict:
        """Calculate IC50 using linear regression.
        
        Returns
        -------
        A dict with `ic50`, `slope` and `intercept` values.
        """
        
        slope, intercept, _, _, _ = linregress(self.concentrations, self.responses)
        ic50 = (0.5 - intercept) / slope
        
        return {'ic50':ic50, 'slope':slope, 'intercept':intercept}
    
    
    def _fit_polynomial(self, degree = 2, root = 1) -> dict:
        """Calculate IC50 using polynomial regression.
        
        Returns
        -------
        A dict with `ic50`, `degree` and `polyfit` object.
        """

        coefficients = np.polyfit(self.concentrations, self.responses, degree)
        poly = np.poly1d(coefficients)
        ic50 = np.roots(poly - 0.5)[root]

        return {'ic50':ic50, 'degree':degree, 'polyfit':poly}

    def _fit_sigmoid(self, maxfev = 100000, **params) -> dict:
        """Calculate IC50 using sigmoid function.
        
        Parameters
        ----------
        maxfev: int, default=100000
            Maximum number of function evaluations to be used in `scipy.optimize.curve_fit`.       
            
        **params : dict, default=None
            Parameters to be used in `scipy.optimize.curve_fit`.
               
        Returns
        -------
        A dict with `ic50` and `slope` values.       
        """
        
        def sigmoid(x, ic50, slope):
            return 1 / (1 + np.exp((x - ic50) * slope))

        popt, _ = curve_fit(sigmoid, self.concentrations, self.responses, 
                            maxfev = maxfev, 
                            **params)
        ic50, slope = popt
        
        return {'ic50':ic50, 'slope':slope}


    def _fit_hill(self, 
                  hill_params = {'top':1, 
                                 'bottom':0, 
                                 'slope':1}, 
                  maxfev = 100000,
                  **params) -> dict:
        """Calculate IC50 using the Hill equation.
        
        Parameters
        ----------
        hill_params: dict, default={'top':1, 'bottom':0, 'slope':1}
            Parameters for the Hill equation.
        
        maxfev: int, default=100000
            Maximum number of function evaluations to be used in `scipy.optimize.curve_fit`.       
            
        **params : dict, default=None
            Parameters to be used in `scipy.optimize.curve_fit`.
        
        Returns
        -------
        A dict with `ic50`, `slope`, `top` and `bottom` values for the Hill equation.
        
        Raises
        ------
        ValueError
            if unable to determine the Hill equation due to insufficient data points.        
        """
    
        def hill_equation(x, ic50, slope, top, bottom):
            return bottom + (top - bottom) / (1 + 10 ** ((ic50 - x) * slope))
        
        if hill_params is None:
            hill_params = {'ic50':None, 'slope':None, 'top':None, 'bottom':None}
        hill_values = [hill_params.get('ic50'), hill_params.get('slope'), hill_params.get('top'), hill_params.get('bottom')]
        bounds = ([-np.inf if p is None else p-10e-8 for p in hill_values],
                  [np.inf if p is None else p+10e-8 for p in hill_values])
        
        if len(self.concentrations) < 4 - len(hill_params):
            raise ValueError(f"The number of data points (n={len(self.concentrations)}) must exceed " 
                            f"the number of Hill equation parameters (n={4-len(hill_params)}). "
                            f"Please consider using linear, polynomial or sigmoid methods.")
        popt, _ = curve_fit(hill_equation, self.concentrations, self.responses, bounds = bounds, 
                            maxfev = maxfev, **params)
        ic50, slope, top, bottom = popt
        
        return {'ic50':ic50, 'slope':slope, 'top':top, 'bottom':bottom}

        
    def calculate_ic50(self, 
                       method ='hill',
                       degree=2,
                       root=1,
                       hill_params = {'top':1, 
                                 'bottom':0, 
                                 'slope':1},
                       maxfev = 100000,
                       **params):
        """Calculate the IC50 value
                    
        Parameters
        ----------
        method: a selection from {'interpolation','linear','hill','sigmoid','polyfit'}, default is `hill`
            Method used for IC50 calculation
        
        degree: int, default=2
            Degree of the fitting polynomial when `method="Polynomial Fit"`
        
        root: int, default=1
            Which root of the function to be used as IC50 value when `method="Polynomial Fit"`
            
        hill_params: dict, default={'top':1, 'bottom':0, 'slope':1}
            Parameters for the Hill equation when `method="Hill Equation"`
        
        maxfev: int, default=100000
            Maximum number of function evaluations to be used in `scipy.optimize.curve_fit`      
            
        **params : dict, default=None
            Parameters to be used in `scipy.optimize.curve_fit`.
            
        Returns
        -------
        self: A IC50Predictor object
        
        Raises
        ------
        ValueError
            if unable to determine the IC50 value.        
        """
        
        methods = {
            'interpolation': self._fit_linear_interpolation,
            'linear': self._fit_linear_regression,
            'hill': self._fit_hill,
            'sigmoid': self._fit_sigmoid,
            'polyfit': self._fit_polynomial
        }

        if method in methods:
            fitting_function = methods[method]
            if method == 'polyfit':
                params = fitting_function(degree, root)
            elif method == 'sigmoid':
                params = fitting_function(maxfev, **params)
            elif method == 'hill':
                params = fitting_function(hill_params, maxfev, **params)
            else:
                params = fitting_function()
            self.method = method
            self.ic50 = params['ic50']  
            self.fitted_params = params  
        else:
            raise ValueError(f"Invalid method '{method}' specified.")

        return self
    
    def _predict_interpolation(self, concentrations):
        """Predict responses using linear interpolation.

        Parameters
        ----------
        concentrations : {list, array-like}, 
                Measured concentrations in log scale..

        Returns
        -------
        responses: An array with predicted responses.
        """
        
        slope = self.fitted_params['slope']
        concentration1 = self.fitted_params['concentration1']
        concentration2 = self.fitted_params['concentration2']
        response1 = self.fitted_params['response1']
        response2 = self.fitted_params['response2']
        n = len(concentrations)
        responses = np.zeros(n)
        
        for i in range(n):
            if concentrations[i] < concentration1:
                responses[i] = response1
            elif concentrations[i] > concentration2:
                responses[i] = response2
            else:
                 responses[i] = response1 + (concentrations[i] - concentration1) * slope
                    
        return responses

    
    def _predict_linear(self, concentrations):
        """Predict responses using linear regression.

        Parameters
        ----------
        concentrations : {list, array-like}, 
                Measured concentrations in log scale..

        Returns
        -------
        responses: An array with predicted responses.
        """
    
        responses = self.fitted_params['intercept'] + self.fitted_params['slope'] * concentrations

        return responses
    
    
    def _predict_sigmoid(self, concentrations):
        """Predict responses using sigmoid function.

        Parameters
        ----------
        concentrations : {list, array-like}, 
                Measured concentrations in log scale.

        Returns
        -------
        responses: An array with predicted responses.
        """
        
        ic50 = self.fitted_params['ic50']
        slope = self.fitted_params['slope']
        responses = 1 / (1 + np.exp((concentrations - ic50) * slope)) 

        return responses
    
    
    def _predict_polynomial(self, concentrations):
        """Predict responses using polynomial regression.

        Parameters
        ----------
        concentrations : {list, array-like}, 
                Measured concentrations.

        Returns
        -------
        responses: An array with predicted responses.
        """
    
        poly = self.fitted_params['polyfit']
        responses = poly(concentrations)

        return responses
    
    
    def _predict_hill(self, concentrations):
        """Predict responses using the Hill equation.

        Parameters
        ----------
        concentrations : {list, array-like}, 
                Measured concentrations in log scale.

        Returns
        -------
        responses: An array with predicted responses.
        """

        top = self.fitted_params['top']
        bottom = self.fitted_params['bottom']
        slope = self.fitted_params['slope']
        ic50 = self.fitted_params['ic50']        
        responses = bottom + (top - bottom) / (1 + 10 ** ((ic50 - concentrations) * slope))

        return responses
    
    
    def predict_response(self, concentrations):
        """Predict responses based on concentrations.
        Parameters
        ----------
        concentrations : {list, array-like}, 
                Measured concentrations in log scale.
                
        Returns
        -------
        responses: An array with predicted responses.
        
        Raises
        ------
        ValueError
            if no model has been run.    
        """
        
        if self.method is None:
            raise ValueError(f"Fitted method is not detected, please run `calculate_ic50`.")

        concentrations = np.array(concentrations)
        methods = {
            'interpolation': self._predict_interpolation,
            'linear': self._predict_linear,
            'hill': self._predict_hill,
            'sigmoid': self._predict_sigmoid,
            'polyfit': self._predict_polynomial
        }
        fitting_function = methods[self.method]
        response = fitting_function(concentrations)
        
        return response
        
        
    def plot_curve(self, n=100):
        """Plot concentration-response curve and IC50 value.
        Parameters
        ----------
        n : int, default=100, 
             Number of concentrations to plot.
                
        Returns
        -------
        Plot of concentration-response curve IC50.
        """
        
        concentrations = np.linspace(min(self.concentrations), max(self.concentrations), n)
        responses = self.predict_response(concentrations)
    
        plt.figure()
        plt.scatter(self.concentrations, self.responses, color='blue', label='Data')
        plt.plot(concentrations, responses, color='red', label='Fitted Curve')
        plt.axvline(x=self.ic50, color='green', linestyle='--', label='IC50')
        plt.xlabel('Concentration (log)')
        plt.ylabel('Response (x 100%)')
        plt.title('Data and Fitted Curve with IC50')
        plt.legend()
        plt.show()
        
        return None

    
if __name__ == "__main__":
    # Example usage
    concentrations = np.array([0.1, 1, 10, 100, 1000])
    responses = np.array([1, 4, 16, 64, 100])
    ic50 = IC50Predictor(concentrations, responses)
    ic50 = ic50.calculate_ic50()