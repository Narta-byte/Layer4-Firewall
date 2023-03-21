library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

entity Tree_logic is
  --type data_array is array (0 to 5) of std_logic_vector(23 downto 0)
  port (
    clk : in std_logic;
    reset : in std_logic;
    key : in std_logic_vector(4 downto 0);
    fileinput : in std_logic_vector(23 downto 0);

    pointer0 : out std_logic_vector(8 downto 0);
    pointer1 : out std_logic_vector(8 downto 0);
    data_out : out std_logic_vector(23 downto 0)
  );
end entity;

architecture rtl of Tree_logic is

begin

  process (clk)
  begin
    if rising_edge(clk) then
      if reset = '1' then
        data_out <= "000000000000000000000000";
      else
        data_out <= fileinput;
      end if;
    end if;
  end process;

end architecture;