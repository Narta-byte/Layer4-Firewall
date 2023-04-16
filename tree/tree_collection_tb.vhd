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
      address_width : integer;
      tree_depth : integer;
      tree_atributes : tree_array;
      total_tree_attributes : integer;
      tree_cumsum : tree_array;
      codeword_length : integer
    );
      port (
      data_in : in std_logic_vector(
            total_tree_attributes - 1 +                               --key_in
            (codeword_length + address_width * 2) * number_of_trees + --data_in
            (address_width) * number_of_trees +                       -- address
            number_of_trees +                                         -- RW (select)
            (-1)                                               
        downto 0);
      data_out : out std_logic_vector(
            number_of_trees -- rdy_collect_header
        downto 0);
      vld_collect_header : in std_logic_vector(number_of_trees -1 downto 0);
      clk : in std_logic;
      reset : in std_logic
    );
  end component;

  -- Clock period
  constant clk_period : time := 5 ns;
  -- Generics
  constant number_of_trees : integer := 5;
  constant address_width : integer := 8;
  constant tree_depth : integer := 16;
  constant tree_atributes : tree_array := (16,16,16,16,32);
  constant total_tree_attributes : integer := 96;
  constant tree_cumsum : tree_array := (16,32,48,64,96);
  constant codeword_length : integer := 16;

  -- Ports
  signal data_in : std_logic_vector(
            total_tree_attributes - 1 +                               --key_in
            (codeword_length + address_width * 2) * number_of_trees + --data_in
            (address_width) * number_of_trees +                       -- address
            number_of_trees +                                         -- RW (select)
            (-1)                                               
        downto 0);
  signal data_out : std_logic_vector(
            number_of_trees -- rdy_collect_header
        downto 0);
  signal vld_collect_header : std_logic_vector(number_of_trees -1 downto 0);
  signal clk : std_logic;
  signal reset : std_logic;
  
  -- From vhdlwiz
  -- procedure UNIFORM(variable SEED1, SEED2 : inout POSITIVE;
  -- variable X : out REAL);
  	
  
  impure function rand_slv(len : integer) return std_logic_vector is
    variable seed1, seed2 : integer := 999;
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
  -- From vhdlwiz

begin

  tree_collection_inst : tree_collection
    generic map (
      number_of_trees => number_of_trees,
      address_width => address_width,
      tree_depth => tree_depth,
      tree_atributes => tree_atributes,
      total_tree_attributes => total_tree_attributes,
      tree_cumsum => tree_cumsum,
      codeword_length => codeword_length
    )
    port map (
      data_in => data_in,
      data_out => data_out,
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
      data_in <= rand_slv(total_tree_attributes - 1 +                               --key_in
                 (codeword_length + address_width * 2) * number_of_trees + --data_in
                 (address_width) * number_of_trees +                       -- address
                 number_of_trees +                                         -- RW (select)
                 (-1));

      vld_collect_header <= (others => '1');
      
    end if;
  end process;

end;
