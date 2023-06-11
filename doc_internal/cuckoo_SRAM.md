# Entity: cuckoo_SRAM 

- **File**: cuckoo_SRAM.vhd
## Diagram

![Diagram](cuckoo_SRAM.svg "Diagram")
## Generics

| Generic name          | Type       | Value | Description |
| --------------------- | ---------- | ----- | ----------- |
| number_of_trees       | integer    |       |             |
| tree_depth            | integer    |       |             |
| address_width         | tree_array |       |             |
| total_address_width   | integer    |       |             |
| address_width_cumsum  | tree_array |       |             |
| largest_address_width | integer    |       |             |
| key_in_lengths        | tree_array |       |             |
| total_key_in_length   | integer    |       |             |
| tree_cumsum           | tree_array |       |             |
| codeword_length       | tree_array |       |             |
| largest_codeword      | integer    |       |             |
| codeword_sum          | integer    |       |             |
## Ports

| Port name  | Direction | Type                                                | Description |
| ---------- | --------- | --------------------------------------------------- | ----------- |
| clk        | in        | std_logic                                           |             |
| reset      | in        | std_logic                                           |             |
| flush_sram | in        | std_logic                                           |             |
| occupied   | in        | std_logic                                           |             |
| RW         | in        | std_logic                                           |             |
| address    | in        | std_logic_vector(8 downto 0)                        |             |
| data_in    | in        | std_logic_vector(codeword_sum + 8 - 1 downto 0)     |             |
| data_out   | out       | std_logic_vector(codeword_sum + 8 - 1 + 1 downto 0) |             |
## Signals

| Name | Type    | Description |
| ---- | ------- | ----------- |
| WE   | WE_type |             |
## Types

| Name    | Type | Description |
| ------- | ---- | ----------- |
| WE_type |      |             |
## Processes
- MEMORY: ( clk, reset, flush_sram )
