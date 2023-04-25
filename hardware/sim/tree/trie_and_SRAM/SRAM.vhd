library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;
use std.textio.all;
use IEEE.std_logic_textio.all;

entity SRAM is
    generic (
      tree_depth : integer := 16;
      codeword_length : integer := 16;
      address_width : integer := 8
        
    );


  port (
    clk : in std_logic;
    reset : in std_logic;
    RW : in std_logic;
    address : in std_logic_vector(address_width - 1 downto 0);
    data_in : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
    data_out : out std_logic_vector(codeword_length + address_width * 2 - 1 downto 0)
  );
end SRAM;

architecture SRAM_arch of SRAM is

  type WE_type is array (0 to 2**address_width - 1) of std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);  
  signal WE : WE_type := (others => (others => 'U'));

begin
 
  MEMORY : process (clk, reset)

  begin
    if reset = '1' then
      WE <= (others => (others => 'U'));
    elsif rising_edge(clk) then
      if RW = '1' then
        WE(to_integer(unsigned(address))) <= data_in;
      else
        data_out <= WE(to_integer(unsigned(address)));
      end if;
    end if;
  end process;
  
end architecture;