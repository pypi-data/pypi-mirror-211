# Thermal Model for the motor devleoped by the M-BLUE team
# @U-M Locomotion Lab, directed by Dr. Robert Gregg
# Authors: Jianping Lin and Gray C. Thomas

import numpy as np


class ThermalModel:
    """
    Thermal model of a motor developed by Jianping Lin and Gray C. Thomas 
    @U-M Locomotion Lab, directed by Dr. Robert Gregg

    The model is based on the following assumptions:
    1. The motor is a lumped system with two thermal nodes: the winding and the case.
    2. The winding and the case are assumed to be in thermal equilibrium with the ambient.
    3. The winding and the case are assumed to be in thermal equilibrium with each other.

    The model is based on the following equations:
    1. C_w * dT_w/dt = (I^2)R + (T_c-T_w)/R_WC
    2. C_c * dT_c/dt = (T_w-T_c)/R_WC + (T_w-T_a)/R_CA

    where:
    C_w: Thermal capacitance of the winding
    C_c: Thermal capacitance of the case
    R_WC: Thermal resistance between the winding and the case
    R_CA: Thermal resistance between the case and the ambient
    T_w: Temperature of the winding
    T_c: Temperature of the case
    T_a: Temperature of the ambient
    I: Current
    R: Resistance

    The model is implemented in the following way:
    1. The model is updated at every time step with the current and the ambient temperature.
    2. The model can be used to predict the temperature of the winding and the case at any time step.
    3. The model can also be used to scale the torque based on the temperature of the winding and the case.

    Args:
        ambient (int, optional): Ambient temperature in Celsius. Defaults to 21.
        params (dict, optional): Dictionary of parameters. Defaults to dict().
        temp_limit_windings (int, optional): Maximum temperature of the windings in Celsius. Defaults to 115.
        soft_border_C_windings (int, optional): Soft border of the windings in Celsius. Defaults to 15.
        temp_limit_case (int, optional): Maximum temperature of the case in Celsius. Defaults to 80.
        soft_border_C_case (int, optional): Soft border of the case in Celsius. Defaults to 5.


    """
    def __init__(
        self,
        ambient=21,
        params=dict(),
        temp_limit_windings=115,
        soft_border_C_windings=15,
        temp_limit_case=80,
        soft_border_C_case=5,
    ) -> None:

        # The following parameters result from Jack Schuchmann's test with no fans
        self.C_w: float = 0.20 * 81.46202695970649
        self.R_WC = 1.0702867186480716
        self.C_c = 512.249065845453
        self.R_CA = 1.9406620046327363
        self.α: float = 0.393 * 1 / 100  # Pure copper. Taken from thermalmodel3.py
        self.R_T_0 = 65  # temp at which resistance was measured
        self.R_ϕ_0 = 0.376  # emirical, from the computed resistance (q-axis voltage/ q-axis current). Ohms

        self.__dict__.update(params)
        self.T_w: int = ambient
        self.T_c: int = ambient
        self.T_a: int = ambient
        self.soft_max_temp_windings: int = temp_limit_windings - soft_border_C_windings
        self.abs_max_temp_windings: int = temp_limit_windings
        self.soft_border_windings: int = soft_border_C_windings

        self.soft_max_temp_case: int = temp_limit_case - soft_border_C_case
        self.abs_max_temp_case: int = temp_limit_case
        self.soft_border_case: int = soft_border_C_case

    def update(self, dt, motor_current: float = 0) -> None:
        """
        Updates the temperature of the winding and the case based on the current and the ambient temperature.

        Args:
            dt (float): Time step in seconds.
            motor_current (float, optional): Current in mA. Defaults to 0.

        Dynamics:
            self.C_w * d self.T_w /dt = (I^2)R + (self.T_c-self.T_w)/self.R_WC
            self.C_c * d self.T_c /dt = (self.T_w-self.T_c)/self.R_WC + (self.T_w-self.T_a)/self.R_CA
        """

        I_q_des: float = motor_current * 1e-3

        I2R = (
            I_q_des**2 * self.R_ϕ_0 * (1 + self.α * (self.T_w - self.R_T_0))
        )  # accounts for resistance change due to temp.

        dTw_dt = (I2R + (self.T_c - self.T_w) / self.R_WC) / self.C_w
        dTc_dt: float = (
            (self.T_w - self.T_c) / self.R_WC + (self.T_a - self.T_c) / self.R_CA
        ) / self.C_c
        self.T_w += dt * dTw_dt
        self.T_c += dt * dTc_dt

    def update_and_get_scale(self, dt, motor_current: float = 0, FOS=3.0):
        """
        Updates the temperature of the winding and the case based on the current and the ambient temperature and returns the scale factor for the torque.

        Args:
            dt (float): Time step in seconds.
            motor_current (float, optional): Current in mA. Defaults to 0.
            FOS (float, optional): Factor of safety. Defaults to 3.0.

        Returns:
            float: Scale factor for the torque.

        Dynamics:
            self.C_w * d self.T_w /dt = (I^2)R + (self.T_c-self.T_w)/self.R_WC
            self.C_c * d self.T_c /dt = (self.T_w-self.T_c)/self.R_WC + (self.T_w-self.T_a)/self.R_CA
        """

        I_q_des: float = motor_current * 1e-3

        I2R_des = (
            FOS * I_q_des**2 * self.R_ϕ_0 * (1 + self.α * (self.T_w - self.R_T_0))
        )  # accounts for resistance change due to temp.
        scale = 1.0
        if self.T_w > self.abs_max_temp_windings:
            scale = 0.0
        elif self.T_w > self.soft_max_temp_windings:
            scale *= (self.abs_max_temp_windings - self.T_w) / (
                self.abs_max_temp_windings - self.soft_max_temp_windings
            )

        if self.T_c > self.abs_max_temp_case:
            scale = 0.0
        elif self.T_c > self.soft_max_temp_case:
            scale *= (self.abs_max_temp_case - self.T_w) / (
                self.abs_max_temp_case - self.soft_max_temp_case
            )

        I2R = I2R_des * scale

        dTw_dt = (I2R + (self.T_c - self.T_w) / self.R_WC) / self.C_w
        dTc_dt: float = (
            (self.T_w - self.T_c) / self.R_WC + (self.T_a - self.T_c) / self.R_CA
        ) / self.C_c
        self.T_w += dt * dTw_dt
        self.T_c += dt * dTc_dt

        if scale <= 0.0:
            return 0.0
        if scale >= 1.0:
            return 1.0

        return np.sqrt(scale)  # this is how much the torque should be scaled
