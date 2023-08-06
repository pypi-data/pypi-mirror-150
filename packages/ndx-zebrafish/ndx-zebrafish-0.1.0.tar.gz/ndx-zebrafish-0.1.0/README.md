# ndx-zebrafish Extension for NWB

Provides standard container formats for tracking zebrafish behavior.
For now tail and position tracking are specified, with

## Installation


```bash

python -m pip install ndx-zebrafish

```

## Usage

Example storage of freely-swimming fish tracking data:

```python
tail_direction = pynwb.behavior.SpatialSeries(
    "fish_direction",
    {},
    timestamps={},
)
tail_shape = pynwb.behavior.SpatialSeries(
    "tail_shape",
    {},
    timestamps={},
    unit="radians",
)
position = pynwb.behavior.SpatialSeries(
    "fish_position",
    {}
    timestamps={},
    unit="mm",
)

behavior_storage = ZebrafishBehavior(
    name=f"fish_{i_fish}_behavior",
    fish_id=i_fish,
    position=position,
    orientation=tail_direction,
    tail_shape=tail_shape,
)

```

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
