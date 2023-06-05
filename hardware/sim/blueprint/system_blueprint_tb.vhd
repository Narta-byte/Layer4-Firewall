library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use IEEE.std_logic_textio.all;
use std.textio.all;
use work.my_types_pkg.all;
entity system_blueprint_tb is
end;

architecture bench of system_blueprint_tb is

  component system_blueprint
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
      cmd_in : in std_logic_vector(4 downto 0);
      key_in : in std_logic_vector(total_key_in_length - 1 downto 0);
      codeword_in : in std_logic_vector(largest_codeword  - 1 downto 0);
      zero_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);
      one_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);
      rdy_driver : out std_logic;
      vld_driver : in std_logic;
      rdy_collect_header : out std_logic_vector(number_of_trees - 1 downto 0);
      vld_collect_header : in std_logic_vector(number_of_trees - 1 downto 0);
      cuckoo_key_in : in std_logic_vector(codeword_sum - 1 downto 0);
      -- rdy_cuckoo_hash : in std_logic;
      -- vld_cuckoo_hash : out std_logic;
      SoP : in std_logic;
      Eop : in std_logic;
      CH_vld : in std_logic;
      packet_in : in std_logic_vector(10 downto 0);

      clk : in std_logic;
      reset : in std_logic
    );
  end component;

  -- Clock period
  constant clk_period : time := 5 ns;
  -- Generics
  -- constant number_of_trees : integer := 5;
  -- constant tree_depth : integer := 16;
  -- constant address_width : tree_array := (8,8,8,16,8);
  -- constant total_address_width : integer := 48;
  -- constant address_width_cumsum : tree_array := (0,8,16,24,40,48);
  -- constant largest_address_width : integer := 16;
  -- constant key_in_lengths : tree_array := (16,16,16,32,16);
  -- constant total_key_in_length : integer := 96;
  -- constant tree_cumsum : tree_array := (0,16,32,48,80,96);
  -- constant codeword_length : tree_array := (16,16,16,16,16);
  -- constant largest_codeword : integer := 16;
  -- constant codeword_sum : integer := 80;
  constant number_of_trees : integer := 5;
  constant tree_depth : integer := 16;
  constant address_width : tree_array := (16, 16, 16, 16, 16);
  constant total_address_width : integer := 80;
  constant address_width_cumsum : tree_array := (0, 16, 32, 48, 64, 80);
  constant largest_address_width : integer := 16;
  constant key_in_lengths : tree_array := (8, 16, 16, 32, 32);
  constant total_key_in_length : integer := 104;
  constant tree_cumsum : tree_array := (0, 8, 24, 40, 72, 104);
  constant codeword_length : tree_array := (32, 32, 32, 32, 32);
  constant largest_codeword : integer := 32;
  constant codeword_sum : integer := 160;

  -- Ports
  signal cmd_in : std_logic_vector(4 downto 0);
  signal key_in : std_logic_vector(total_key_in_length - 1 downto 0);
  signal codeword_in : std_logic_vector(largest_codeword - 1 downto 0);
  signal zero_pointer_in : std_logic_vector(largest_address_width - 1 downto 0);
  signal one_pointer_in : std_logic_vector(largest_address_width - 1 downto 0);
  signal rdy_driver : std_logic;
  signal vld_driver : std_logic;
  signal rdy_collect_header : std_logic_vector(number_of_trees - 1 downto 0);
  signal vld_collect_header : std_logic_vector(number_of_trees - 1 downto 0);
  signal cuckoo_codeword : std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
  signal cuckoo_key_in : std_logic_vector(codeword_sum+8- 1 downto 0);
  signal rdy_cuckoo_hash : std_logic;
  signal vld_cuckoo_hash : std_logic;
  signal clk : std_logic;
  signal reset : std_logic;
  signal i, j, cnt, wait_cnt, bytenm : integer := 0;
  signal enable : std_logic := '0';
  signal packet_data : std_logic_vector(7 downto 0);
  signal packet_in : std_logic_vector (10 downto 0);

  signal packet_start : std_logic := '0';
  signal CH_vld : std_logic;
  signal SoP : std_logic;
  signal EoP : std_logic;
  signal filedone : std_logic:='0';

begin

  system_blueprint_inst : system_blueprint
  generic map(
    number_of_trees => number_of_trees,
    tree_depth => tree_depth,
    address_width => address_width,
    total_address_width => total_address_width,
    address_width_cumsum => address_width_cumsum,
    largest_address_width => largest_address_width,
    key_in_lengths => key_in_lengths,
    total_key_in_length => total_key_in_length,
    tree_cumsum => tree_cumsum,
    codeword_length => codeword_length,
    largest_codeword => largest_codeword,
    codeword_sum => codeword_sum
  )
  port map(
    cmd_in => cmd_in,
    key_in => key_in,
    codeword_in => codeword_in,
    zero_pointer_in => zero_pointer_in,
    one_pointer_in => one_pointer_in,
    rdy_driver => rdy_driver,
    vld_driver => vld_driver,
    rdy_collect_header => rdy_collect_header,
    vld_collect_header => vld_collect_header,
    cuckoo_key_in => cuckoo_key_in,
    -- rdy_cuckoo_hash => rdy_cuckoo_hash,
    -- vld_cuckoo_hash => vld_cuckoo_hash,
    SoP => SoP,
    Eop => Eop,
    CH_vld => CH_vld,
    packet_in => packet_in,

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
  process (clk)
    file input0 : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/hardware/sim/blueprint/tree_data_tb.txt";
    variable current_read_line0 : line;
    variable hex_reader0 : std_logic_vector(largest_codeword + largest_address_width * 2 - 1 downto 0);

    -- file input1 : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/hardware/sim/blueprint/cuckoo_hash/large_input_file_increment.txt";
    file input1 : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/hardware/sim/blueprint/cuckoo_hash/cuckoo_sram_data.txt";
    variable current_read_line1 : line;
    variable hex_reader1 : std_logic_vector(codeword_sum + 8 - 1 downto 0);


    file packet_file : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/hardware/sim/blueprint/collect_header/input_packets.txt";
    variable current_read_line2 : line;
    variable current_read_field	: std_logic_vector (7 downto 0);
    variable current_write_line : std_logic;
  begin
    if rising_edge(clk) and rdy_driver = '1' then
      i <= i + 1;
      if i >= 2 then
        if not ENDFILE(input0) and rdy_driver = '1' then
          vld_driver <= '1';
          cmd_in <= "00001";

          readline(input0, current_read_line0);
          hread(current_read_line0, hex_reader0);

          codeword_in <= hex_reader0(largest_codeword + largest_address_width * 2 - 1 downto largest_address_width * 2);
          zero_pointer_in <= hex_reader0(largest_address_width * 2 - 1 downto largest_address_width);
          one_pointer_in <= hex_reader0(largest_address_width - 1 downto 0);
          cnt <= cnt + 1;
        else
          vld_driver <= '0';
          wait_cnt <= wait_cnt + 1;
          if wait_cnt = 2 then
            -- vld_collect_header <= ((others => '1'));

            -- key_in <= ("1100100000000000"& 
            --            "1110000000000000"&
            --            "1000100000000000"&
            --            "11010000000000000000000000000000"&
            --            "1011000000000000");
          elsif wait_cnt = 4 then
            vld_collect_header <= ((others => '0'));
          elsif wait_cnt = 15 then
            if rdy_collect_header = "11111" then
              -- vld_collect_header <= ((others => '1'));

              -- key_in <= (
              --     "0000000000000000" &
              --     "1000000000000000" &
              --     "1010000000000000" &
              --     "11100000000000000000000000000000" &
              --     "1010000000000000" );
            end if;
          elsif wait_cnt = 17 then
            vld_collect_header <= ((others => '0'));
            enable <= '1';
            -- i <= 0;
            -- wait_cnt <= 0;

          elsif wait_cnt >= 19 then
            j <= j + 1;
            if j > 2 then
              if not ENDFILE(input1) and rdy_driver = '1' then
                readline(input1, current_read_line1);
                read(current_read_line1, hex_reader1);
                cuckoo_key_in <= hex_reader1;
                cmd_in <= "00010";
                vld_driver <= '1';
              else
                -- vld_cuckoo_hash <= '0';
                cmd_in <= "00000";

                vld_driver <= '0';
                if not ENDFILE(packet_file) or not filedone = '1' then 

                  packet_start <= '1';
                  bytenm <= bytenm + 1;
                  readline(packet_file, current_read_line2);
                  hread(current_read_line2, current_read_field);
                  packet_data <= current_read_field;
              
      
                  read(current_read_line2, current_write_line);
                  CH_vld <= current_write_line;
      
                  read(current_read_line2, current_write_line);
                  SoP <= current_write_line;
              
                  read(current_read_line2, current_write_line);
                  EoP <= current_write_line;
      
                  -- packet_in <= packet_data & SoP & EoP;
                  packet_in <= packet_data & CH_vld & SoP & EoP;
                else
                  filedone <= '1';
                end if;
                -- key_in <= (
                --   "11001000" &
                --   "1110000000000000" &
                --   "1000100000000000" &
                --   "11010000000000000000000000000000" &
                --   "10110000000000000000000000000000");
                -- vld_collect_header <= ((others => '1'));
                

              end if;
            end if;
          end if;
        end if;

      end if;

    end if;
  end process;
end;