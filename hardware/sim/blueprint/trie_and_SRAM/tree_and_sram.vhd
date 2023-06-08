library ieee;
use ieee.std_logic_1164.all;
use work.my_types_pkg.all;

entity tree_and_sram is
    generic (
        key_length : integer := 32;
        address_width : integer := 8;
        codeword_length : integer := 16;
        tree_depth : integer := 16;
        max_iterations : integer := 1;
        tree_config : integer
    );
    port (
        key_in : in std_logic_vector(key_length - 1 downto 0);
        -- data_in : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
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

        clk   : in std_logic;
        reset : in std_logic
    );
end entity tree_and_sram;

architecture rtl of tree_and_sram is

    component trie_tree_logic
        generic (
          key_length : integer;
          address_width : integer;
          codeword_length : integer;
          max_iterations : integer;
          address_offset : integer
        );
          port (
          key_in : in std_logic_vector(key_length - 1 downto 0);
          codeword : out std_logic_vector(codeword_length - 1 downto 0);
          address : out std_logic_vector(address_width - 1 downto 0);
          data_from_memory : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
          RW : in std_logic;
          rdy_collect_header : out std_logic;
          vld_collect_header : in std_logic;

          rdy_codeword_concatinator : in std_logic;
          vld_codeword_concatinator : out std_logic;

          input_address : in std_logic_vector(address_width - 1 downto 0);
          output_address : out std_logic_vector(address_width - 1 downto 0);
  
          input_codeword : in std_logic_vector(codeword_length - 1 downto 0);
          key_out : out std_logic_vector(key_length - 1 downto 0);
          key_cnt_out : out std_logic_vector(4 downto 0 );
          key_cnt_in : in std_logic_vector(4 downto 0);

          clk : in std_logic;
          reset : in std_logic
        );
      end component;

      component SRAM
        generic (
          tree_depth : integer;
          codeword_length : integer;
          address_width : integer
        );
          port (
          clk : in std_logic;
          reset : in std_logic;
          RW : in std_logic;
          address : in std_logic_vector(address_width - 1 downto 0);
          data_in : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
          data_out : out std_logic_vector(codeword_length + address_width * 2 - 1 downto 0)
        );
      end component;


  signal wire0, wire1 : std_logic_vector(address_width - 1 downto 0);
  signal data_from_memory : std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);

  signal this_data_in : std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
  signal junk_a,junk_aa : std_logic_vector(address_width - 1 downto 0);
  signal junk_k : std_logic_vector(key_length - 1 downto 0);

  signal zero_input : std_logic_vector(address_width - 1 downto 0) := (others => '0');  

  signal tawire0, tawire1, tawire2, tawire3 : std_logic_vector(address_width - 1 downto 0);
  signal tcwire0, tcwire1, tcwire2, junk_c : std_logic_vector(codeword_length - 1 downto 0);

  signal trwire0, trwire1, trwire2 : std_logic;
  signal tvwire0, tvwire1, tvwire2 : std_logic;

  signal tkwire0, tkwire1, tkwire2 : std_logic_vector(key_length - 1 downto 0);

  signal swire0, swire1, swire2, swire3 : std_logic_vector(codeword_length + address_width * 2  - 1 downto 0);
  signal sawire0, sawire1, sawire2, sawire3 : std_logic_vector(address_width - 1 downto 0);
  signal tkcwire0, tkcwire1, tkcwire2, junk_kc : std_logic_vector(4 downto 0);
begin

  this_data_in <= codeword_in & zero_pointer & one_pointer;

    mux : process (wire0, address, RW, tawire0, tawire1, tawire2, tawire3)
    begin
        if RW = '1' then
          wire1 <= address;
          sawire0 <= address;
          sawire1 <= address;
          sawire2 <= address;
          sawire3 <= address;
        elsif RW = '0' then
          wire1 <= wire0;
          sawire0 <= tawire0;
          sawire1 <= tawire1;
          sawire2 <= tawire2;
          sawire3 <= tawire3;
          -- tawire0 <=sawire0;
          -- tawire1 <=sawire1;
          -- tawire2 <=sawire2;
          -- tawire3 <=sawire3;


        end if;
      
    end process;


    -- tree_gen : for i in 0 to tree_config generate
    --   if i = 0 generate
        
    --   elsif i /= 0 and i /= tree_config generate

    --   elsif i = tree_config generate

     
    --   end if;





    -- end generate;

    
    t0 : trie_tree_logic
    generic map (
      key_length => key_length,
      address_width => address_width,
      codeword_length => codeword_length,
      max_iterations => 8,
      address_offset => 0
    )
    port map (
      key_in => key_in,
      codeword => tcwire0,
      address => tawire0,
      data_from_memory => swire0,
      RW => RW,
      rdy_collect_header => rdy_collect_header,
      vld_collect_header => vld_collect_header,
      rdy_codeword_concatinator => trwire0,
      vld_codeword_concatinator => tvwire0,
      input_address => zero_input,
      output_address => junk_aa,
      input_codeword => junk_c,
      key_out => tkwire0,
      key_cnt_out => tkcwire0,
      key_cnt_in => junk_kc,
      clk => clk,
      reset => reset
    );

    t1 : trie_tree_logic
    generic map (
      key_length => key_length,
      address_width => address_width,
      codeword_length => codeword_length,
      max_iterations => 16,
      address_offset => 8
    )
    port map (
      key_in => tkwire0,
      codeword => tcwire1,
      address => tawire1,
      data_from_memory => swire1,
      RW => RW,
      rdy_collect_header => trwire0,
      vld_collect_header => tvwire0,
      rdy_codeword_concatinator => trwire1,
      vld_codeword_concatinator => tvwire1,
      input_address => tawire0,
      output_address => junk_a,
      input_codeword => tcwire1, -- THIS SHOULD BE TCWIRE0
      key_out => tkwire1,
      key_cnt_out => tkcwire1,
      key_cnt_in => tkcwire0,

      clk => clk,
      reset => reset
    );

    t2 : trie_tree_logic
    generic map (
      key_length => key_length,
      address_width => address_width,
      codeword_length => codeword_length,
      max_iterations => 24,
      address_offset => 16
    )
    port map (
      key_in => tkwire1,
      codeword => tcwire2,
      address => tawire2,
      data_from_memory => swire2,
      RW => RW,
      rdy_collect_header => trwire1,
      vld_collect_header => tvwire1,
      rdy_codeword_concatinator => trwire2,
      vld_codeword_concatinator => tvwire2,
      input_address => tawire1,
      output_address => junk_a,
      input_codeword => tcwire1,
      key_out => tkwire2,
      key_cnt_out => tkcwire2,
      key_cnt_in => tkcwire1,

      clk => clk,
      reset => reset
    );

    t3 :  trie_tree_logic
    generic map (
      key_length => key_length,
      address_width => address_width,
      codeword_length => codeword_length,
      max_iterations => 32,
      address_offset => 24
    )
    port map (
      key_in => tkwire2,
      codeword => codeword,
      address => tawire3,
      data_from_memory => swire3,
      RW => RW,
      rdy_collect_header => trwire2,
      vld_collect_header => tvwire2,
      rdy_codeword_concatinator => rdy_codeword_concatinator,
      vld_codeword_concatinator => vld_codeword_concatinator,
      input_address => tawire2,
      output_address => junk_a,
      input_codeword => tcwire2,
      key_out => junk_k,
      key_cnt_out => junk_kc,
      key_cnt_in => tkcwire2,
      clk => clk,
      reset => reset
    );

     
        
    s0 : SRAM
    generic map (
      tree_depth => tree_depth,
      codeword_length => codeword_length,
      address_width => address_width
    )
    port map (
      clk => clk,
      reset => reset,
      RW => RW,
      address => sawire0, 
      data_in => this_data_in,
      data_out => swire0
    );
    s1 : SRAM
    generic map (
      tree_depth => tree_depth,
      codeword_length => codeword_length,
      address_width => address_width
    )
    port map (
      clk => clk,
      reset => reset,
      RW => RW,
      address => sawire1,
      data_in => this_data_in,
      data_out => swire1
    );
    s2 : SRAM
    generic map (
      tree_depth => tree_depth,
      codeword_length => codeword_length,
      address_width => address_width
    )
    port map (
      clk => clk,
      reset => reset,
      RW => RW,
      address => sawire2,
      data_in => this_data_in,
      data_out => swire2
    );
    s3 : SRAM
    generic map (
      tree_depth => tree_depth,
      codeword_length => codeword_length,
      address_width => address_width
    )
    port map (
      clk => clk,
      reset => reset,
      RW => RW,
      address => sawire3,
      data_in => this_data_in,
      data_out => swire3
    );








    -- trie_tree_logic_inst : trie_tree_logic
    -- generic map (
    --   key_length => key_length,
    --   address_width => address_width,
    --   codeword_length => codeword_length,
    --   max_iterations => max_iterations
    -- )
    -- port map (
    --   key_in => key_in,
    --   codeword => codeword,
    --   address => wire0,
    --   data_from_memory => data_from_memory,
    --   RW => RW,
    --   rdy_collect_header => rdy_collect_header,
    --   vld_collect_header => vld_collect_header,
    --   rdy_codeword_concatinator => rdy_codeword_concatinator,
    --   vld_codeword_concatinator => vld_codeword_concatinator,
    --   input_address => junk_a,
    --   output_address => junk_aa,
    --   input_codeword => junk_c,
    --   key_cnt_out => junk_k,

    --   clk => clk,
    --   reset => reset
    -- );

    -- SRAM_inst : SRAM
    -- generic map (
    --   tree_depth => tree_depth,
    --   codeword_length => codeword_length,
    --   address_width => address_width
    -- )
    -- port map (
    --   clk => clk,
    --   reset => reset,
    --   RW => RW,
    --   address => wire1,
    --   data_in => this_data_in,
    --   data_out => data_from_memory
    -- );

end architecture;


