-- vsg_off
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;
-- use ieee.std_logic_textio.all;

library std;
-- use ieee.std_logic_unsigned.all;
use ieee.std_logic_textio.all;

entity tree_logic_tb is
end entity tree_logic_tb;

architecture bench of tree_logic_tb is

  -- file input : text open read_mode is "Trienodes.txt";
  component tree_logic is
    port (
      clk : in std_logic;
      reset : in std_logic;
      key : in std_logic_vector(4 downto 0);
      fileinput : in std_logic_vector(23 downto 0);
      pointer0 : out std_logic_vector(8 downto 0);
      pointer1 : out std_logic_vector(8 downto 0);
      data_out : out std_logic_vector(23 downto 0)
    );
  end component;

  -- Clock period
  constant clk_period : time := 5 ns;
  -- Generics

  -- Ports
  signal clk : std_logic;
  signal reset : std_logic;
  signal key : std_logic_vector(4 downto 0);
  signal fileinput : std_logic_vector(23 downto 0);
  signal pointer0 : std_logic_vector(8 downto 0);
  signal pointer1 : std_logic_vector(8 downto 0);
  signal data_out : std_logic_vector(23 downto 0);

  type data_array is array (0 to 5) of std_logic_vector(23 downto 0);

  signal data_array_sig : data_array;

begin

  tree_logic_inst : component tree_logic
    port map(
      clk => clk,
      reset => reset,
      key => key,
      fileinput => fileinput,
      pointer0 => pointer0,
      pointer1 => pointer1,
      data_out => data_out
    );

    process (clk) is

      file input : text open read_mode is "Trienodes.txt";

      variable current_read_line : line;
      variable hex_reader : std_logic_vector(23 downto 0);

    begin

      read_array : for i in 0 to 5 loop

        if (not endfile(input)) then
          readline(input, current_read_line);
          read(current_read_line, hex_reader);
          -- write(OUTPUT, current_read_line.all & LF);

          -- data_out <= hex_reader;
          -- data_array_sig(i) <= hex_reader;
          -- fileinput <= current_read_line;
          -- wait for clk_period;
          fileinput <= hex_reader;
          -- fileinput <= data_array_sig(4);

        end if;

      end loop; -- READ_ARRAY

    end process;

    clk_process : process is
    begin

      while now < 1000 ns loop

        clk <= '1';
        wait for clk_period / 2;
        clk <= '0';
        wait for clk_period / 2;

      end loop;

    end process clk_process;

  end architecture bench;