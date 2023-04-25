library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;
use std.textio.all;
use IEEE.std_logic_textio.all;
use work.my_types_pkg.all;


entity cuckoo_SRAM is
  generic (
    number_of_trees : integer;
    tree_depth : integer;
    address_width : tree_array;
    total_address_width : integer;
    address_width_cumsum : tree_array;
    largest_address_width : integer;
    key_in_lengths : tree_array;
    total_key_in_length : integer;
    tree_cumsum : tree_array;
    codeword_length : tree_array;
    largest_codeword : integer;
    codeword_sum : integer
  );
  port (
    clk : in std_logic;
    reset : in std_logic;
    flush_sram : in std_logic;
    occupied : in std_logic;
    RW : in std_logic;
    address : in std_logic_vector(8 downto 0);
    data_in : in std_logic_vector(codeword_sum - 1 downto 0);
    data_out : out std_logic_vector(codeword_sum - 1 + 1 downto 0)
  );
end cuckoo_SRAM;

architecture cuckoo_SRAM_arch of cuckoo_SRAM is

  type WE_type is array (0 to 2** 9) of std_logic_vector(codeword_sum - 1 + 1 downto 0); --occupied and key  
  signal WE : WE_type := (others => (others => 'U'));

begin
 
  MEMORY : process (clk, reset, flush_sram)

  begin
    if reset = '1' or flush_sram = '1' then
      WE <= (others => (others => '0')); --flush
    elsif rising_edge(clk) then
      if RW = '1' then
        WE(to_integer(unsigned(address))) <= occupied & data_in;
      else
        data_out <= WE(to_integer(unsigned(address)));
      end if;
    end if;
  end process;
  
end architecture; -- SRAM_arch