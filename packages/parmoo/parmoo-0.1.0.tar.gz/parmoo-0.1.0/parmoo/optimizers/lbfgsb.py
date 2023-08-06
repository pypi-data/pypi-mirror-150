
""" Implementations of the SurrogateOptimizer class.

This module contains implementations of the SurrogateOptimizer ABC, which
are based on the L-BFGS-B quasi-Newton algorithm.

Note that all of these methods are gradient based, and therefore require
objective, constraint, and surrogate gradient methods to be defined.

The classes include:
 * ``LBFGSB`` -- Limited-memory bound-constrained BFGS (L-BFGS-B) method
 * ``TR_LBFGSB`` -- L-BFGS-B is applied within a trust region

"""

import numpy as np
import inspect
from parmoo.structs import SurrogateOptimizer, AcquisitionFunction


class LBFGSB(SurrogateOptimizer):
    """ Use L-BFGS-B and gradients to identify local solutions.

    Applies L-BFGS-B to the surrogate problem, in order to identify design
    points that are locally Pareto optimal with respect to the surrogate
    problem.

    """

    # Slots for the LBFGSB class
    __slots__ = ['n', 'bounds', 'acquisitions', 'budget', 'constraints',
                 'objectives', 'gradients', 'lagrangian']

    def __init__(self, o, lb, ub, hyperparams):
        """ Constructor for the LocalGPS class.

        Args:
            o (int): The number of objectives.

            lb (numpy.ndarray): A 1d array of lower bounds for the design
                region. The number of design variables is inferred from the
                dimension of lb.

            ub (numpy.ndarray): A 1d array of upper bounds for the design
                region. The dimension must match ub.

            hyperparams (dict): A dictionary of hyperparameters for the
                optimization procedure. It may contain the following:
                 * opt_budget (int): The evaluation budget (default: 10,000).

        Returns:
            SurrogateOptimizer: A new SurrogateOptimizer object.

        """

        from parmoo.util import xerror

        # Check inputs
        xerror(o, lb, ub, hyperparams)
        self.n = lb.size
        self.bounds = np.zeros((self.n, 2))
        self.bounds[:, 0] = lb
        self.bounds[:, 1] = ub
        # Check that the contents of hyperparams is legal
        if 'opt_budget' in hyperparams:
            if isinstance(hyperparams['opt_budget'], int):
                if hyperparams['opt_budget'] < 1:
                    raise ValueError("hyperparams['opt_budget'] "
                                     "must be positive")
                else:
                    self.budget = hyperparams['opt_budget']
            else:
                raise ValueError("hyperparams['opt_budget'] "
                                 "must be an integer")
        else:
            self.budget = 10000
        self.acquisitions = []
        return

    def setObjective(self, obj_func):
        """ Add a vector-valued objective function that will be solved.

        Args:
            obj_func (function): A vector-valued function that can be evaluated
                to solve the surrogate optimization problem.

        """

        # Check whether obj_func() has an appropriate signature
        if callable(obj_func):
            if len(inspect.signature(obj_func).parameters) != 1:
                raise ValueError("obj_func() must accept exactly one input")
            else:
                # Add obj_func to the problem
                self.objectives = obj_func
        else:
            raise ValueError("obj_func() must be callable")
        return

    def setReset(self, reset):
        """ Add a reset function for resetting surrogate updates.

        This method is not used by this class.

        """

        return

    def setLagrangian(self, lagrangian, grad_func):
        """ Add a matrix-valued gradient function for obj_func.

        Args:
            lagrangian (function): A vector-valued augmented Lagrangian
                that incorporates a penalty for violating constraints.

            grad_func (function): A matrix-valued function that can be
                evaluated to obtain the Jacobian matrix for the Lagrangian.

        """

        # Check whether grad_func() has an appropriate signature
        if callable(grad_func):
            if len(inspect.signature(grad_func).parameters) != 1:
                raise ValueError("grad_func() must accept exactly one input")
            else:
                # Add grad_func to the problem
                self.gradients = grad_func
        else:
            raise ValueError("grad_func() must be callable")
        # Check whether lagrangian() has an appropriate signature
        if callable(lagrangian):
            if len(inspect.signature(lagrangian).parameters) != 1:
                raise ValueError("lagrangian() must accept exactly one input")
            else:
                # Add Lagrangian to the problem
                self.lagrangian = lagrangian
        else:
            raise ValueError("lagrangian() must be callable")
        return

    def setConstraints(self, constraint_func):
        """ Add a constraint function that will be satisfied.

        Args:
            constraint_func (function): A vector-valued function from the
                design space whose components correspond to constraint
                violations. If the problem is unconstrained, a function
                that returns zeros could be provided.

        """

        # Check whether constraint_func() has an appropriate signature
        if callable(constraint_func):
            if len(inspect.signature(constraint_func).parameters) != 1:
                raise ValueError("constraint_func() must accept exactly one"
                                 + " input")
            else:
                # Add constraint_func to the problem
                self.constraints = constraint_func
        else:
            raise ValueError("constraint_func() must be callable")
        return

    def addAcquisition(self, *args):
        """ Add an acquisition function for the surrogate optimizer.

        Args:
            *args (AcquisitionFunction): Acquisition functions that are used
                to scalarize the list of objectives in order to solve the
                surrogate optimization problem.

        """

        # Check for illegal inputs
        if not all([isinstance(arg, AcquisitionFunction) for arg in args]):
            raise ValueError("Args must be instances of AcquisitionFunction")
        # Append all arguments to the acquisitions list
        for arg in args:
            self.acquisitions.append(arg)
        return

    def solve(self, x):
        """ Solve the surrogate problem using L-BFGS-B.

        Args:
            x (np.ndarray): A 2d array containing a list of feasible
                design points used to warm start the search.

        Returns:
            np.ndarray: A 2d numpy.ndarray of potentially efficient design
            points that were found by L-BFGS-B.

        """

        from scipy import optimize

        # Check that x is legal
        if isinstance(x, np.ndarray):
            if self.n != x.shape[1]:
                raise ValueError("The columns of x must match n")
            elif len(self.acquisitions) != x.shape[0]:
                raise ValueError("The rows of x must match the number " +
                                 "of acquisition functions")
        else:
            raise ValueError("x must be a numpy array")
        # Check that x is feasible.
        for xj in x:
            if np.any(xj[:] < self.bounds[:, 0]) or \
               np.any(xj[:] > self.bounds[:, 1]):
                raise ValueError("some of starting points (x) are infeasible")
        # Initialize an empty list of results
        result = []
        # Calculate budget per call
        budget_per_call = self.budget / len(self.acquisitions)
        # For each acqusisition function
        for j, acquisition in enumerate(self.acquisitions):

            # Define the scalarized wrapper functions
            def scalar_f(x, *args):
                return acquisition.scalarize(self.lagrangian(x))

            def scalar_g(x, *args):
                return acquisition.scalarizeGrad(self.lagrangian(x),
                                                 self.gradients(x))

            # Get the solution
            res = optimize.minimize(scalar_f, x[j, :], method='L-BFGS-B',
                                    jac=scalar_g, bounds=self.bounds,
                                    options={'maxiter': budget_per_call})
            # Append the found minima to the results list
            result.append(res['x'])
        return np.asarray(result)


class TR_LBFGSB(SurrogateOptimizer):
    """ Use L-BFGS-B and gradients to identify solutions within a trust region.

    Applies L-BFGS-B to the surrogate problem, in order to identify design
    points that are locally Pareto optimal with respect to the surrogate
    problem.

    """

    # Slots for the LBFGSB class
    __slots__ = ['n', 'bounds', 'acquisitions', 'budget', 'constraints',
                 'objectives', 'gradients', 'lagrangian', 'resetObjectives']

    def __init__(self, o, lb, ub, hyperparams):
        """ Constructor for the LocalGPS class.

        Args:
            o (int): The number of objectives.

            lb (numpy.ndarray): A 1d array of lower bounds for the design
                region. The number of design variables is inferred from the
                dimension of lb.

            ub (numpy.ndarray): A 1d array of upper bounds for the design
                region. The dimension must match ub.

            hyperparams (dict): A dictionary of hyperparameters for the
                optimization procedure. It may contain the following:
                 * opt_budget (int): The evaluation budget (default: 10,000).

        Returns:
            SurrogateOptimizer: A new SurrogateOptimizer object.

        """

        from parmoo.util import xerror

        # Check inputs
        xerror(o, lb, ub, hyperparams)
        self.n = lb.size
        self.bounds = np.zeros((self.n, 2))
        self.bounds[:, 0] = lb
        self.bounds[:, 1] = ub
        # Check that the contents of hyperparams is legal
        if 'opt_budget' in hyperparams:
            if isinstance(hyperparams['opt_budget'], int):
                if hyperparams['opt_budget'] < 1:
                    raise ValueError("hyperparams['opt_budget'] "
                                     "must be positive")
                else:
                    self.budget = hyperparams['opt_budget']
            else:
                raise ValueError("hyperparams['opt_budget'] "
                                 "must be an integer")
        else:
            self.budget = 10000
        self.acquisitions = []
        return

    def setObjective(self, obj_func):
        """ Add a vector-valued objective function that will be solved.

        Args:
            obj_func (function): A vector-valued function that can be evaluated
                to solve the surrogate optimization problem.

        """

        # Check whether obj_func() has an appropriate signature
        if callable(obj_func):
            if len(inspect.signature(obj_func).parameters) != 1:
                raise ValueError("obj_func() must accept exactly one input")
            else:
                # Add obj_func to the problem
                self.objectives = obj_func
        else:
            raise ValueError("obj_func() must be callable")
        return

    def setReset(self, reset):
        """ Add a reset function for resetting surrogate updates.

        Args:
            reset (function): A function with one input, which will be
                called prior to solving the surrogate optimization
                problem with each acquisition function.

        """

        # Check whether reset() has an appropriate signature
        if callable(reset):
            if len(inspect.signature(reset).parameters) != 1:
                raise ValueError("reset() must accept exactly one input")
            else:
                # Add obj_func to the problem
                self.resetObjectives = reset
        else:
            raise ValueError("reset() must be callable")
        return

    def setLagrangian(self, lagrangian, grad_func):
        """ Add a matrix-valued gradient function for obj_func.

        Args:
            lagrangian (function): A vector-valued augmented Lagrangian
                that incorporates a penalty for violating constraints.

            grad_func (function): A matrix-valued function that can be
                evaluated to obtain the Jacobian matrix for the Lagrangian.

        """

        # Check whether grad_func() has an appropriate signature
        if callable(grad_func):
            if len(inspect.signature(grad_func).parameters) != 1:
                raise ValueError("grad_func() must accept exactly one input")
            else:
                # Add grad_func to the problem
                self.gradients = grad_func
        else:
            raise ValueError("grad_func() must be callable")
        # Check whether lagrangian() has an appropriate signature
        if callable(lagrangian):
            if len(inspect.signature(lagrangian).parameters) != 1:
                raise ValueError("lagrangian() must accept exactly one input")
            else:
                # Add Lagrangian to the problem
                self.lagrangian = lagrangian
        else:
            raise ValueError("lagrangian() must be callable")
        return

    def setConstraints(self, constraint_func):
        """ Add a constraint function that will be satisfied.

        Args:
            constraint_func (function): A vector-valued function from the
                design space whose components correspond to constraint
                violations. If the problem is unconstrained, a function
                that returns zeros could be provided.

        """

        # Check whether constraint_func() has an appropriate signature
        if callable(constraint_func):
            if len(inspect.signature(constraint_func).parameters) != 1:
                raise ValueError("constraint_func() must accept exactly one"
                                 + " input")
            else:
                # Add constraint_func to the problem
                self.constraints = constraint_func
        else:
            raise ValueError("constraint_func() must be callable")
        return

    def addAcquisition(self, *args):
        """ Add an acquisition function for the surrogate optimizer.

        Args:
            *args (AcquisitionFunction): Acquisition functions that are used
                to scalarize the list of objectives in order to solve the
                surrogate optimization problem.

        """

        # Check for illegal inputs
        if not all([isinstance(arg, AcquisitionFunction) for arg in args]):
            raise ValueError("Args must be instances of AcquisitionFunction")
        # Append all arguments to the acquisitions list
        for arg in args:
            self.acquisitions.append(arg)
        return

    def solve(self, x):
        """ Solve the surrogate problem using L-BFGS-B.

        Args:
            x (np.ndarray): A 2d array containing a list of feasible
                design points used to warm start the search.

        Returns:
            np.ndarray: A 2d numpy.ndarray of potentially efficient design
            points that were found by L-BFGS-B.

        """

        from scipy import optimize

        # Check that x is legal
        if isinstance(x, np.ndarray):
            if self.n != x.shape[1]:
                raise ValueError("The columns of x must match n")
            elif len(self.acquisitions) != x.shape[0]:
                raise ValueError("The rows of x must match the number " +
                                 "of acquisition functions")
        else:
            raise ValueError("x must be a numpy array")
        # Check that x is feasible.
        for xj in x:
            if np.any(xj[:] < self.bounds[:, 0]) or \
               np.any(xj[:] > self.bounds[:, 1]):
                raise ValueError("some of starting points (x) are infeasible")
        # Initialize an empty list of results
        result = []
        # Calculate budget per call
        budget_per_call = self.budget / len(self.acquisitions)
        # For each acqusisition function
        for j, acquisition in enumerate(self.acquisitions):

            # Define the scalarized wrapper functions
            def scalar_f(x, *args):
                return acquisition.scalarize(self.lagrangian(x))

            def scalar_g(x, *args):
                return acquisition.scalarizeGrad(self.lagrangian(x),
                                                 self.gradients(x))

            # Create a new trust region
            rad = self.resetObjectives(x[j, :])
            bounds = np.zeros((self.n, 2))
            for i in range(self.n):
                bounds[i, 0] = max(self.bounds[i, 0], x[j, i] - rad)
                bounds[i, 1] = min(self.bounds[i, 1], x[j, i] + rad)
            # Get the solution
            res = optimize.minimize(scalar_f, x[j, :], method='L-BFGS-B',
                                    jac=scalar_g, bounds=bounds,
                                    options={'maxiter': budget_per_call})
            # Append the found minima to the results list
            result.append(res['x'])
        return np.asarray(result)
