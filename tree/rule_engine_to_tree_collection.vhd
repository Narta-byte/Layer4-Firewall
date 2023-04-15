library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


entity rule_engine_and_tree_collection is
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
end;

architecture rtl of rule_engine_and_tree_collection is

  component rule_engine
    generic (
      address_width : integer;
      codeword_length : integer;
      tree_depth : integer
    );
      port (
      cmd_in : in std_logic_vector(4 downto 0);
      data_in : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      data_out : out std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      RW : out std_logic;
      sel : out std_logic_vector(2 downto 0);
      address : out std_logic_vector(address_width - 1 downto 0);
      rdy : out std_logic;
      vld : in std_logic;
      clk : in std_logic;
      reset : in std_logic
    );
  end component;

  component mux5
    generic (
      address_width : integer;
      codeword_length : integer
    );
      port (
      c0 : out std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      c1 : out std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      c2 : out std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      c3 : out std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      c4 : out std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      r0 : out std_logic;
      r1 : out std_logic;
      r2 : out std_logic;
      r3 : out std_logic;
      r4 : out std_logic;
      a0 : out std_logic_vector(address_width - 1 downto 0);
      a1 : out std_logic_vector(address_width - 1 downto 0);
      a2 : out std_logic_vector(address_width - 1 downto 0);
      a3 : out std_logic_vector(address_width - 1 downto 0);
      a4 : out std_logic_vector(address_width - 1 downto 0);
      sel : in std_logic_vector(2 downto 0);
      address_in : in std_logic_vector(address_width - 1 downto 0);
      r_in : in std_logic;
      b : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0)
    );
  end component;
  
  component tree_collection
    generic (
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
      tree0_key_in : in std_logic_vector(tree0_key_length - 1 downto 0);
      tree0_data_in : in std_logic_vector(codeword_length + tree0_address_width * 2 - 1 downto 0);
      tree0_address : in std_logic_vector(tree0_address_width - 1 downto 0);
      tree0_RW : in std_logic;
      tree0_rdy_collect_header : out std_logic;
      tree0_vld_collect_header : in std_logic;
      tree1_key_in : in std_logic_vector(tree1_key_length - 1 downto 0);
      tree1_data_in : in std_logic_vector(codeword_length + tree1_address_width * 2 - 1 downto 0);
      tree1_address : in std_logic_vector(tree1_address_width - 1 downto 0);
      tree1_RW : in std_logic;
      tree1_rdy_collect_header : out std_logic;
      tree1_vld_collect_header : in std_logic;
      tree2_key_in : in std_logic_vector(tree2_key_length - 1 downto 0);
      tree2_data_in : in std_logic_vector(codeword_length + tree2_address_width * 2 - 1 downto 0);
      tree2_address : in std_logic_vector(tree2_address_width - 1 downto 0);
      tree2_RW : in std_logic;
      tree2_rdy_collect_header : out std_logic;
      tree2_vld_collect_header : in std_logic;
      tree3_key_in : in std_logic_vector(tree3_key_length - 1 downto 0);
      tree3_data_in : in std_logic_vector(codeword_length + tree3_address_width * 2 - 1 downto 0);
      tree3_address : in std_logic_vector(tree3_address_width - 1 downto 0);
      tree3_RW : in std_logic;
      tree3_rdy_collect_header : out std_logic;
      tree3_vld_collect_header : in std_logic;
      tree4_key_in : in std_logic_vector(tree4_key_length - 1 downto 0);
      tree4_data_in : in std_logic_vector(codeword_length + tree3_address_width * 2 - 1 downto 0);
      tree4_address : in std_logic_vector(tree4_address_width - 1 downto 0);
      tree4_RW : in std_logic;
      tree4_rdy_collect_header : out std_logic;
      tree4_vld_collect_header : in std_logic;
      clk : in std_logic;
      reset : in std_logic
    );
  end component;
  
  -- Wires
    signal wire_mux : std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
    signal RW_in : std_logic;
    signal sel : std_logic_vector(2 downto 0);

    signal wire_address : std_logic_vector(address_width - 1 downto 0);
    signal data_out : std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);

    signal tree0 : std_logic_vector(codeword_length+address_width * 2 - 1 downto 0);
    signal tree1 : std_logic_vector(codeword_length+address_width * 2 - 1 downto 0);
    signal tree2 : std_logic_vector(codeword_length+address_width * 2 - 1 downto 0);
    signal tree3 : std_logic_vector(codeword_length+address_width * 2 - 1 downto 0);
    signal tree4 : std_logic_vector(codeword_length+address_width * 2 - 1 downto 0);

    signal RW0:  std_logic;
    signal RW1:  std_logic;
    signal RW2:  std_logic;
    signal RW3:  std_logic;
    signal RW4:  std_logic;

    signal address0 : std_logic_vector(address_width - 1 downto 0);
    signal address1 : std_logic_vector(address_width - 1 downto 0);
    signal address2 : std_logic_vector(address_width - 1 downto 0);
    signal address3 : std_logic_vector(address_width - 1 downto 0);
    signal address4 : std_logic_vector(address_width - 1 downto 0);


begin

  rule_engine_inst : rule_engine
    generic map (
      address_width => address_width,
      codeword_length => codeword_length,
      tree_depth => tree_depth
    )
    port map (
      cmd_in => cmd_in,
      data_in => data_in,
      data_out => data_out,
      RW => RW_in,
      sel => sel,
      address => wire_address,
      rdy => rdy,
      vld => vld,
      clk => clk,
      reset => reset
    );

  mux5_inst : mux5
    generic map (
      address_width => address_width,
      codeword_length => codeword_length
    )
    port map (
      c0 => tree0,
      c1 => tree1,
      c2 => tree2,
      c3 => tree3,
      c4 => tree4,
      r0 => RW0,
      r1 => RW1,
      r2 => RW2,
      r3 => RW3,
      r4 => RW4,
      a0 => address0,
      a1 => address1,
      a2 => address2,
      a3 => address3,
      a4 => address4,
      sel => sel,
      address_in => wire_address,
      r_in => RW_in,
      b => data_out
  );


  tree_collection_inst : tree_collection
    generic map (
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
      tree0_key_in => tree0_key_in,
      tree0_data_in => tree0,
      tree0_address => address0,
      tree0_RW => RW0,
      tree0_rdy_collect_header => tree0_rdy_collect_header,
      tree0_vld_collect_header => tree0_vld_collect_header,
      tree1_key_in => tree1_key_in,
      tree1_data_in => tree1,
      tree1_address => address1,
      tree1_RW => RW1,
      tree1_rdy_collect_header => tree1_rdy_collect_header,
      tree1_vld_collect_header => tree1_vld_collect_header,
      tree2_key_in => tree2_key_in,
      tree2_data_in => tree2,
      tree2_address => address2,
      tree2_RW => RW2,
      tree2_rdy_collect_header => tree2_rdy_collect_header,
      tree2_vld_collect_header => tree2_vld_collect_header,
      tree3_key_in => tree3_key_in,
      tree3_data_in => tree3,
      tree3_address => address3,
      tree3_RW => RW3,
      tree3_rdy_collect_header => tree3_rdy_collect_header,
      tree3_vld_collect_header => tree3_vld_collect_header,
      tree4_key_in => tree4_key_in,
      tree4_data_in => tree4,
      tree4_address => address4,
      tree4_RW => RW4,
      tree4_rdy_collect_header => tree4_rdy_collect_header,
      tree4_vld_collect_header => tree4_vld_collect_header,
      clk => clk,
      reset => reset
    );
  

end;




  




