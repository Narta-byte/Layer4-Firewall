# Entity: codeword_concatinator 

- **File**: codeword_concatinator.vhd
## Diagram

![Diagram](codeword_concatinator.svg "Diagram")
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
## Ports

| Port name       | Direction | Type                                                              | Description |
| --------------- | --------- | ----------------------------------------------------------------- | ----------- |
| codeword_in     | in        | std_logic_vector(largest_codeword * number_of_trees - 1 downto 0) |             |
| codeword_out    | out       | std_logic_vector(largest_codeword * number_of_trees - 1 downto 0) |             |
| rdy_tree        | out       | std_logic_vector(number_of_trees - 1 downto 0)                    |             |
| vld_tree        | in        | std_logic_vector(number_of_trees - 1 downto 0)                    |             |
| rdy_cuckoo_hash | in        | std_logic                                                         |             |
| vld_cuckoo_hash | out       | std_logic                                                         |             |
| clk             | in        | std_logic                                                         |             |
| reset           | in        | std_logic                                                         |             |
## Signals

| Name        | Type                                           | Description |
| ----------- | ---------------------------------------------- | ----------- |
| flag        | std_logic_vector(number_of_trees - 1 downto 0) |             |
| wait_signal | std_logic_vector(number_of_trees - 1 downto 0) |             |
| lock        | std_logic                                      |             |
| reg         | std_logic                                      |             |
## Constants

| Name                   | Type                                           | Value                              | Description |
| ---------------------- | ---------------------------------------------- | ---------------------------------- | ----------- |
| total_code_word_length | integer                                        | largest_codeword * number_of_trees |             |
| ones                   | std_logic_vector(number_of_trees - 1 downto 0) | (others => '1')                    |             |
## Processes
- unnamed: ( clk, reset )
