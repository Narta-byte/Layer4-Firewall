library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity my_array_tb is
end my_array_tb;

architecture behavioral of my_array_tb is
  constant ROWS : integer := 4;
  constant COLS : integer := 4;

  signal clk : std_logic := '0';
  signal rst : std_logic := '0';
  signal row_idx : std_logic_vector(ROWS - 1 downto 0);
  signal col_idx : std_logic_vector(COLS - 1 downto 0);
  signal data_out : std_logic;

  component my_array
    generic (
      ROWS : integer := 4;
      COLS : integer := 4
    );
    port (
      clk : in std_logic;
      rst : in std_logic;
      row_idx : in std_logic_vector(ROWS - 1 downto 0);
      col_idx : in std_logic_vector(COLS - 1 downto 0);
      data_out : out std_logic
    );
  end component;

begin

  dut : my_array
  generic map(
    ROWS => ROWS,
    COLS => COLS
  )
  port map(
    clk => clk,
    rst => rst,
    row_idx => row_idx,
    col_idx => col_idx,
    data_out => data_out
  );

  -- Clock generation process
  clk_gen : process
  begin
    while now < 1000 ns loop
      clk <= '0';
      wait for 10 ns;
      clk <= '1';
      wait for 10 ns;
    end loop;
    wait;
  end process clk_gen;

  -- Reset process
  rst_proc : process
  begin
    rst <= '1';
    wait for 10 ns;
    rst <= '0';
    wait for 10 ns;
    rst <= '1';
    wait;
  end process rst_proc;

  -- Test process
  test_proc : process
  begin
    -- Test each element of the array
    for i in 0 to ROWS - 1 loop
      for j in 0 to COLS - 1 loop
        row_idx <= std_logic_vector(to_unsigned(i, row_idx'length));
        col_idx <= std_logic_vector(to_unsigned(j, col_idx'length));
        wait for 10 ns;
        --assert to_bit(data_out) = to_bit(((i + j) mod 2)) report "Unexpected value at (" & integer'image(i) & ", " & integer'image(j) & ")" severity error;
      end loop;
    end loop;

    -- Test out-of-bounds indices
    --row_idx <= ROWS;
    --col_idx <= COLS;
    wait for 10 ns;
    --assert to_bit(data_out) = '0' report "Unexpected value at out-of-bounds index" severity error;

    wait;
  end process test_proc;

end behavioral;