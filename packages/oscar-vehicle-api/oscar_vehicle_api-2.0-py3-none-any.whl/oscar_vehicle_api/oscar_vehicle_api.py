#!/usr/bin/env python

###############################################################################
# Copyright 2020 ScPA StarLine Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import threading
import time

from math import cos, sin, tan, pi

from .protocol import Protocol, VEHICLE_MODE
from .loops import Spinner
from .asp import print_raw
from .control import *
from .vehicle_interface import SerialVehicleInterface

from . import log

CONTROLLER_RATE  = 50
ODOMETRY_RATE = 50
VEHICLE_MODE_CHECK_RATE = 2
LOG_RATE = 50
LOG_DIR  = "/tmp/oscar_vehicle_api_logs"
ALPHA_PORT = "dev/alpha"


class VehicleParams(dict):
    """
    Класс для задания всех параметров используемого автомобиля. Наследуется от dict.
    Соответственно, параметры задаются как ключи словаря.

    :param wheel_radius: Радиус колес автомобиля [м]
    :param wheel_width: Ширина колес автомобиля [м]
    :param wheelbase: Осевое расстояние между колес [м]
    :param axle_track: Межосевое расстояние [м]
    :param steering_ratio: Передаточное число между углом поворота руля и направляющей угла поворота колес
    :param max_sw_angle: Максимальный угол поворота руля [град]
    :param max_sw_rate: Максимальная скорость вращения руля [град/с]
    :param max_acceleration: Максимальное ускорение [м/с^2]
    :param max_deceleration: Максимальное торможение (положительное значение) [м/с^2]
    :param controller_name: Наименование контроллера автомобиля
    :param controller_rate: Частота расчета управления для автомобиля
    :param controller_params: Параметры контроллера автомобиля
    :param odometry_calc_rate: Частота расчета одометрии автомобиля
    """

    def __init__(self, *args, **kwargs):

        self["wheel_radius"]       = 0.37
        self["wheel_width"]        = 0.25
        self["wheelbase"]          = 2.75
        self["axle_track"]         = 1.64
        self["steering_ratio"]     = 14.8
        self["max_sw_angle"]       = 500
        self["max_sw_rate"]        = 250
        self["max_acceleration"]   = 2.0
        self["max_deceleration"]   = 6.
        self["controller_name"]    = "SteeringPidDirectThrottle"
        self["controller_rate"]    = CONTROLLER_RATE
        self["controller_params"]  = available_controllers()["SteeringPidDirectThrottle"].Params()
        self["odometry_calc_rate"] = ODOMETRY_RATE

        super(VehicleParams, self).__init__(*args, **kwargs)


class Vehicle(object):
    """
    Основной класс для взаимодействия с автомобилем.

    :param port: Абсолютный путь последовательного порта сигмы
    :param params: Объект с параметрами автомобиля
    :type params: VehicleParams or None
    """

    def __init__(self, port   = ALPHA_PORT,
                       params = None):

        self._protocol = Protocol()

        self._vehicle_interface = SerialVehicleInterface(self._protocol, port)
        self._vehicle_interface.start_communication()

        self._params = params or VehicleParams()

        self._raw_control = True

        self._vehicle_mode = VEHICLE_MODE.UNKNOWN

        self._odometry = Odometry(self)

        self._controller = new_controller(self._params["controller_name"],
                                          self,
                                          self._params["controller_params"])

        self._vehicle_log = None
        self._vehicle_log_dir = LOG_DIR

        # spinners ------------------------------------------------------------

        self._vehicle_mode_check_spinner = Spinner(self._check_vehicle_mode,
                                                   VEHICLE_MODE_CHECK_RATE)

        self._vehicle_mode_check_spinner.start()

        self._control_spinner = Spinner(self._calc_control,
                                        self._params["controller_rate"])

        self._odometry_spinner = Spinner(self._odometry.calc_odometry,
                                         self._params["odometry_calc_rate"])

        self._vehicle_log_spinner = Spinner(self._log_vehicle_state,
                                            LOG_RATE)


    # Control -----------------------------------------------------------------

    def start_controller(self):
        if self._controller:
            self._controller.reset()
            self._control_spinner.start()

        if self._control_spinner.is_active():
            self._raw_control = False


    def stop_controller(self):
        self._raw_control = True
        self._control_spinner.stop()


    def set_controller(self, controller_name, params = None):

        if self._control_spinner.is_active():
            self.stop_controller()

        self._controller = new_controller(self._params["controller_name"],
                                          self,
                                          self._params["controller_params"])

        self.start_controller()


    def set_controller_params(self, params):
        if self._controller:
            self._controller.update_params(params)


    def set_controller_rate(self, rate):
        self._control_spinner.set_rate(rate)


    def get_actual_controller_rate(self):
        return self._control_spinner.get_real_rate()


    def _calc_control(self):

        throttle, sw_torque = self._controller.calc_output()

        self._protocol.set_vehicle_throttle(throttle)
        self._protocol.set_steering_wheel_torque(sw_torque)


    def move(self, throttle = None, speed = None, acceleration = None, jerk = None):
        """
        Задает желаемые значения движения автомобиля.
        Учет параметров speed, acceleration и jerk происходит только при
        использовании контроллера (см. Control).

        :param throttle: Ускорение/торможение автомобиля в процентах [-100:100]
        :type throttle: float
        :param speed: Скорость автомобиля (контроллер) [м/с]
        :type speed: float
        :param acceleration: Ускорение автомобиля (контроллер) [м/с^2]
        :type acceleration: float
        :param jerk: Рывок автомобиля (контроллер) [м/с^3]
        :type jerk: float
        """

        if self._raw_control:
            self._protocol.set_vehicle_throttle(throttle)

        else:
            self._controller.set_target_move(speed, acceleration, jerk, throttle)


    def steer(self,  angle = None, velocity = None, torque = None):
        """
        Задает желаемые значения вращения руля автомобиля.
        Учет параметров angle, velocity происходит только при
        использовании контроллера (см. Control).

        :param angle: Угол поворота руля (контроллер) [град]
        :type angle: float
        :param velocity: Скорость вращения руля (контроллер) [град/с]
        :type velocity: float
        :param torque: Момент, прикладываемый к рулю в процентах [-100:100]
        :type torque: float
        """

        if self._raw_control:
            self._protocol.set_steering_wheel_torque(torque)

        else:
            self._controller.set_target_steering(angle, velocity, torque)


    def get_vehicle_speed(self):
        """
        Возвращает текущее значение скорости автомобиля в м/с

        :rtype: float
        """

        return self._protocol.get_vehicle_speed()


    def get_vehicle_acceleration(self):
        return self._protocol.get_vehicle_acceleration()


    def get_steering_wheel_angle(self):
        """
        Возвращает текущий угол поворота руля [град]

        :rtype: float
        """

        return self._protocol.get_steering_wheel_angle()


    def get_steering_wheel_velocity(self):
        """
        Возвращает текущую скорость вращения руля [град/с]

        :rtype: float
        """

        return self._protocol.get_steering_wheel_velocity()


    def get_steering_wheel_angle_and_velocity(self):
        return self._protocol.get_steering_wheel_angle_and_velocity()


    def get_steering_wheel_and_eps_torques(self):
        return self._protocol.get_steering_wheel_and_eps_torques()


    def start_sending_vehicle_move_cmd(self):
        return self._protocol.start_sending_vehicle_move_cmd()


    def stop_sending_vehicle_move_cmd(self):
        return self._protocol.stop_sending_vehicle_move_cmd()


    def start_sending_steering_wheel_torque_cmd(self):
        return self._protocol.start_sending_steering_wheel_torque_cmd()


    def stop_sending_steering_wheel_torque_cmd(self):
        return self._protocol.stop_sending_steering_wheel_torque_cmd()


    # Modes -------------------------------------------------------------------

    def get_mode(self):
        """
        Возвращает текущий режим работы автомобиля

        :rtype: VEHICLE_MODE
        """

        return self._vehicle_mode


    def drive(self, start_send_cmds = True):
        """
        Выполняет перехват управления автомобилем в режим DRIVE (см. VEHICLE_MODE)

        :param start_send_cmds: Начинает потоковую отправку команд для движения и управления рулем автомобиля
        :type start_send_cmds: bool

        :rtype: Bool
        """

        if not self._protocol.drive_mode():
            return False

        if start_send_cmds:
            self.start_send_vehicle_cmd()

        return True


    def reverse(self, start_send_cmds = True):
        """
        Выполняет перехват управления автомобилем в режим REVERSE (см. VEHICLE_MODE)

        :param start_send_cmds: Начинает потоковую отправку команд для движения и управления рулем автомобиля
        :type start_send_cmds: bool

        :rtype: Bool
        """

        if not self._protocol.reverse_mode():
            return False

        if start_send_cmds:
            self.start_send_vehicle_cmd()

        return True


    def manual(self):
        """
        Переводит автомобиль в ручной режим управления MANUAL (см. VEHICLE_MODE)

        :rtype: Bool
        """

        self.stop_send_vehicle_cmd()

        if not self._protocol.manual_mode():
            return False

        return True


    def start_send_vehicle_cmd(self):
        """
        Начинает потоковую отправку команд для движения и управления рулем автомобиля
        """

        self._protocol.start_sending_vehicle_move_cmd()
        self._protocol.start_sending_steering_wheel_torque_cmd()


    def stop_send_vehicle_cmd(self):
        """
        Останавливает потоковую отправку команд для движения и управления рулем автомобиля
        """

        self._protocol.start_sending_vehicle_move_cmd()
        self._protocol.start_sending_steering_wheel_torque_cmd()

        self._protocol.set_vehicle_throttle(0)
        self._protocol.set_steering_wheel_torque(0)


    def _check_vehicle_mode(self):
        vehicle_mode, source = self._protocol.get_mode()

        if self._vehicle_mode != vehicle_mode:

            if (source != self._protocol.launcher_info.SOURCE_CMD):     # bad

                if (vehicle_mode == VEHICLE_MODE.DRIVE or
                    vehicle_mode == VEHICLE_MODE.REVERSE):

                    self._protocol.start_sending_vehicle_move_cmd()
                    self._protocol.start_sending_steering_wheel_torque_cmd()

                elif vehicle_mode == VEHICLE_MODE.MANUAL:
                    self._protocol.stop_sending_vehicle_move_cmd()
                    self._protocol.stop_sending_steering_wheel_torque_cmd()
                    self._protocol.set_vehicle_throttle(0)
                    self._protocol.set_steering_wheel_torque(0)

            self._vehicle_mode = vehicle_mode


    # STOPs -------------------------------------------------------------------

    def emergency_stop(self):
        """
        Включает режим экстренного торможения

        :rtype: Bool
        """

        return self._protocol.emergency_stop_on()


    def emergency_stop_off(self):
        """
        Выключает режим экстренного торможения

        :rtype: Bool
        """

        return self._protocol.emergency_stop_off()


    def recover(self):
        return (self._protocol.hand_brake_off() and
                self._protocol.emergency_stop_off())


    def hand_brake_on(self):
        """
        Активирует ручной тормоз

        :rtype: Bool
        """

        return self._protocol.hand_brake_on()


    def hand_brake_off(self):
        """
        Снимает ручной тормоз

        :rtype: Bool
        """

        return self._protocol.hand_brake_off()


    def get_emergency_stop(self):
        """
        Возвращает текущее состояние режима экстренного торможения

        :rtype: Bool
        """
        return self._protocol.get_emergency_stop()


    def get_hand_brake(self):
        """
        Возвращает текущее состояние ручного тормоза

        :rtype: Bool
        """

        return self._protocol.get_hand_brake()


    # Lights ------------------------------------------------------------------

    def led_blink(self):
        return self._protocol.led_blink()


    def led_on(self):
        return self._protocol.led_on()


    def led_off(self):
        return self._protocol.led_off()


    def get_led(self):
        return self._protocol.get_led()


    def left_turn_signal(self):
        """
        Включает левый сигнал поворота

        """

        self._protocol.left_turn_signal()


    def right_turn_signal(self):
        """
        Включает правый сигнал поворота

        """

        self._protocol.right_turn_signal()


    def emergency_signals(self):
        """
        Включает аварийную сигнализацию

        """

        self._protocol.emergency_signals()


    def turn_off_signals(self):
        """
        Выключает сигналы поворота и аварийную сигнализацию

        """

        self._protocol.turn_off_signals()


    # Logger ------------------------------------------------------------------

    def _log_vehicle_state(self):
        cur_time = time.time()

        mode = self.get_mode()

        vehicle_speed         = self._protocol.get_vehicle_speed()
        sw_angle, sw_velocity = self._protocol.get_steering_wheel_angle_and_velocity()
        sw_torque, eps_torque = self._protocol.get_steering_wheel_and_eps_torques()

        self._vehicle_log.add_data(cur_time,
                                   sw_angle,
                                   sw_velocity,
                                   sw_torque,
                                   eps_torque,
                                   vehicle_speed,
                                   mode)


    def start_vehicle_logger(self):
        self._vehicle_log = log.VehicleLog(self._vehicle_log_dir)
        self._vehicle_log_spinner.start()


    def change_vehicle_logger_dir(self, log_dir):
        self._vehicle_log_dir = log_dir


    def stop_vehicle_logger(self):
        self._vehicle_log_spinner.stop()
        self._vehicle_log.save()
        self._vehicle_log = None


    def error_report(self):
        return 'NO_ERROR'


    # Odometry ----------------------------------------------------------------

    def start_odometry_calculation(self):
        if self._odometry_spinner.is_active():
            self._odometry_spinner.stop()
            self._odometry.reset()
        self._odometry_spinner.start()


    def stop_odometry_calculation(self):
        self._odometry_spinner.stop()


    def get_odometry(self):
        return self._odometry.get()


    def reset_odometry(self):
        self._odometry.reset()


    def set_odometry_calc_rate(self, rate):
        self._odometry_spinner.set_rate(rate)


    def get_actual_odometry_calc_rate(self):
        return self._odometry_spinner.get_real_rate()


class Odometry():

    def __init__(self, vehicle):

        self._vehicle = vehicle

        self.wheelbase      = vehicle._params["wheelbase"]
        self.steering_ratio = vehicle._params["steering_ratio"]

        self._pose_data_lock = threading.Lock()
        self.x    = 0.0
        self.y    = 0.0
        self.yaw  = 0.0
        self.dx   = 0.0
        self.dy   = 0.0
        self.dyaw = 0.0
        self.time = 0.0


    def get(self):
        return self.x, self.y, self.yaw, self.dx, self.dy, self.dyaw, self.time


    def reset(self):
        with self._pose_data_lock:
            self.x    = 0.0
            self.y    = 0.0
            self.yaw  = 0.0
            self.dx   = 0.0
            self.dy   = 0.0
            self.dyaw = 0.0
            self.time = 0.0


    def calc_odometry(self):

        cur_time = time.time()
        cur_vehicle_velocity          = self._vehicle.get_vehicle_speed()
        cur_sw_angle, cur_sw_velocity = self._vehicle.get_steering_wheel_angle_and_velocity()
        cur_vehicle_steering_angle = (cur_sw_angle * pi / 180) / self.steering_ratio

        with self._pose_data_lock:

            dt = cur_time - self.time

            self.dx = cos(self.yaw) * cur_vehicle_velocity
            self.dy = sin(self.yaw) * cur_vehicle_velocity
            self.dyaw = cur_vehicle_velocity / self.wheelbase * tan(cur_vehicle_steering_angle)

            self.x += dt * self.dx
            self.y += dt * self.dy
            self.yaw += dt * self.dyaw

            self.time = cur_time
