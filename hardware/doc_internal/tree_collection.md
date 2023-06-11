# Entity: tree_collection 

- **File**: tree_collection.vhd
## Diagram

![Diagram](tree_collection.svg "Diagram")
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
| max_iterations        | tree_array | (1,1,1,1,1)        |             |
| tree_config           | tree_array | (1,1,1,1,1)        |             |
## Ports

| Port name          | Direction | Type                                                              | Description |
| ------------------ | --------- | ----------------------------------------------------------------- | ----------- |
| key_in             | in        | std_logic_vector(total_key_in_length - 1 downto 0)                |             |
| codeword_in        | in        | std_logic_vector(largest_codeword - 1 downto 0)                   |             |
| zero_pointer       | in        | std_logic_vector(largest_address_width - 1 downto 0)              |             |
| one_pointer        | in        | std_logic_vector(largest_address_width - 1 downto 0)              |             |
| address            | in        | std_logic_vector(largest_address_width - 1 downto 0)              |             |
| RW                 | in        | std_logic_vector(number_of_trees - 1 downto 0)                    |             |
| rdy_collect_header | out       | std_logic_vector(number_of_trees - 1 downto 0)                    |             |
| vld_collect_header | in        | std_logic_vector(number_of_trees -1 downto 0)                     |             |
| codeword_out       | out       | std_logic_vector(largest_codeword * number_of_trees - 1 downto 0) |             |
| cuckoo_codeword    | out       | std_logic_vector(largest_codeword * number_of_trees - 1 downto 0) |             |
| rdy_cuckoo_hash    | in        | std_logic                                                         |             |
| vld_cuckoo_hash    | out       | std_logic                                                         |             |
| clk                | in        | std_logic                                                         |             |
| reset              | in        | std_logic                                                         |             |
## Signals

| Name               | Type                                                              | Description |
| ------------------ | ----------------------------------------------------------------- | ----------- |
| w_rdy_concatinator | std_logic_vector(number_of_trees - 1 downto 0)                    |             |
| w_vld_concatinator | std_logic_vector(number_of_trees - 1 downto 0)                    |             |
| debug              | std_logic_vector(15 downto 0)                                     |             |
| codeword_to_concat | std_logic_vector(largest_codeword * number_of_trees - 1 downto 0) |             |
## Constants

| Name                   | Type    | Value                                        | Description |
| ---------------------- | ------- | -------------------------------------------- | ----------- |
| data_in_length         | integer | largest_codeword + largest_address_width * 2 |             |
| total_code_word_length | integer | largest_codeword * number_of_trees           |             |
## Instantiations

- codeword_concatinator_inst: codeword_concatinator
