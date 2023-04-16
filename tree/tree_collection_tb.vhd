library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;
use ieee.std_logic_arith.all;
use ieee.math_real.all;
use work.my_types_pkg.all;


entity tree_collection_tb is
end;

architecture bench of tree_collection_tb is

  component tree_collection
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
      largest_codeword : integer
    );
      port (
      key_in : in std_logic_vector(total_key_in_length - 1 downto 0);
      codeword_in : in std_logic_vector(largest_codeword - 1 downto 0);
      zero_pointer : in std_logic_vector(largest_address_width - 1 downto 0);
      one_pointer : in std_logic_vector(largest_address_width - 1 downto 0);
      address : in std_logic_vector(largest_address_width - 1 downto 0);
      RW : in std_logic_vector(number_of_trees - 1 downto 0);
      rdy_collect_header : out std_logic_vector(number_of_trees - 1 downto 0);
      vld_collect_header : in std_logic_vector(number_of_trees -1 downto 0);
      clk : in std_logic;
      reset : in std_logic
    );
  end component;

  -- Clock period
  constant clk_period : time := 5 ns;
  -- Generics
  constant number_of_trees : integer := 5;
  constant tree_depth : integer := 16;
  constant address_width : tree_array := (8,8,8,16,8);
  constant total_address_width : integer := 48;
  constant address_width_cumsum : tree_array := (0,8,16,24,40,48);
  constant largest_address_width : integer := 16;
  constant key_in_lengths : tree_array := (16,16,16,32,16);
  constant total_key_in_length : integer := 96;
  constant tree_cumsum : tree_array := (0,16,32,48,80,96);
  constant codeword_length : tree_array := (16,16,16,16,16);
  constant largest_codeword : integer := 16;



  -- Ports
  signal key_in : std_logic_vector(total_key_in_length - 1 downto 0);
  signal codeword_in : std_logic_vector(largest_codeword - 1 downto 0);
  signal zero_pointer : std_logic_vector(largest_address_width - 1 downto 0);
  signal one_pointer : std_logic_vector(largest_address_width - 1 downto 0);
  signal address : std_logic_vector(largest_address_width - 1 downto 0);
  signal RW : std_logic_vector(number_of_trees - 1 downto 0);
  signal rdy_collect_header : std_logic_vector(number_of_trees - 1 downto 0);
  signal vld_collect_header : std_logic_vector(number_of_trees -1 downto 0);
  signal clk : std_logic;
  signal reset : std_logic;
  
  -- From vhdlwiz https://vhdlwhiz.com/random-numbers/

  
  impure function rand_slv(len : integer; seed1 : integer; seed2 : integer) return std_logic_vector is
    -- variable seed1, seed2 : integer := 999;
    variable r : real;
    variable slv : std_logic_vector(len - 1 downto 0);
  begin
    for i in slv'range loop
      uniform(seed1, seed2, r);
      -- slv(i) := '1' when r > 0.5 else '0';
      if r > 0.5 then
        slv(i) := '1';
      else
        slv(i) := '0';
      end if;

    end loop;
    return slv;
  end function;
  -- From vhdlwiz https://vhdlwhiz.com/random-numbers/

begin

  tree_collection_inst : tree_collection
    generic map (
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
      largest_codeword => largest_codeword
    )
    port map (
      key_in => key_in,
      codeword_in => codeword_in,
      zero_pointer => zero_pointer,
      one_pointer => one_pointer,
      address => address,
      RW => RW,
      rdy_collect_header => rdy_collect_header,
      vld_collect_header => vld_collect_header,
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
  begin
    if rising_edge(clk) then
      -- Random data_in
      -- data_in <= rand_slv(total_key_in_length - 1 +                               --key_in
      --            (codeword_length + address_width * 2) * number_of_trees + --data_in
      --            (address_width) * number_of_trees +                       -- address
      --            number_of_trees +                                         -- RW (select)
      --            (-1));
      key_in <= rand_slv(total_key_in_length, 0, 1);
      -- data_in <= rand_slv(total_address_width - 1);
      codeword_in <= rand_slv(largest_codeword, 2, 3);
      zero_pointer <= rand_slv(largest_address_width, 4, 5);
      one_pointer <= rand_slv(largest_address_width, 6, 7);

      address <= rand_slv(largest_address_width, 8, 9);
      RW <= rand_slv(number_of_trees, 10, 11);
      rdy_collect_header <= rand_slv(number_of_trees, 12, 13);
      vld_collect_header <= (others => '1');
      
    end if;
  end process;

end;

