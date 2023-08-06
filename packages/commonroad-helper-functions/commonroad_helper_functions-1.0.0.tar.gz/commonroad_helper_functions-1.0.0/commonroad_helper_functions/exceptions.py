"""This module contains exceptions tailored to motion planning."""


class GoalReachedNotification(Exception):
    """Raised when the goal is reached."""


class PlanningError(Exception):
    """General Error during MotionPlanning."""


class ExecutionTimeoutError(PlanningError):
    """Exception for timed out processes."""


class ScenarioCompatibilityError(PlanningError):
    """Raised when a scenario is incompatibel."""


class CollisionDetectedError(PlanningError):
    """Raise this Exception when a collision is detected."""


class EgoVehicleOutsideLaneletError(PlanningError):
    """Raised when no Lanelet is found for the ego vehicle."""


class NoGlobalPathFoundError(PlanningError):
    """Raised when no global path can be found."""


class NoLocalTrajectoryFoundError(PlanningError):
    """Raised when no local trajectory can be found."""
