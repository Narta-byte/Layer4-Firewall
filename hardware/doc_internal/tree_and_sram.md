# Entity: tree_and_sram 

- **File**: tree_and_sram.vhd
## Diagram

![Diagram](tree_and_sram.svg "Diagram")
## Generics

| Generic name    | Type    | Value | Description |
| --------------- | ------- | ----- | ----------- |
| key_length      | integer | 32    |             |
| address_width   | integer | 8     |             |
| codeword_length | integer | 16    |             |
| tree_depth      | integer | 16    |             |
| max_iterations  | integer | 1     |             |
| tree_config     | integer |       |             |
## Ports

| Port name                 | Direction | Type                                           | Description |
| ------------------------- | --------- | ---------------------------------------------- | ----------- |
| key_in                    | in        | std_logic_vector(key_length - 1 downto 0)      |             |
| codeword_in               | in        | std_logic_vector(codeword_length - 1 downto 0) |             |
| zero_pointer              | in        | std_logic_vector(address_width - 1 downto 0)   |             |
| one_pointer               | in        | std_logic_vector(address_width - 1 downto 0)   |             |
| address                   | in        | std_logic_vector(address_width - 1 downto 0)   |             |
| RW                        | in        | std_logic                                      |             |
| codeword                  | out       | std_logic_vector(codeword_length - 1 downto 0) |             |
| rdy_collect_header        | out       | std_logic                                      |             |
| vld_collect_header        | in        | std_logic                                      |             |
| rdy_codeword_concatinator | in        | std_logic                                      |             |
| vld_codeword_concatinator | out       | std_logic                                      |             |
| clk                       | in        | std_logic                                      |             |
| reset                     | in        | std_logic                                      |             |
## Signals

| Name             | Type                                                                | Description |
| ---------------- | ------------------------------------------------------------------- | ----------- |
| wire0            | std_logic_vector(address_width - 1 downto 0)                        |             |
| wire1            | std_logic_vector(address_width - 1 downto 0)                        |             |
| data_from_memory | std_logic_vector(codeword_length + address_width * 2 - 1 downto 0)  |             |
| this_data_in     | std_logic_vector(codeword_length + address_width * 2 - 1 downto 0)  |             |
| junk_a           | std_logic_vector(address_width - 1 downto 0)                        |             |
| junk_aa          | std_logic_vector(address_width - 1 downto 0)                        |             |
| junk_k           | std_logic_vector(key_length - 1 downto 0)                           |             |
| zero_input       | std_logic_vector(address_width - 1 downto 0)                        |             |
| tawire0          | std_logic_vector(address_width - 1 downto 0)                        |             |
| tawire1          | std_logic_vector(address_width - 1 downto 0)                        |             |
| tawire2          | std_logic_vector(address_width - 1 downto 0)                        |             |
| tawire3          | std_logic_vector(address_width - 1 downto 0)                        |             |
| taowire0         | std_logic_vector(address_width - 1 downto 0)                        |             |
| taowire1         | std_logic_vector(address_width - 1 downto 0)                        |             |
| taowire2         | std_logic_vector(address_width - 1 downto 0)                        |             |
| taowire3         | std_logic_vector(address_width - 1 downto 0)                        |             |
| tcwire0          | std_logic_vector(codeword_length - 1 downto 0)                      |             |
| tcwire1          | std_logic_vector(codeword_length - 1 downto 0)                      |             |
| tcwire2          | std_logic_vector(codeword_length - 1 downto 0)                      |             |
| junk_c           | std_logic_vector(codeword_length - 1 downto 0)                      |             |
| trwire0          | std_logic                                                           |             |
| trwire1          | std_logic                                                           |             |
| trwire2          | std_logic                                                           |             |
| tvwire0          | std_logic                                                           |             |
| tvwire1          | std_logic                                                           |             |
| tvwire2          | std_logic                                                           |             |
| tkwire0          | std_logic_vector(key_length - 1 downto 0)                           |             |
| tkwire1          | std_logic_vector(key_length - 1 downto 0)                           |             |
| tkwire2          | std_logic_vector(key_length - 1 downto 0)                           |             |
| swire0           | std_logic_vector(codeword_length + address_width * 2  - 1 downto 0) |             |
| swire1           | std_logic_vector(codeword_length + address_width * 2  - 1 downto 0) |             |
| swire2           | std_logic_vector(codeword_length + address_width * 2  - 1 downto 0) |             |
| swire3           | std_logic_vector(codeword_length + address_width * 2  - 1 downto 0) |             |
| sawire0          | std_logic_vector(address_width - 1 downto 0)                        |             |
| sawire1          | std_logic_vector(address_width - 1 downto 0)                        |             |
| sawire2          | std_logic_vector(address_width - 1 downto 0)                        |             |
| sawire3          | std_logic_vector(address_width - 1 downto 0)                        |             |
| tkcwire0         | std_logic_vector(4 downto 0)                                        |             |
| tkcwire1         | std_logic_vector(4 downto 0)                                        |             |
| tkcwire2         | std_logic_vector(4 downto 0)                                        |             |
| junk_kc          | std_logic_vector(4 downto 0)                                        |             |
## Processes
- mux: ( wire0, address, RW, tawire0, tawire1, tawire2, tawire3 )
## Instantiations

- t0: trie_tree_logic
- t1: trie_tree_logic
- t2: trie_tree_logic
- t3: trie_tree_logic
- s0: SRAM
- s1: SRAM
- s2: SRAM
- s3: SRAM
