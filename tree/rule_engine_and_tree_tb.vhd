library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use IEEE.std_logic_textio.all;
use std.textio.all;

entity rule_engine_and_tree_collection_tb is
end;

architecture bench of rule_engine_and_tree_collection_tb is

  component rule_engine_and_tree_collection
    generic (
      address_width : integer;
      codeword_length : integer;
      tree_depth : integer;
      tree0_key_length : integer;
      tree0_address_width : integer;
      tree1_key_length : integer;
      tree1_address_width : integer;
      tree2_key_length : integer;
      tree2_address_width : integer;
      tree3_key_length : integer;
      tree3_address_width : integer;
      tree4_key_length : integer;
      tree4_address_width : integer
    );
      port (
      cmd_in : in std_logic_vector(4 downto 0);
      data_in : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      rdy : out std_logic;
      vld : in std_logic;
      tree0_key_in : in std_logic_vector(tree0_key_length - 1 downto 0);
      tree1_key_in : in std_logic_vector(tree1_key_length - 1 downto 0);
      tree2_key_in : in std_logic_vector(tree2_key_length - 1 downto 0);
      tree3_key_in : in std_logic_vector(tree3_key_length - 1 downto 0);
      tree4_key_in : in std_logic_vector(tree4_key_length - 1 downto 0);
      tree0_rdy_collect_header : out std_logic;
      tree0_vld_collect_header : in std_logic;
      tree1_rdy_collect_header : out std_logic;
      tree1_vld_collect_header : in std_logic;
      tree2_rdy_collect_header : out std_logic;
      tree2_vld_collect_header : in std_logic;
      tree3_rdy_collect_header : out std_logic;
      tree3_vld_collect_header : in std_logic;
      tree4_rdy_collect_header : out std_logic;
      tree4_vld_collect_header : in std_logic;
      clk : in std_logic;
      reset : in std_logic
    );
  end component;

  -- Clock period
  constant clk_period : time := 5 ns;
  -- Generics
  constant address_width : integer := 8;
  constant codeword_length : integer := 16;
  constant tree_depth : integer := 16;
  constant tree0_key_length : integer := 16;
  constant tree0_address_width : integer := 8;
  constant tree1_key_length : integer := 16;
  constant tree1_address_width : integer := 8;
  constant tree2_key_length : integer := 16;
  constant tree2_address_width : integer := 8;
  constant tree3_key_length : integer := 16;
  constant tree3_address_width : integer := 8;
  constant tree4_key_length : integer := 16;
  constant tree4_address_width : integer := 8;

  -- Ports
  signal cmd_in : std_logic_vector(4 downto 0);
  signal data_in : std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
  signal rdy : std_logic;
  signal vld : std_logic;
  signal tree0_key_in : std_logic_vector(tree0_key_length - 1 downto 0);
  signal tree1_key_in : std_logic_vector(tree1_key_length - 1 downto 0);
  signal tree2_key_in : std_logic_vector(tree2_key_length - 1 downto 0);
  signal tree3_key_in : std_logic_vector(tree3_key_length - 1 downto 0);
  signal tree4_key_in : std_logic_vector(tree4_key_length - 1 downto 0);
  signal tree0_rdy_collect_header : std_logic;
  signal tree0_vld_collect_header : std_logic;
  signal tree1_rdy_collect_header : std_logic;
  signal tree1_vld_collect_header : std_logic;
  signal tree2_rdy_collect_header : std_logic;
  signal tree2_vld_collect_header : std_logic;
  signal tree3_rdy_collect_header : std_logic;
  signal tree3_vld_collect_header : std_logic;
  signal tree4_rdy_collect_header : std_logic;
  signal tree4_vld_collect_header : std_logic;
  signal clk : std_logic;
  signal reset : std_logic;

  signal cnt, wait_cnt : integer := 0;
  
begin

  rule_engine_and_tree_collection_inst : rule_engine_and_tree_collection
    generic map (
      address_width => address_width,
      codeword_length => codeword_length,
      tree_depth => tree_depth,
      tree0_key_length => tree0_key_length,
      tree0_address_width => tree0_address_width,
      tree1_key_length => tree1_key_length,
      tree1_address_width => tree1_address_width,
      tree2_key_length => tree2_key_length,
      tree2_address_width => tree2_address_width,
      tree3_key_length => tree3_key_length,
      tree3_address_width => tree3_address_width,
      tree4_key_length => tree4_key_length,
      tree4_address_width => tree4_address_width
    )
    port map (
      cmd_in => cmd_in,
      data_in => data_in,
      rdy => rdy,
      vld => vld,
      tree0_key_in => tree0_key_in,
      tree1_key_in => tree1_key_in,
      tree2_key_in => tree2_key_in,
      tree3_key_in => tree3_key_in,
      tree4_key_in => tree4_key_in,
      tree0_rdy_collect_header => tree0_rdy_collect_header,
      tree0_vld_collect_header => tree0_vld_collect_header,
      tree1_rdy_collect_header => tree1_rdy_collect_header,
      tree1_vld_collect_header => tree1_vld_collect_header,
      tree2_rdy_collect_header => tree2_rdy_collect_header,
      tree2_vld_collect_header => tree2_vld_collect_header,
      tree3_rdy_collect_header => tree3_rdy_collect_header,
      tree3_vld_collect_header => tree3_vld_collect_header,
      tree4_rdy_collect_header => tree4_rdy_collect_header,
      tree4_vld_collect_header => tree4_vld_collect_header,
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
        --   RW <= '1';
          vld <= '1';
          cmd_in <= "00001";

          readline(input, current_read_line);
          hread(current_read_line, hex_reader);

          data_in <= hex_reader;
        --   address <= std_logic_vector(to_unsigned(cnt, address_width));
          
          cnt <= cnt + 1;
        end if;
      else
        vld <= '0';
        cmd_in <= "00000";
        wait_cnt <= wait_cnt + 1;
        -- if wait_cnt = 1 then
        --   RW <= '0';
        -- elsif wait_cnt = 3 then
           
        --   vld_collect_header <= '1';
        --   key_in <= "1100100000000000";
        -- elsif wait_cnt = 4 then
        --   -- vld <= '0';
        -- elsif wait_cnt = 5 then
        --   vld_collect_header <= '0';
        --   -- assert codeword = "0000000000000001"
        --   --   report "codeword is not correct"
        --   --   severity note;
        -- elsif wait_cnt = 30 then
        --   vld_collect_header <= '1';
        --   key_in <= "1001000000000000";
        -- elsif wait_cnt = 31 then
        -- elsif wait_cnt = 32 then
        --   vld_collect_header <= '0';

        -- else
        --   cnt <= 0;
         
          
        -- end if;
      end if;
  end process;

end;
