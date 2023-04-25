library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;
use ieee.math_real.all;
use work.my_types_pkg.all;




entity rule_engine_tb is
end;

architecture bench of rule_engine_tb is
   
  component rule_engine
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
      cmd_in : in std_logic_vector(4 downto 0);
      codeword_in : in std_logic_vector(largest_codeword - 1 downto 0);
      zero_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);
      one_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);
      codeword_out : out std_logic_vector(largest_codeword - 1 downto 0);
      zero_pointer_out : out std_logic_vector(largest_address_width - 1 downto 0);
      one_pointer_out : out std_logic_vector(largest_address_width - 1 downto 0);
      RW : out std_logic_vector(number_of_trees - 1 downto 0);
      address : out std_logic_vector(largest_address_width - 1 downto 0);
      rdy_driver : out std_logic;
      vld_driver : in std_logic;
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
  signal cmd_in : std_logic_vector(4 downto 0);
  signal codeword_in : std_logic_vector(largest_codeword - 1 downto 0);
  signal zero_pointer_in : std_logic_vector(largest_address_width - 1 downto 0);
  signal one_pointer_in : std_logic_vector(largest_address_width - 1 downto 0);
  signal codeword_out : std_logic_vector(largest_codeword - 1 downto 0);
  signal zero_pointer_out : std_logic_vector(largest_address_width - 1 downto 0);
  signal one_pointer_out : std_logic_vector(largest_address_width - 1 downto 0);
  signal RW : std_logic_vector(number_of_trees - 1 downto 0);
  signal address : std_logic_vector(largest_address_width - 1 downto 0);
  signal rdy_driver : std_logic;
  signal vld_driver : std_logic;
  signal clk : std_logic;
  signal reset : std_logic;

  signal i : integer:=0;

   -- From vhdlwiz https://vhdlwhiz.com/random-numbers/

     
   impure function rand_slv(len : integer;s1 : integer;s2 : integer) return std_logic_vector is
    variable seed1, seed2 : integer := 999;
    variable r : real;
    variable slv : std_logic_vector(len - 1 downto 0);
begin
    seed1 := s1;
    seed2 := s2;
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

  rule_engine_inst : rule_engine
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
      cmd_in => cmd_in,
      codeword_in => codeword_in,
      zero_pointer_in => zero_pointer_in,
      one_pointer_in => one_pointer_in,
      codeword_out => codeword_out,
      zero_pointer_out => zero_pointer_out,
      one_pointer_out => one_pointer_out,
      RW => RW,
      address => address,
      rdy_driver => rdy_driver,
      vld_driver => vld_driver,
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
    if rising_edge(clk) and rdy_driver = '1' then
        i <= i + 1;
        if i = 1 then
            cmd_in <= "00001";
            codeword_in <= (largest_codeword -1  downto 0 => '0');
            zero_pointer_in <= (largest_address_width-1 downto 0 => '0') ;
            one_pointer_in <= (largest_address_width-1 downto 0 => '0');
            vld_driver <= '1';
        elsif i >= 2 then

            if i mod 19 = 0 then
                codeword_in <= "0000000000000000";
                zero_pointer_in <= "0000000000000000";
                one_pointer_in <= "0000000000000000";
            else
                codeword_in <=     rand_slv(largest_codeword,i,i+1);
                zero_pointer_in <= rand_slv(largest_address_width,i+2,i+3);
                one_pointer_in <=  rand_slv(largest_address_width,i+4,i+5);
            end if;
        end if;
        
    end if;
  end process;



end;
