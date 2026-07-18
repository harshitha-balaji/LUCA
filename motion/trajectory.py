"""
Trajectory planning for the robotic arm.

This module generates intermediate joint configurations
between the robot's current pose and the desired target pose.

Responsibilities:
- Plan joint-space trajectories
- Generate intermediate JointAngles
- Provide a smooth interface between inverse kinematics
  and the hardware controller

This module does not perform:
- Inverse kinematics
- Forward kinematics
- Hardware communication
- Servo control

Future versions will support:
- Linear interpolation
- Velocity limiting
- Acceleration profiles
- Smooth trajectory generation
"""

from core.models import JointAngles


class TrajectoryPlanner:
    """
    Plans robot motion in joint space.

    The planner converts a desired target joint configuration
    into a sequence of intermediate JointAngles that can be
    executed by the robot.

    Version 1 returns a direct trajectory consisting of the
    target configuration only.

    Future versions will generate smooth interpolated paths.
    """

    def __init__(self) -> None:
        """Initialize the trajectory planner."""
        pass

    def plan(
        self,
        current: JointAngles,
        target: JointAngles
    ) -> list[JointAngles]:
        """
        Plan a trajectory between two joint configurations.

        Args:
            current:
                Current robot joint configuration.

            target:
                Desired robot joint configuration.

        Returns:
            A list of JointAngles representing the trajectory.

        Raises:
            TypeError:
                If either argument is not a JointAngles instance.
        """

        if not isinstance(current, JointAngles):
            raise TypeError(
                f"Expected JointAngles, got {type(current).__name__}."
            )

        if not isinstance(target, JointAngles):
            raise TypeError(
                f"Expected JointAngles, got {type(target).__name__}."
            )

        return self._generate_path(current, target)

    def _generate_path(
        self,
        current: JointAngles,
        target: JointAngles
    ) -> list[JointAngles]:
        """
        Generate the joint-space trajectory.

        Version 1 returns only the target configuration.

        Future versions will interpolate intermediate
        configurations for smooth robot motion.
        """

        return [target]