library ieee;
use ieee.std_logic_1164.all;
use IEEE.numeric_std.all;

entity my_array is
  generic (
    ROWS : integer := 4; -- number of rows in the array
    COLS : integer := 4 -- number of columns in the array
  );
  port (
    clk : in std_logic;
    rst : in std_logic;
    row_idx : in std_logic_vector(ROWS - 1 downto 0);
    col_idx : in std_logic_vector(COLS - 1 downto 0);
    data_out : out std_logic
  );
end my_array;

architecture behavioral of my_array is
  type array_type is array(0 to ROWS - 1, 0 to COLS - 1) of std_logic;
  signal array2d : array_type := (
  ('1', '0', '1', '0'),
    ('0', '1', '0', '1'),
    ('1', '0', '1', '0'),
    ('0', '1', '0', '1')
  );
begin
  process (clk)
  begin
    if rising_edge(clk) then
      if rst = '0' then
        data_out <= '0';
      else
        data_out <= array2d(to_integer(unsigned(row_idx)), to_integer(unsigned(col_idx)));
      end if;
    end if;
  end process;
end behavioral;