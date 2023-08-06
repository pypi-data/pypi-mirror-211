# KiwiCoder
A biology framework for biological experiments.



## Quick Start

KiwiCoder can be installed using pip

```
pip install KiwiCoder
```

You can generate your first project.

```
kiwi-gen {your path}
```

The project hierarchy is shown as below.
```
├── keee-weee
│    ├── report
│       ├── formal.html
│    	├── process_graph.dot
│    ├── user
│       ├── __init__.py
│    	├── override.py
│    	├── protocol.py
├── __main__.py
```

You can define your experiment protocol by finishing `protocol.py` .

Function `kiwi_protocol` is the main function for protocol. You should NOT rename the function or write a new one.

```python
# define experiment protocol in this file
from kiwi import Step

def kiwi_protocol():
	""" Define experiment protocol. """
	Step("example step 1", "sn:1")
```

If you want to use user-defined class or functions, you can override them in `override.py` .

Then you can run the main script, and a command line will appear. You can run your protocol by entering the following commands.

```
kiwi>auto
```



## Usage

### Commands

#### load & scan & run

You can initialize the experiment by following commands.

```
kiwi>load
kiwi>scan
kiwi>run
```

* load: load the protocol and user-defined objects.
* scan: scan the protocol and build basic runtime environment.
* run: run the whole experiment.

#### ctrl

You can control and debug by following commands.

```
kiwi> ctrl -sp {step number} -op {operation index} {signal parameter}
```

* ctrl: the control command

| Signal   | Signal Parameter |
| -------- | ---------------- |
| STOP     | s                |
| RUN      | r                |
| SUSPEND  | p                |
| KILL     | k                |
| CONTINUE | c                |

#### sys

You can get or set some system variables or status by following commands.

```
kiwi>sys show {var name}
kiwi>sys set {var name} {var value}
```

#### gen

You can generate report or process graph by following commands.

```
kiwi>gen report {file name without suffix}
kiwi>gen process {file name without suffix}
```



### Experiment Report

You can generate your report in html format, with a dot file which contains the experiment graph.

```
├── ..
│    ├── report
│       ├── formal.html
│    	├── process_graph.dot
```



### Monitor

You can add bio object that required to be monitored just in protocol file.

A watched variable attribute will send message when its value changes.

An alarmed variable attribute will send message when its value exceeds the threshold value.

watch_list is composed of variable name and its attribute.

alarm_list is composed of variable name, attribute, math operation and threshold value.

```python
# protocol.py
def watch():
    watch_list = [
        ("eppendorf_name", "volume")
    ]
    return watch_list


def alarm():
    alarm_list = [
        ("eppendorf_name", "volume", MathOp.LE, Volume(200, "ml"))
    ]
    return alarm_list
```

You can also monitor with class decorator in self-defined class. Nothing will be overwritten unless the attribute name is same.

```python
@watch_change(watch_list=["attr1"], alarm_list=[("attr2",MathOp.LE,Any)])
class Example(BioObject):
	pass
```

**ATTENTION:**  ALL monitored variables need to be assigned name explicitly when they initialize as shown below.

```python
eppendorf = Container(ContainerType.EPPENDORF, name="eppendorf_name")
```



### Mock

You can mock both bio obj and operation in protocol in `mock` function in `protocol.py`.

```python
# protocol.py
def mock():
    mock_bio_obj_list = {"INCLUDE": ["eppendorf_name"]}
    mock_op_list = {"INCLUDE": ["$ALL$"], "EXCLUDE": ["sn:1,op:0"]}
    return mock_bio_obj_list, mock_op_list
```

ALL mocked variables need to be assigned name explicitly when they initialize.

#### Mock Operation

When an operation is mocked, `_mock_run` will be executed when the operation runs instead of `_run`. 

#### Mock Bio Object

You can also mock by decorator `@class_mock_enable`. This annotation enables you to specify a function with mock prefix and suffix `__mock_{real func name}__` . When the bio object is in mock status, the mock function will be executed instead of the non-mock one.

```python
@class_mock_enable
class FlowMeter(MeasureInstrumPeriphery):
    def __init__(self, mock=False, mock_obj=None):
        super().__init__(mock=mock, mock_obj=mock_obj)

    def read(self) -> Optional[float]:
        pass

    def __mock_read__(self) -> Optional[float]:
        pass
```

You can create a new class as `mock_obj` , and pass it as parameter in constructor.  The decorator `@class_mock_enable` will call function in `mock_obj` instead search the function in its class.  



### Customize Class

You may need to write your own class, or override the built-in class in KiwiCoder. Then you should add your customized class in `override.py` . 

The name of your class should be same as the one in built-in.

KiwiCoder will load customize class in priority.



## Example

```python
def kiwi_protocol():
    start_protocol("DNA Oligo Synthesis")

    ''' define peripheries '''
    pump_relay = ControlPeriphery(company="Phidget", product="Relay", comment="", name="pump_relay", vintport=1)
    valve_relay = ControlPeriphery(company="Phidget", product="Relay", comment="", name="valve_relay", vintport=2)

    pump0 = SignalPeriphery(company="", product="Pump", comment="", name="pump0", usage=PeripheryUsage.DRIVER,
                            control_periphery=pump_relay, port=11, flow_rate=FlowRate(5, "ml/s"))
    pump1 = SignalPeriphery(company="", product="Pump", comment="", name="pump1", usage=PeripheryUsage.DRIVER,
                            control_periphery=pump_relay, port=12, flow_rate=FlowRate(5, "ml/s"))
    pump2 = SignalPeriphery(company="", product="Pump", comment="", name="pump2", usage=PeripheryUsage.DRIVER,
                            control_periphery=pump_relay, port=13, flow_rate=FlowRate(5, "ml/s"))
    pump3 = SignalPeriphery(company="", product="Pump", comment="", name="pump3", usage=PeripheryUsage.DRIVER,
                            control_periphery=pump_relay, port=10, flow_rate=FlowRate(5, "ml/s"))
    pump4 = SignalPeriphery(company="", product="Pump", comment="", name="pump4", usage=PeripheryUsage.DRIVER,
                            control_periphery=pump_relay, port=15, flow_rate=FlowRate(5, "ml/s"))

    valve_a = SignalPeriphery(company="", product="Valve", comment="", name="valve_a", usage=PeripheryUsage.VALVE,
                              control_periphery=valve_relay, port=4)
    valve_t = SignalPeriphery(company="", product="Valve", comment="", name="valve_t", usage=PeripheryUsage.VALVE,
                              control_periphery=valve_relay, port=3)
    valve_c = SignalPeriphery(company="", product="Valve", comment="", name="valve_c", usage=PeripheryUsage.VALVE,
                              control_periphery=valve_relay, port=5)
    valve_g = SignalPeriphery(company="", product="Valve", comment="", name="valve_g", usage=PeripheryUsage.VALVE,
                              control_periphery=valve_relay, port=7)
    valve_act = SignalPeriphery(company="", product="Valve", comment="", name="valve_act", usage=PeripheryUsage.VALVE,
                                control_periphery=valve_relay, port=2)
    valve_chem = SignalPeriphery(company="", product="Valve", comment="", name="valve_chem", usage=PeripheryUsage.VALVE,
                                 control_periphery=valve_relay, port=1)
    valve_wet = SignalPeriphery(company="", product="Valve", comment="", name="valve_wet", usage=PeripheryUsage.VALVE,
                                control_periphery=valve_relay, port=6)
    valve_dry = SignalPeriphery(company="", product="Valve", comment="", name="valve_dry", usage=PeripheryUsage.VALVE,
                                control_periphery=valve_relay, port=0)
    valve_zero_dead = SignalPeriphery(company="", product="Valve", comment="", name="valve_zero_dead",
                                      usage=PeripheryUsage.VALVE,
                                      control_periphery=valve_relay, port=9)

    flowmeter = InstrumPeriphery(company="", product="FlowMeter", comment="", name="flowmeter",
                                 usage=PeripheryUsage.MEASURE, port="COM8")

    ''' define samples '''
    dna_a = Fluid("A", "A sample", sample_io_peripheries=[valve_a])
    dna_t = Fluid("T", "T sample", sample_io_peripheries=[valve_t])
    dna_c = Fluid("C", "C sample", sample_io_peripheries=[valve_c])
    dna_g = Fluid("G", "G sample", sample_io_peripheries=[valve_g])
    act = Fluid("ACT", "ACT sample", sample_io_peripheries=[valve_act])
    chem = Fluid("CHEM", "CHEM sample", sample_io_peripheries=[valve_chem])
    wet = Fluid("WET", "WET sample", sample_io_peripheries=[valve_wet])
    dry = Fluid("DRY", "DRY sample", sample_io_peripheries=[valve_dry])

    synthesis_container = Container(ContainerType.FLASK, name="container", sample_io_peripheries=[],
                                    volume=Volume(100, "ml"))
    store_container = Container(ContainerType.EPPENDORF, name="store container", sample_io_peripheries=[],
                                    volume=Volume(5, "ml"))

    Step("step 1, waiting and initializing", "sn:1")
    wait(synthesis_container, Time(5.0, "s"))

    ''' target seq '''
    target_seq = "ATCG"

    Step("step 2, oligo synthesis", "sn:2")

    for ch in target_seq:
        direct_call(valve_zero_dead, "shutdown", {})
        if ch == 'A':
            measure_fluid(dna_a, synthesis_container, Volume(1, "ml"), [flowmeter, pump4], AutoLevel.FULL)
        elif ch == 'T':
            measure_fluid(dna_t, synthesis_container, Volume(1, "ml"), [flowmeter, pump1], AutoLevel.FULL)
        elif ch == 'C':
            measure_fluid(dna_c, synthesis_container, Volume(1, "ml"), [flowmeter, pump2], AutoLevel.FULL)
        elif ch == 'G':
            measure_fluid(dna_g, synthesis_container, Volume(1, "ml"), [flowmeter, pump3], AutoLevel.FULL)
        direct_call(valve_zero_dead, "start", {})
        measure_fluid(act, synthesis_container, Volume(1, "ml"), [flowmeter, pump2], AutoLevel.FULL)
        measure_fluid(dry, synthesis_container, Volume(1, "ml"), [flowmeter, pump4], AutoLevel.FULL)

    Step("step 3, dissociation", "sn:3")
    direct_call(valve_zero_dead, "start", {})
    measure_fluid(chem, synthesis_container, Volume(1, "ml"), [flowmeter, pump1], AutoLevel.FULL)
    direct_call(valve_zero_dead, "shutdown", {})
    measure_fluid(wet, synthesis_container, Volume(1, "ml"), [flowmeter, pump0], AutoLevel.FULL)

    Step("step 4, transfer and store", "sn:4")
    transfer(synthesis_container, store_container, [], AutoLevel.FULL)
    store(store_container, Temperature(Temperature.ON_ICE), [], AutoLevel.FULL)

    end_protocol()
```



