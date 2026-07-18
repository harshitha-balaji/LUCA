"""
Inverse Kinematics module for the robotic arm.

This module is responsible for converting a target position in the
robot workspace into the corresponding joint angles required to
reach that position.

Current Version:
    - Input validation
    - Workspace validation
    - Placeholder inverse kinematics implementation
    - Joint angle validation

Future Versions:
    - Analytical inverse kinematics
    - Joint limit enforcement
    - Multiple IK solutions
    - Singularity detection
"""
import math

from core.models import Position, JointAngles

from config import (
    BASE_HEIGHT,
    UPPER_ARM_LENGTH,
    FOREARM_LENGTH,
    WRIST_LENGTH,

    BASE_MIN,
    BASE_MAX,

    SHOULDER_MIN,
    SHOULDER_MAX,

    ELBOW_MIN,
    ELBOW_MAX,

    WRIST_PITCH_MIN,
    WRIST_PITCH_MAX,

    WRIST_ROLL_MIN,
    WRIST_ROLL_MAX,

    GRIPPER_MIN,
    GRIPPER_MAX,
)


class InverseKinematics:
    """
    Computes the joint angles required to reach a target position.

    This class performs the mathematical conversion from a Cartesian
    position to a robot joint configuration. It is completely
    independent of hardware communication and robot control logic.

    """
    # ==========================================================
    # Initialization
    # ==========================================================

    def __init__(self):
        """
        Initialize the inverse kinematics solver.

        Robot geometry and joint limits are loaded from the
        central configuration so that the solver remains
        independent of the physical robot dimensions.
        """

        # Robot geometry
        self.base_height = BASE_HEIGHT
        self.upper_arm = UPPER_ARM_LENGTH
        self.forearm = FOREARM_LENGTH
        self.wrist = WRIST_LENGTH

        # Joint limits
        self.base_limits = (
            BASE_MIN,
            BASE_MAX
        )

        self.shoulder_limits = (
            SHOULDER_MIN,
            SHOULDER_MAX
        )

        self.elbow_limits = (
            ELBOW_MIN,
            ELBOW_MAX
        )

        self.wrist_pitch_limits = (
            WRIST_PITCH_MIN,
            WRIST_PITCH_MAX
        )

        self.wrist_roll_limits = (
            WRIST_ROLL_MIN,
            WRIST_ROLL_MAX
        )

        self.gripper_limits = (
            GRIPPER_MIN,
            GRIPPER_MAX
        )
    
    # ==========================================================
    # Public API
    # ==========================================================


    def solve(self, target: Position) -> JointAngles:
        """
        Compute the joint angles required to reach the specified
        target position.

        Args:
            target (Position):
                Desired end-effector position.

        Returns:
            JointAngles:
                Joint configuration corresponding to the target.

        Raises:
            TypeError:
                If the target is not a Position object.

            ValueError:
                If the target position is invalid.
        """

        if not isinstance(target, Position):
            raise TypeError(
                f"Expected Position, got {type(target).__name__}."
            )

        self._check_workspace(target)

        angles = self._compute_angles(target)

        self._validate_angles(angles)

        return angles
    
    # ==========================================================
    # Workspace Validation
    # ==========================================================

    def _check_workspace(self, target: Position):
        """
        Validate that the target lies within the reachable
        workspace of the robot.
        """

        if target.z < 0:
            raise ValueError(
                f"Target z-coordinate ({target.z}) cannot be negative."
            )

        r = self._horizontal_distance(target)
        dz = self._vertical_distance(target)

        distance = math.hypot(r, dz)

        maximum_reach = (
            self.upper_arm +
            self.forearm +
            self.wrist
        )

        if distance > maximum_reach:
            raise ValueError(
                "Target lies outside the robot workspace."
            )
    
    # ==========================================================
    # Inverse Kinematics
    # ==========================================================

    def _compute_angles(self, target: Position) -> JointAngles:
        """
        Compute the robot joint angles required to reach
        the requested target position.
        """

        base = self._compute_base(target)

        shoulder, elbow = self._compute_planar(target)

        wrist_pitch = self._compute_wrist_pitch(
            shoulder,
            elbow
        )

        wrist_roll = 0.0

        return JointAngles(
            base=base,
            shoulder=shoulder,
            elbow=elbow,
            wrist_pitch=wrist_pitch,
            wrist_roll=wrist_roll,
            gripper=0.0,
        )
    
    def _compute_base(self, target: Position) -> float:
        """
        Compute the base rotation angle.

        The base rotates about the vertical axis so that the
        arm faces the target position.
        """

        return math.degrees(
            math.atan2(
                target.y,
                target.x
            )
        )
    
    def _compute_planar(
        self,
        target: Position
    ) -> tuple[float, float]:
        """
        Compute the shoulder and elbow joint angles required
        to reach the specified target position.

        The inverse kinematics problem is reduced to a planar
        two-link manipulator after the base rotation has been
        computed.

        Args:
            target (Position):
                Desired target position.

        Returns:
            tuple[float, float]:
                (shoulder_angle, elbow_angle) in degrees.

        Raises:
            ValueError:
                If the target produces an invalid planar
                configuration.
        """

        r = self._horizontal_distance(target)
        dz = target.z - self.base_height

        distance = math.hypot(r, dz)

        if distance == 0:
            raise ValueError(
                "Target coincides with the shoulder joint."
            )

        # Law of Cosines for the elbow angle.
        cos_elbow = (
            self.upper_arm ** 2
            + self.forearm ** 2
            - distance ** 2
        ) / (
            2
            * self.upper_arm
            * self.forearm
        )

        # Clamp to protect against floating-point error.
        cos_elbow = max(
            -1.0,
            min(1.0, cos_elbow)
        )

        elbow = math.degrees(
            math.acos(cos_elbow)
        )

        # Angle from the shoulder to the target.
        phi = math.atan2(
            dz,
            r
        )

        # Internal shoulder triangle angle.
        cos_alpha = (
            self.upper_arm ** 2
            + distance ** 2
            - self.forearm ** 2
        ) / (
            2
            * self.upper_arm
            * distance
        )

        cos_alpha = max(
            -1.0,
            min(1.0, cos_alpha)
        )

        alpha = math.acos(cos_alpha)

        shoulder = math.degrees(
            phi + alpha
        )

        return shoulder, elbow
    
    def _compute_wrist_pitch(
        self,
        shoulder: float,
        elbow: float
    ) -> float:
        """
        Compute the wrist pitch angle required to maintain
        the desired end-effector orientation.

        Args:
            shoulder (float):
                Shoulder joint angle in degrees.

            elbow (float):
                Elbow joint angle in degrees.

        Returns:
            float:
                Wrist pitch angle in degrees.
        """

        desired_tool_angle = 0.0

        wrist_pitch = (
            desired_tool_angle
            - shoulder
            - elbow
        )

        return wrist_pitch
    
    # ==========================================================
    # Joint Validation
    # ==========================================================

    def _validate_angles(self, angles: JointAngles):
        """
        Validate the generated joint configuration.

        Ensures that every computed joint angle lies
        within its configured mechanical limits.
        """

        if not isinstance(angles, JointAngles):
            raise TypeError(
                "Expected JointAngles from inverse kinematics."
            )

        self._check_joint_limit(
            "Base",
            angles.base,
            self.base_limits
        )

        self._check_joint_limit(
            "Shoulder",
            angles.shoulder,
            self.shoulder_limits
        )

        self._check_joint_limit(
            "Elbow",
            angles.elbow,
            self.elbow_limits
        )

        self._check_joint_limit(
            "Wrist Pitch",
            angles.wrist_pitch,
            self.wrist_pitch_limits
        )

        self._check_joint_limit(
            "Wrist Roll",
            angles.wrist_roll,
            self.wrist_roll_limits
        )

        self._check_joint_limit(
            "Gripper",
            angles.gripper,
            self.gripper_limits
        )

    def _check_joint_limit(
        self,
        joint_name: str,
        angle: float,
        limits: tuple[float, float]
    ):
        """
        Validate that a joint angle lies within its
        configured mechanical limits.

        Args:
            joint_name (str):
                Name of the joint.

            angle (float):
                Computed joint angle.

            limits (tuple):
                (minimum, maximum) allowable angles.

        Raises:
            ValueError:
                If the angle exceeds its limits.
        """

        minimum, maximum = limits

        if not minimum <= angle <= maximum:
            raise ValueError(
                f"{joint_name} angle "
                f"({angle:.2f}°) "
                f"is outside "
                f"[{minimum:.2f}°, {maximum:.2f}°]."
            )
    
    # ==========================================================
    # Utility Functions
    # ==========================================================
        
    def _horizontal_distance(self, target: Position) -> float:
        """
        Compute the horizontal distance from the robot base
        to the target position.
        """

        return math.hypot(
            target.x,
            target.y
        )
    
    def _vertical_distance(self, target: Position) -> float:
        """
        Compute the vertical distance between the shoulder
        joint and the target.
        """

        return target.z - self.base_height
    
