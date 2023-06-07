library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;
use work.my_types_pkg.all;


entity tree_collection is
    generic (
        number_of_trees : integer := 5;
        -- address_width : integer := 8;
        tree_depth : integer := 16;

        address_width : tree_array := (8,8,8,16,8);
        total_address_width : integer := 48;
        address_width_cumsum : tree_array := (0,8,16,24,40,48);

        largest_address_width : integer := 16;

        key_in_lengths : tree_array:=(16,16,16,32,16);
        total_key_in_length : integer := 96; 

        tree_cumsum : tree_array :=  (0,16,32,48,80,96); -- ,96);
        -- total_tree_address : integer := number_of_trees * address_width ;

        codeword_length : tree_array := (16,16,16,16,16);
        largest_codeword : integer := 16;

        max_iterations : tree_array := (1,1,1,1,1);
        tree_config : tree_array    := (1,1,1,1,1)

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

        codeword_out : out std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
        cuckoo_codeword : out std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
        rdy_cuckoo_hash : in std_logic;
        vld_cuckoo_hash : out std_logic;

        clk   : in std_logic;
        reset : in std_logic
        
    );
end entity tree_collection;

architecture rtl of tree_collection is
  component tree_and_sram
    generic (
      key_length : integer;
      address_width : integer;
      codeword_length : integer;
      tree_depth : integer;
      max_iterations : integer;
      tree_config : integer
    );
      port (
      key_in : in std_logic_vector(key_length - 1 downto 0);
      codeword_in : in std_logic_vector(codeword_length - 1 downto 0);
      zero_pointer : in std_logic_vector(address_width - 1 downto 0);
      one_pointer : in std_logic_vector(address_width - 1 downto 0);
      address : in std_logic_vector(address_width - 1 downto 0);
      RW : in std_logic;
      codeword : out std_logic_vector(codeword_length - 1 downto 0);
      rdy_collect_header : out std_logic;
      vld_collect_header : in std_logic;
      rdy_codeword_concatinator : in std_logic;
      vld_codeword_concatinator : out std_logic;
      clk : in std_logic;
      reset : in std_logic
    );
  end component;
  component codeword_concatinator
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
      codeword_in : in std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
      codeword_out : out std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
      rdy_tree : out std_logic_vector(number_of_trees - 1 downto 0);
      vld_tree : in std_logic_vector(number_of_trees - 1 downto 0);
      rdy_cuckoo_hash : in std_logic;
      vld_cuckoo_hash : out std_logic;
      clk : in std_logic;
      reset : in std_logic
    );
  end component;
      constant data_in_length : integer := largest_codeword + largest_address_width * 2;
      constant total_code_word_length : integer := largest_codeword * number_of_trees;
      
      signal w_rdy_concatinator : std_logic_vector(number_of_trees - 1 downto 0) := (others => '1');
      signal w_vld_concatinator : std_logic_vector(number_of_trees - 1 downto 0);

      signal debug : std_logic_vector(15 downto 0);
      signal codeword_to_concat : std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
    begin
    
    
    
      tree_gen : for i in 0 to number_of_trees - 1 generate
        tree_and_sram_inst : tree_and_sram
          generic map (
            key_length => key_in_lengths(i),
            address_width => address_width(i),
            codeword_length => codeword_length(i),
            tree_depth => tree_depth,
            max_iterations => max_iterations(i),
            tree_config => tree_config(i)
          )
          port map (
            key_in => key_in(total_key_in_length - tree_cumsum(i) - 1 downto total_key_in_length - tree_cumsum(i + 1)),
            codeword_in => codeword_in(codeword_length(i) - 1 downto 0),
            zero_pointer => zero_pointer(address_width(i) - 1 downto 0),
            one_pointer => one_pointer(address_width(i) - 1 downto 0),
            address => address(address_width(i) - 1 downto 0),
            RW => RW(i),
            codeword => codeword_to_concat(total_code_word_length - largest_codeword * i - 1 downto total_code_word_length - largest_codeword*(i+1)),
            rdy_collect_header => rdy_collect_header(i),
            vld_collect_header => vld_collect_header(i),
            rdy_codeword_concatinator => w_rdy_concatinator(i),
            vld_codeword_concatinator => w_vld_concatinator(i),
            clk => clk,
            reset => reset
          );
    end generate;

    codeword_concatinator_inst : codeword_concatinator
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
      codeword_in => codeword_to_concat,
      codeword_out => codeword_out,
      rdy_tree => w_rdy_concatinator,
      vld_tree => w_vld_concatinator,
      rdy_cuckoo_hash => rdy_cuckoo_hash, --rdy_cuckoo_hash,
      vld_cuckoo_hash => vld_cuckoo_hash,
      clk => clk,
      reset => reset
    );
end architecture;







