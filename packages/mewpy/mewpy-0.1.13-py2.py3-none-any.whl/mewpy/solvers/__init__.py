from .ode import (ODEMethod, SolverConfigurations, ODEStatus,
                  KineticConfigurations)
from .solution import Solution, Status

# #################################################
# Linear Programming Solvers
# #################################################

solvers = dict()

try:
    from .gurobi_solver import GurobiSolver
    solvers['gurobi'] = GurobiSolver
except ImportError:
    pass


try:
    from .cplex_solver import CplexSolver
    solvers['cplex'] = CplexSolver
except ImportError:
    pass

try:
    from .optlang_solver import OptLangSolver
    solvers['optlang'] = OptLangSolver
except ImportError:
    pass


default_solver = None


def get_default_solver():

    global default_solver

    if default_solver:
        return default_solver

    solver_order = ['cplex', 'gurobi', 'optlang']

    for solver in solver_order:
        if solver in list(solvers.keys()):
            default_solver = solver
            break

    if not default_solver:
        raise RuntimeError("No solver available.")

    return default_solver


def set_default_solver(solvername):
    """ Sets default solver.

    Arguments:
        solvername : (str) solver name (currently available: 'gurobi', 'cplex')
    """

    global default_solver

    if solvername.lower() in list(solvers.keys()):
        default_solver = solvername.lower()
    else:
        raise RuntimeError(f"Solver {solvername} not available.")


def solver_instance(model=None):
    """ Returns a new instance of the currently selected solver.

    Arguments:
        model : COBRApy/REFRAMED model or a Simulator (optional) -- immediatly instantiate problem with given model

    Returns:
        Solver
    """

    solver = get_default_solver()

    if solver:
        return solvers[solver](model)

# #################################################
# ODE solvers
# #################################################


ode_solvers = dict()


try:
    from .scikits_solver import ScikitsODESolver
    ode_solvers['scikits'] = ScikitsODESolver
except ImportError:
    pass


try:
    from .scipy_solver import ScipySolver
    ode_solvers['scipy'] = ScipySolver
except ImportError:
    pass


try:
    from .odespy_solver import ODESpySolver
    ode_solvers['odespy'] = ODESpySolver
except ImportError:
    pass


default_ode_solver = None


def get_default_ode_solver():
    global default_ode_solver

    if default_ode_solver:
        return default_ode_solver

    ode_solver_order = ['scikits', 'scipy', 'odespy']

    for solver in ode_solver_order:
        if solver in list(ode_solvers.keys()):
            default_ode_solver = solver
            break

    if not default_ode_solver:
        raise RuntimeError("No solver ODE available.")

    return default_ode_solver


def set_default_ode_solver(solvername):
    """ Sets default solver.

    Arguments:
        solvername : (str) solver name (currently available: 'gurobi', 'cplex')
    """

    global default_ode_solver

    if solvername.lower() in list(ode_solvers.keys()):
        default_ode_solver = solvername.lower()
    else:
        raise RuntimeError(f"ODE solver {solvername} not available.")


def ode_solver_instance(func, method: ODEMethod):
    """ Returns a new instance of the currently selected solver.

    Arguments:
        func : a function
        method: a method

    Returns:
        Solver
    """

    solver = get_default_ode_solver()
    if solver:
        return ode_solvers[solver](func, method)
