# Entity: rule_engine 

- **File**: rule_engine.vhd
## Diagram

![Diagram](rule_engine.svg "Diagram")
## Generics

| Generic name          | Type       | Value              | Description |
| --------------------- | ---------- | ------------------ | ----------- |
| number_of_trees       | integer    | 5                  |             |
| tree_depth            | integer    | 16                 |             |
| address_width         | tree_array | (8,8,8,16,8)       |             |
| total_address_width   | integer    | 48                 |             |
| address_width_cumsum  | tree_array | (0,8,16,24,40,48)  |             |
| largest_address_width | integer    | 16                 |             |
| key_in_lengths        | tree_array | (16,16,16,32,16)   |             |
| total_key_in_length   | integer    | 96                 |             |
| tree_cumsum           | tree_array | (0,16,32,48,80,96) |             |
| codeword_length       | tree_array | (16,16,16,16,16)   |             |
| largest_codeword      | integer    | 16                 |             |
| codeword_sum          | integer    | 80                 |             |
## Ports

| Port name        | Direction | Type                                                 | Description |
| ---------------- | --------- | ---------------------------------------------------- | ----------- |
| cmd_in           | in        | std_logic_vector(4 downto 0)                         |             |
| codeword_in      | in        | std_logic_vector(largest_codeword - 1 downto 0)      |             |
| zero_pointer_in  | in        | std_logic_vector(largest_address_width - 1 downto 0) |             |
| one_pointer_in   | in        | std_logic_vector(largest_address_width - 1 downto 0) |             |
| codeword_out     | out       | std_logic_vector(largest_codeword - 1 downto 0)      |             |
| zero_pointer_out | out       | std_logic_vector(largest_address_width - 1 downto 0) |             |
| one_pointer_out  | out       | std_logic_vector(largest_address_width - 1 downto 0) |             |
| RW               | out       | std_logic_vector(number_of_trees - 1 downto 0)       |             |
| address          | out       | std_logic_vector(largest_address_width - 1 downto 0) |             |
| rdy_driver       | out       | std_logic                                            |             |
| vld_driver       | in        | std_logic                                            |             |
| cuckoo_select    | out       | std_logic                                            |             |
| cuckoo_cmd       | out       | std_logic_vector(1 downto 0)                         |             |
| cuckoo_key_out   | out       | std_logic_vector(codeword_sum + 8 - 1 downto 0)      |             |
| cuckoo_key_in    | in        | std_logic_vector(codeword_sum + 8 - 1 downto 0)      |             |
| cuckoo_rdy       | in        | std_logic                                            |             |
| cuckoo_vld       | out       | std_logic                                            |             |
| cuckoo_set_rule  | out       | std_logic                                            |             |
| clk              | in        | std_logic                                            |             |
| reset            | in        | std_logic                                            |             |
## Signals

| Name        | Type                                                                        | Description |
| ----------- | --------------------------------------------------------------------------- | ----------- |
| rw_reg      | std_logic_vector(number_of_trees - 1 + 1 downto 0)                          |             |
| zeros       | std_logic_vector(largest_codeword + largest_address_width * 2 - 1 downto 0) |             |
| debug       | boolean                                                                     |             |
| address_cnt | natural range 0 to 2**largest_address_width                                 |             |
## Processes
- unnamed: ( clk, reset )
