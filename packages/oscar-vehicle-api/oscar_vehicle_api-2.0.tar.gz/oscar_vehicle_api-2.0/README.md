### OSCAR vehicle API

Репозиторий содержит API низкоуровневой системы управления автомобилем [Alpha](alpha.starline.ru), разрабатываемой в рамках проекта [OSCAR](https://gitlab.com/starline/oscar), для беспилотных транспортных средств.


#### Установка с PyPI

```
pip3 install --user oscar_vehicle_api
```


#### Установка из исходников

```
git clone https://gitlab.com/starline/oscar_vehicle_api.git && cd oscar_vehicle_api
pip3 install --user -e .
```


#### Использование

```
import oscar_vehicle_api as oscar
vehicle = oscar.Vehicle(“/dev/ttyACM0”)
vehicle.drive()
vehicle.steer(20)
vehicle.move(10)
vehicle.manual()
vehicle.led_blink()
vehicle.emergency_stop()
vehicle.recover()
vehicle.left_turn_signal()
vehicle.right_turn_signal()
vehicle.emergency_signals()
vehicle.turn_off_signals()
vehicle.get_vehicle_speed()
```
