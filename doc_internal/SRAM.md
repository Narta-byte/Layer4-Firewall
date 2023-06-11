# Entity: SRAM 

- **File**: SRAM.vhd
## Diagram

![Diagram](SRAM.svg "Diagram")
## Generics

| Generic name    | Type    | Value | Description |
| --------------- | ------- | ----- | ----------- |
| tree_depth      | integer | 16    |             |
| codeword_length | integer | 16    |             |
| address_width   | integer | 8     |             |
## Ports

| Port name | Direction | Type                                                               | Description |
| --------- | --------- | ------------------------------------------------------------------ | ----------- |
| clk       | in        | std_logic                                                          |             |
| reset     | in        | std_logic                                                          |             |
| RW        | in        | std_logic                                                          |             |
| address   | in        | std_logic_vector(address_width - 1 downto 0)                       |             |
| data_in   | in        | std_logic_vector(codeword_length + address_width * 2 - 1 downto 0) |             |
| data_out  | out       | std_logic_vector(codeword_length + address_width * 2 - 1 downto 0) |             |
## Signals

| Name | Type    | Description |
| ---- | ------- | ----------- |
| WE   | WE_type |             |
## Types

| Name    | Type | Description |
| ------- | ---- | ----------- |
| WE_type |      |             |
## Processes
- MEMORY: ( clk, reset )
