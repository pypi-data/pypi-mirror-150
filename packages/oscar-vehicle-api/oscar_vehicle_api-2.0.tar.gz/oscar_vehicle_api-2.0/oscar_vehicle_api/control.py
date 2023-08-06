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

import inspect
import sys
import threading
import time
from math import cos, sin, tan, copysign

from . import log


def available_controllers():
    """
    Возвращает словарь с доступными контроллерами
    Ключ - наименование контроллера
    Значение - соответствующий класс контроллера

    :rtype: dict
    """

    controllers = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and name != "BaseController":
            controllers.update({name: obj})

    return controllers


def new_controller(controller_name, vehicle, params = None):
    """
    Возвращает объект контроллера для автомобиля или None в случае
    невозможности найти контроллер с заданным наименованием

    :param controller_name: наименование контроллера
    :type controller_name: str
    :param vehicle: объект автомобиля, используется для получения актуальных
    показаний с автомобиля для реализации управления
    :type vehicle: Vehicle
    :param params: параметры контроллера
    :type params: dict
    """

    if controller_name:
        controllers = available_controllers()
        if controller_name in controllers:
            return controllers[controller_name](vehicle, params)
        else:
            log.print_warn("There is no " + str(controller) + " controller!")

    return None


class BaseController(object):
    """
    Базовый клас контроллера. Не реализует управления и служит для основы для
    создания всех контроллеров, работающих в рамках API. Подкласс Params определяет
    параметры для контроллера по умолчанию.

    :param vehicle: объект автомобиля, используется для получения актуальных
    показаний с автомобиля для реализации управления
    :type vehicle: Vehicle
    :param params: параметры контроллера
    :type params: BaseController.Params
    """

    class Params(dict):

        def __init__(self, *args, **kwargs):

            super(BaseController.Params, self).__init__(*args, **kwargs)


    def __init__(self, vehicle, params = None):
        self._params = {}

        self._vehicle = vehicle

        self._state_lock = threading.Lock()

        self._target_vehicle_speed        = None
        self._target_vehicle_acceleration = None
        self._target_vehicle_jerk         = None
        self._target_vehicle_throttle     = None

        self._target_sw_angle    = None
        self._target_sw_velocity = None
        self._target_sw_torque   = None

        self._output_vehicle_throttle = None
        self._output_sw_torque        = None


    def update_params(self, params):
        self._params.update(params)


    def get_params(self):
        return self._params


    def reset(self):
        pass


    def set_target_move(self, speed        = None,
                              acceleration = None,
                              jerk         = None,
                              throttle     = None):

        self._target_vehicle_speed        = speed
        self._target_vehicle_acceleration = acceleration
        self._target_vehicle_jerk         = jerk
        self._target_vehicle_throttle     = throttle


    def set_target_steering(self, angle    = None,
                                  velocity = None,
                                  torque   = None):

        self._target_sw_angle    = angle
        self._target_sw_velocity = velocity
        self._target_sw_torque   = torque


    def calc_output():
        return self._target_vehicle_throttle, self._target_sw_torque


class SteeringPidDirectThrottle(BaseController):

    MAX_DELAY_IN_CONTROL_LOOP = 0.2

    class Params(dict):

        def __init__(self, *args, **kwargs):

            self["P"]              = 0.1
            self["I"]              = 0.1
            self["I_saturation"]   = 80.
            self["D"]              = 0.001
            self["out_saturation"] = 90.

            super(SteeringPidDirectThrottle.Params, self).__init__(*args, **kwargs)


    def __init__(self, vehicle, params = None):
        super(SteeringPidDirectThrottle, self).__init__(vehicle, params)

        self._target_sw_angle    = self._vehicle.get_steering_wheel_angle()
        self._target_sw_velocity = 0.0

        self._target_vehicle_throttle = 0.0

        self._output_vehicle_throttle = 0.0
        self._output_sw_torque        = 0.0

        self._last_sw_angle_error = 0.0
        self._last_control_time = 0.0

        self._i_term = 0.0

        self._params = params or Params()

        if params:
            self._params.update(params)


    def reset(self):
        # self._last_sw_angle_error = 0.0
        self._last_control_time = time.time()
        self._i_term = 0.0


    def calc_output(self):

        cur_time = time.time()
        d_time = cur_time - self._last_control_time
        self._last_control_time = cur_time

        if self._target_vehicle_throttle < 0:
            self._output_vehicle_throttle = max(self._target_vehicle_throttle, -100)
        else:
            self._output_vehicle_throttle = min(self._target_vehicle_throttle,  100)

        if (d_time > self.MAX_DELAY_IN_CONTROL_LOOP):
            log.print_warn("[ALPHA]: Control loop rate is too low")
            d_time = self.MAX_DELAY_IN_CONTROL_LOOP
            # return self._output_vehicle_throttle, self._output_sw_torque

        # steering wheel control part
        cur_vehicle_speed = self._vehicle.get_vehicle_speed()
        cur_sw_angle, cur_sw_velocity = self._vehicle.get_steering_wheel_angle_and_velocity()

        sw_angle_error = self._target_sw_angle - cur_sw_angle

        p_term = sw_angle_error * self._params['P']

        new_i_term = self._i_term + sw_angle_error * d_time * self._params['I']
        if abs(new_i_term) <  self._params['I_saturation']:
            self._i_term = new_i_term

        d_sw_angle_error = sw_angle_error - self._last_sw_angle_error
        self._last_sw_angle_error = sw_angle_error

        d_term = (d_sw_angle_error / d_time) * self._params['D']

        output_sw_torque = p_term + self._i_term + d_term
        if abs(output_sw_torque) <  self._params['out_saturation']:
            self._output_sw_torque = output_sw_torque

        return self._output_vehicle_throttle, self._output_sw_torque
