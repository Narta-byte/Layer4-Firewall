library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;


entity tree_collection is
    generic (
        codeword_length : integer := 16;
        tree_depth : integer := 16;

        tree0_key_length : integer := 16;
        tree0_address_width : integer := 8;

        tree1_key_length : integer := 16;
        tree1_address_width : integer := 8;

        tree2_key_length : integer := 16;
        tree2_address_width : integer := 8;

        tree3_key_length : integer := 0;
        tree3_address_width : integer := 0;

        tree4_key_length : integer := 0;
        tree4_address_width : integer := 0
    );
    port (
        tree0_key_in : in std_logic_vector(tree0_key_length -1 downto 0);
        tree0_data_in : in std_logic_vector(codeword_length + tree0_address_width * 2 - 1 downto 0);
        tree0_address : in std_logic_vector(tree0_address_width - 1 downto 0);
        tree0_RW : in std_logic;
        tree0_rdy_collect_header : out std_logic;
        tree0_vld_collect_header : in std_logic;

        tree1_key_in : in std_logic_vector(tree1_key_length -1 downto 0);
        tree1_data_in : in std_logic_vector(codeword_length + tree1_address_width * 2 - 1 downto 0);
        tree1_address : in std_logic_vector(tree1_address_width - 1 downto 0);
        tree1_RW : in std_logic;
        tree1_rdy_collect_header : out std_logic;
        tree1_vld_collect_header : in std_logic;

        tree2_key_in : in std_logic_vector(tree2_key_length -1 downto 0);
        tree2_data_in : in std_logic_vector(codeword_length + tree2_address_width * 2 - 1 downto 0);
        tree2_address : in std_logic_vector(tree2_address_width - 1 downto 0);
        tree2_RW : in std_logic;
        tree2_rdy_collect_header : out std_logic;
        tree2_vld_collect_header : in std_logic;

        tree3_key_in : in std_logic_vector(tree3_key_length -1 downto 0);
        tree3_data_in : in std_logic_vector(codeword_length + tree3_address_width * 2 - 1 downto 0);
        tree3_address : in std_logic_vector(tree3_address_width - 1 downto 0);
        tree3_RW : in std_logic;
        tree3_rdy_collect_header : out std_logic;
        tree3_vld_collect_header : in std_logic;

        tree4_key_in : in std_logic_vector(tree4_key_length -1 downto 0);
        tree4_data_in : in std_logic_vector(codeword_length + tree3_address_width * 2 - 1 downto 0);
        tree4_address : in std_logic_vector(tree4_address_width - 1 downto 0);
        tree4_RW : in std_logic;
        tree4_rdy_collect_header : out std_logic;
        tree4_vld_collect_header : in std_logic;

        clk : in std_logic;
        reset : in std_logic

    
    );
end entity tree_collection;

architecture rtl of tree_collection is
    constant num_of_codewords : integer := 3;
    signal final_codeword : std_logic_vector(codeword_length * num_of_codewords - 1 downto 0 ) := (others => '0') ;
    signal rdy_cuckoo_hash, vld_cuckoo_hash : std_logic := '0';
    
    
    
    signal wire0_codeword : std_logic_vector(codeword_length - 1 downto 0);
    signal wire1_codeword : std_logic_vector(codeword_length - 1 downto 0);
    signal wire2_codeword : std_logic_vector(codeword_length - 1 downto 0);
    signal wire3_codeword : std_logic_vector(codeword_length - 1 downto 0);
    signal wire4_codeword : std_logic_vector(codeword_length - 1 downto 0);

    
    signal wire0_rdy : std_logic;
    signal wire0_vld : std_logic;

    signal wire1_rdy : std_logic;
    signal wire1_vld : std_logic;

    signal wire2_rdy : std_logic;
    signal wire2_vld : std_logic;

    signal wire3_rdy : std_logic;
    signal wire3_vld : std_logic;

    signal wire4_rdy : std_logic;
    signal wire4_vld : std_logic;

    
    component tree_and_sram
        generic (
          key_length : integer;
          address_width : integer;
          codeword_length : integer;
          tree_depth : integer
        );
          port (
          key_in : in std_logic_vector(key_length - 1 downto 0);
          codeword : out std_logic_vector(codeword_length - 1 downto 0);
          data_in : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
          address : in std_logic_vector(address_width - 1 downto 0);
          RW : in std_logic;
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
          codeword_length : integer;
          num_of_codewords : integer
        );
          port (
          codeword_in0 : in std_logic_vector(codeword_length - 1 downto 0);
          codeword_in1 : in std_logic_vector(codeword_length - 1 downto 0);
          codeword_in2 : in std_logic_vector(codeword_length - 1 downto 0);
          codeword_out : out std_logic_vector((codeword_length * num_of_codewords) - 1 downto 0);
          rdy0 : out std_logic;
          vld0 : in std_logic;
          rdy1 : out std_logic;
          vld1 : in std_logic;
          rdy2 : out std_logic;
          vld2 : in std_logic;
          rdy_cuckoo_hash : in std_logic;
          vld_cuckoo_hash : out std_logic;
          clk : in std_logic;
          reset : in std_logic
        );
      end component;
begin

    tree0_and_sram_inst : tree_and_sram
    generic map (
      key_length => tree0_key_length,
      address_width => tree0_address_width,
      codeword_length => codeword_length,
      tree_depth => tree_depth
    )
    port map (
      key_in => tree0_key_in,
      codeword => wire0_codeword,
      data_in => tree0_data_in,
      address => tree0_address,
      RW => tree0_RW,
      rdy_collect_header => tree0_rdy_collect_header,
      vld_collect_header => tree0_vld_collect_header,
      rdy_codeword_concatinator => wire0_rdy,
      vld_codeword_concatinator => wire0_vld,
      clk => clk,
      reset => reset
    );

    tree1_and_sram_inst : tree_and_sram
    generic map (
      key_length => tree1_key_length,
      address_width => tree1_address_width,
      codeword_length => codeword_length,
      tree_depth => tree_depth
    )
    port map (
      key_in => tree1_key_in,
      codeword => wire1_codeword,
      data_in => tree1_data_in,
      address => tree1_address,
      RW => tree1_RW,
      rdy_collect_header => tree1_rdy_collect_header,
      vld_collect_header => tree1_vld_collect_header,
      rdy_codeword_concatinator => wire1_rdy,
      vld_codeword_concatinator => wire1_vld,
      clk => clk,
      reset => reset
    );

    tree2_and_sram_inst : tree_and_sram
    generic map (
      key_length => tree2_key_length,
      address_width => tree2_address_width,
      codeword_length => codeword_length,
      tree_depth => tree_depth
    )
    port map (
      key_in => tree2_key_in,
      codeword => wire2_codeword,
      data_in => tree2_data_in,
      address => tree2_address,
      RW => tree2_RW,
      rdy_collect_header => tree2_rdy_collect_header,
      vld_collect_header => tree2_vld_collect_header,
      rdy_codeword_concatinator => wire2_rdy,
      vld_codeword_concatinator => wire2_vld,
      clk => clk,
      reset => reset
    );

    tree3_and_sram_inst : tree_and_sram
    generic map (
      key_length => tree3_key_length,
      address_width => tree3_address_width,
      codeword_length => codeword_length,
      tree_depth => tree_depth
    )
    port map (
      key_in => tree3_key_in,
      codeword => wire3_codeword,
      data_in => tree3_data_in,
      address => tree3_address,
      RW => tree3_RW,
      rdy_collect_header => tree3_rdy_collect_header,
      vld_collect_header => tree3_vld_collect_header,
      rdy_codeword_concatinator => wire3_rdy,
      vld_codeword_concatinator => wire3_vld,
      clk => clk,
      reset => reset
    );

    tree4_and_sram_inst : tree_and_sram
    generic map (
      key_length => tree4_key_length,
      address_width => tree4_address_width,
      codeword_length => codeword_length,
      tree_depth => tree_depth
    )
    port map (
      key_in => tree4_key_in,
      codeword => wire4_codeword,
      data_in => tree4_data_in,
      address => tree4_address,
      RW => tree4_RW,
      rdy_collect_header => tree4_rdy_collect_header,
      vld_collect_header => tree4_vld_collect_header,
      rdy_codeword_concatinator => wire4_rdy,
      vld_codeword_concatinator => wire4_vld,
      clk => clk,
      reset => reset
    );

    codeword_concatinator_inst : codeword_concatinator
    generic map (
      codeword_length => codeword_length,
      num_of_codewords => num_of_codewords
    )
    port map (
      codeword_in0 => wire0_codeword,
      codeword_in1 => wire1_codeword,
      codeword_in2 => wire2_codeword,
      codeword_out => final_codeword,
      rdy0 => wire0_rdy,
      vld0 => wire0_vld,
      rdy1 => wire1_rdy,
      vld1 => wire1_vld,
      rdy2 => wire2_rdy,
      vld2 => wire2_vld,
      rdy_cuckoo_hash => rdy_cuckoo_hash,
      vld_cuckoo_hash => vld_cuckoo_hash,
      clk => clk,
      reset => reset
    );

end architecture;




