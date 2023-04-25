library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;
use ieee.math_real.all;
use work.my_types_pkg.all;



entity system_blueprint is
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
    codeword_in : in std_logic_vector(largest_codeword - 1 downto 0);
    zero_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);
    one_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);


    rdy_driver : out std_logic;
    vld_driver : in std_logic;

    rdy_collect_header : out std_logic_vector(number_of_trees - 1 downto 0);
    vld_collect_header : in std_logic_vector(number_of_trees -1 downto 0);

    cuckoo_key_in : in std_logic_vector(codeword_sum - 1 downto 0);
    
    -- rdy_cuckoo_hash : in std_logic;
    -- vld_cuckoo_hash : out std_logic;

    clk : in std_logic;
    reset : in std_logic
  );
end;

architecture rtl of system_blueprint is

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
      codeword_out : out std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
      cuckoo_codeword : out std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
      rdy_cuckoo_hash : in std_logic;
      vld_cuckoo_hash : out std_logic;
      clk : in std_logic;
      reset : in std_logic
    );
  end component;
  
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
      largest_codeword : integer;
      codeword_sum : integer
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
      cuckoo_select : out std_logic;
      cuckoo_cmd : out std_logic_vector(1 downto 0);
      cuckoo_key_out : out std_logic_vector(codeword_sum - 1 downto 0);
      cuckoo_key_in : in std_logic_vector(codeword_sum - 1 downto 0);
      cuckoo_rdy : in std_logic;
      cuckoo_vld : out std_logic;
      cuckoo_set_rule : out std_logic;
      clk : in std_logic;
      reset : in std_logic
    );
  end component;
  component Cuckoo_Hashing
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
      clk : in std_logic;
      reset : in std_logic;
      set_rule : in std_logic;
      cmd_in : in std_logic_vector(1 downto 0);
      key_in : in std_logic_vector(codeword_sum - 1 downto 0);
      header_data : in std_logic_vector(codeword_sum - 1 downto 0);
      vld_hdr : in std_logic;
      rdy_hash : out std_logic;
      vld_firewall_hash : in std_logic;
      rdy_firewall_hash : out std_logic;
      acc_deny_hash : out std_logic;
      vld_ad_hash : out std_logic;
      rdy_ad_hash : in std_logic
    );
  end component;


  signal set_rule : std_logic;
  signal header_data : std_logic_vector(codeword_sum - 1 downto 0);
  signal vld_hdr : std_logic;
  signal rdy_hash : std_logic;
  signal vld_firewall_hash : std_logic;
  signal rdy_firewall_hash : std_logic;
  signal acc_deny_hash : std_logic;
  signal vld_ad_hash : std_logic;
  signal rdy_ad_hash : std_logic;

  signal address : std_logic_vector(largest_address_width - 1 downto 0);
  signal RW : std_logic_vector(number_of_trees - 1 downto 0);

  signal codeword_out : std_logic_vector(largest_codeword - 1 downto 0);
  signal zero_pointer_out : std_logic_vector(largest_address_width - 1 downto 0);
  signal one_pointer_out : std_logic_vector(largest_address_width - 1 downto 0);

  signal codeword_to_concat : std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);

  signal cuckoo_codeword : std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
  signal cuckoo_select : std_logic;
  signal cuckoo_cmd : std_logic_vector(1 downto 0);
  signal cuckoo_key_out: std_logic_vector(codeword_sum - 1 downto 0);
  signal rule_cuckoo_rdy : std_logic;
  signal rule_cuckoo_vld : std_logic;


  signal trees_to_cuckoo_hash_vld : std_logic;
  signal trees_to_cuckoo_hash_rdy : std_logic;

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
      largest_codeword => largest_codeword,
      codeword_sum => codeword_sum
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
      cuckoo_select => cuckoo_select,
      cuckoo_cmd => cuckoo_cmd,
      cuckoo_key_out => cuckoo_key_out,
      cuckoo_key_in => cuckoo_key_in,
      cuckoo_rdy => rule_cuckoo_rdy,
      cuckoo_vld => rule_cuckoo_vld,
      cuckoo_set_rule => set_rule,
      clk => clk,
      reset => reset
    );
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
    codeword_in => codeword_out,
    zero_pointer => zero_pointer_out,
    one_pointer => one_pointer_out,
    address => address,
    RW => RW,
    rdy_collect_header => rdy_collect_header,
    vld_collect_header => vld_collect_header,
    codeword_out => codeword_to_concat,
    cuckoo_codeword => cuckoo_codeword,
    rdy_cuckoo_hash => trees_to_cuckoo_hash_rdy,
    vld_cuckoo_hash => trees_to_cuckoo_hash_vld,
    clk => clk,
    reset => reset
  );
  Cuckoo_Hashing_inst : Cuckoo_Hashing
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
      largest_codeword => largest_codeword,
      codeword_sum => codeword_sum
    )
    port map (
      clk => clk,
      reset => reset,
      set_rule => set_rule,
      cmd_in => cuckoo_cmd,
      key_in => cuckoo_key_out,
      header_data => codeword_to_concat, -- change the name to something like codeword out
      vld_hdr => trees_to_cuckoo_hash_vld, 
      rdy_hash => trees_to_cuckoo_hash_rdy, --rdy_hash,
      vld_firewall_hash => rule_cuckoo_vld,
      rdy_firewall_hash => rule_cuckoo_rdy,
      acc_deny_hash => acc_deny_hash,
      vld_ad_hash => vld_ad_hash,
      rdy_ad_hash => rdy_ad_hash
    );




end;


