library ieee;
library std;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use IEEE.std_logic_textio.all;
use std.textio.all;

entity tree_and_sram_tb is
end;

architecture bench of tree_and_sram_tb is

  component tree_and_sram
    generic (
      key_length : integer;
      address_width : integer;
      codeword_length : integer;
      tree_depth : integer
    );
      port (
      key_in : in std_logic_vector(key_length downto 0);
      codeword : out std_logic_vector(codeword_length - 1 downto 0);
      data_in : in std_logic_vector(codeword_length + address_width * 2 downto 0);
      address : in std_logic_vector(address_width downto 0);
      RW : in std_logic;
      rdy_collect_header : out std_logic;
      vld_collect_header : in std_logic;
      rdy_codeword_concatinator : in std_logic;
      vld_codeword_concatinator : out std_logic;

      clk : in std_logic;
      reset : in std_logic
    );
  end component;

  -- Clock period
  constant clk_period : time := 5 ns;
  -- Generics
  constant key_length : integer := 16;
  constant address_width : integer := 8;
  constant codeword_length : integer := 16;
  constant tree_depth : integer := 16;

  -- Ports
  signal key_in : std_logic_vector(key_length - 1 downto 0);
  signal codeword : std_logic_vector(codeword_length - 1 downto 0);
  signal data_in : std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
  signal address : std_logic_vector(address_width - 1 downto 0);
  signal RW : std_logic := '0';
  signal rdy_collect_header : std_logic;
  signal vld_collect_header : std_logic:= '0';
  signal clk : std_logic;
  signal reset : std_logic;
  signal cnt : integer := 0;
  signal wait_cnt : integer := 0;  
  signal rdy_codeword_concatinator : std_logic := '1';
  signal vld_codeword_concatinator : std_logic;
begin

  tree_and_sram_inst : tree_and_sram
    generic map (
      key_length => key_length,
      address_width => address_width,
      codeword_length => codeword_length,
      tree_depth => tree_depth
    )
    port map (
      key_in => key_in,
      codeword => codeword,
      data_in => data_in,
      address => address,
      RW => RW,
      rdy_collect_header => rdy_collect_header,
      vld_collect_header => vld_collect_header,
      rdy_codeword_concatinator => rdy_codeword_concatinator,
      vld_codeword_concatinator => vld_codeword_concatinator,
      clk => clk,
      reset => reset
    );

  clk_process : process
  begin
  clk <= '1';
  wait for clk_period/2;
  clk <= '0';
  wait for clk_period/2;
  end process clk_process;

  Read_file :  process (clk)
    file input : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/tree/tree_data_tb.txt";

    variable current_read_line : line;
    variable hex_reader : std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
  begin
      if not ENDFILE(input) then 
        if rising_edge(clk) then
          RW <= '1';
          readline(input, current_read_line);
          hread(current_read_line, hex_reader);

          data_in <= hex_reader;
          address <= std_logic_vector(to_unsigned(cnt, address_width));
          
          cnt <= cnt + 1;
        end if;
      else
        wait_cnt <= wait_cnt + 1;
        if wait_cnt = 1 then
          RW <= '0';
        elsif wait_cnt = 3 then
           
          vld_collect_header <= '1';
          key_in <= "1100100000000000";
        elsif wait_cnt = 4 then
          -- vld <= '0';
        elsif wait_cnt = 5 then
          vld_collect_header <= '0';
          -- assert codeword = "0000000000000001"
          --   report "codeword is not correct"
          --   severity note;
        elsif wait_cnt = 30 then
          vld_collect_header <= '1';
          key_in <= "1001000000000000";
        elsif wait_cnt = 31 then
        elsif wait_cnt = 32 then
          vld_collect_header <= '0';

        else
          cnt <= 0;
         
          
        end if;
      end if;
  end process;

end;
