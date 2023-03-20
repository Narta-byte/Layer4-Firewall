use std.textio.all;
library vunit_lib;
context vunit_lib.vunit_context;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity my_array_tb is
  generic (
    runner_cfg : string := runner_cfg_default;
    -- output_path : string;
    rowing : natural;
    coling : natural
    -- sign : boolean;
    -- message : string
  );
end entity my_array_tb;

architecture behavioral of my_array_tb is

  constant rows : integer := 4;
  constant cols : integer := 4;

  signal clk : std_logic := '0';
  signal rst : std_logic := '0';
  signal row_idx : std_logic_vector(rows - 1 downto 0);
  signal col_idx : std_logic_vector(cols - 1 downto 0);
  --signal rowing : std_logic_vector(rows - 1 downto 0);
  --signal coling : std_logic_vector(cols - 1 downto 0);
  signal data_out : std_logic;
  signal data_out_for_test : std_logic;

  component my_array is
    generic (
      rows : integer := 4;
      cols : integer := 4
    );
    port (
      rowing : in natural;
      coling : in natural;
      data_out_for_test : out std_logic;

      clk : in std_logic;
      rst : in std_logic;
      row_idx : in std_logic_vector(rows - 1 downto 0);
      col_idx : in std_logic_vector(cols - 1 downto 0);
      data_out : out std_logic
    );
  end component;

begin

  dut : component my_array
    generic map(
      rows => rows,
      cols => cols
    )
    port map(
      data_out_for_test => data_out_for_test,
      rowing => rowing,
      coling => coling,

      clk => clk,
      rst => rst,
      row_idx => row_idx,
      col_idx => col_idx,
      data_out => data_out
    );

    test_proc : process is
    begin

      test_runner_setup(runner, runner_cfg);
      wait for 200 ns;
      while test_suite loop
        if run("Test_with_loop") then
          -- Test forloops
          assert data_out_for_test = '1' report "Error. test_loop exp = '1'" severity error;

        elsif run("test_pass") then
          -- Test reading the last element
          assert data_out_for_test = '1' report "Error. Expected data_out for test_pass = '1'" severity error;

        elsif run("2nd test") then
          -- Test for reading middle element
          assert data_out_for_test = '1' report "Error. Expected data_out for 2nd test = '1'" severity error;

        elsif run("test_fail") then
          assert false report "It fails :(";

        end if;
      end loop;
      test_runner_cleanup(runner);

    end process test_proc; -- EOF --

    -- Clock generation process
    clk_gen : process is
    begin
      rst <= '1';
      wait for 10 ns;
      rst <= '0';
      while now < 1000 ns loop
        clk <= '0';
        wait for 10 ns;
        clk <= '1';
        wait for 10 ns;
      end loop;
      wait;
    end process clk_gen;
  end architecture behavioral;