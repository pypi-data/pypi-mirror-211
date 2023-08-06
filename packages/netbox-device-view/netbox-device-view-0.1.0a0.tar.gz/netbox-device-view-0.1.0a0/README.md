## netbox-device-view

Display Device Ports

Usage:

For each Device Type you need to add a DeviceView.

Example for Cisco C9300-24T with 8x 10G module

```
/* C9300-24T-8T */
.switchview.area {
	grid-template-areas: "x x x x x x x x x x x x x x gigabitethernet0-1 gigabitethernet0-3 gigabitethernet0-5 gigabitethernet0-7 gigabitethernet0-9 gigabitethernet0-11 s0 gigabitethernet0-13 gigabitethernet0-15 gigabitethernet0-17 gigabitethernet0-19 gigabitethernet0-21 gigabitethernet0-23 s1 tengigabitethernet1-1 tengigabitethernet1-3 tengigabitethernet1-5 tengigabitethernet1-7 s2" "x x x x x x x x x x x x x x gigabitethernet0-2 gigabitethernet0-4 gigabitethernet0-6 gigabitethernet0-8 gigabitethernet0-10 gigabitethernet0-12 s0 gigabitethernet0-14 gigabitethernet0-16 gigabitethernet0-18 gigabitethernet0-20 gigabitethernet0-22 gigabitethernet0-24 s1 tengigabitethernet1-2 tengigabitethernet1-4 tengigabitethernet1-6 tengigabitethernet1-8 s2";
}
```

It will look like

![example](docs/example_view.png)