# Entity: packet_fifo 

- **File**: fifo.vhd
## Diagram

![Diagram](fifo.svg "Diagram")
## Ports

| Port name | Direction | Type                           | Description |
| --------- | --------- | ------------------------------ | ----------- |
| clock     | in        | STD_LOGIC                      |             |
| data      | in        | STD_LOGIC_VECTOR (10 DOWNTO 0) |             |
| rdreq     | in        | STD_LOGIC                      |             |
| wrreq     | in        | STD_LOGIC                      |             |
| empty     | out       | STD_LOGIC                      |             |
| full      | out       | STD_LOGIC                      |             |
| q         | out       | STD_LOGIC_VECTOR (10 DOWNTO 0) |             |
| usedw     | out       | STD_LOGIC_VECTOR (7 DOWNTO 0)  |             |
## Signals

| Name      | Type                           | Description |
| --------- | ------------------------------ | ----------- |
| sub_wire0 | STD_LOGIC                      |             |
| sub_wire1 | STD_LOGIC                      |             |
| sub_wire2 | STD_LOGIC_VECTOR (10 DOWNTO 0) |             |
| sub_wire3 | STD_LOGIC_VECTOR (7 DOWNTO 0)  |             |
## Instantiations

- scfifo_component: scfifo
