library ieee;
use ieee.std_logic_1164.all;


entity tree_and_sram is
    generic (
        key_length : integer := 32;
        address_width : integer := 8;
        codeword_length : integer := 16;
        tree_depth : integer := 16
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
          codeword_length : integer
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
  

begin

  this_data_in <= codeword_in & zero_pointer & one_pointer;

    mux : process (wire0, address, RW)
    begin
        if RW = '1' then
          wire1 <= address;
        elsif RW = '0' then
          wire1 <= wire0;
        end if;
      
    end process;

    trie_tree_logic_inst : trie_tree_logic
    generic map (
      key_length => key_length,
      address_width => address_width,
      codeword_length => codeword_length
    )
    port map (
      key_in => key_in,
      codeword => codeword,
      address => wire0,
      data_from_memory => data_from_memory,
      RW => RW,
      rdy_collect_header => rdy_collect_header,
      vld_collect_header => vld_collect_header,
      rdy_codeword_concatinator => rdy_codeword_concatinator,
      vld_codeword_concatinator => vld_codeword_concatinator,
      clk => clk,
      reset => reset
    );

    SRAM_inst : SRAM
    generic map (
      tree_depth => tree_depth,
      codeword_length => codeword_length,
      address_width => address_width
    )
    port map (
      clk => clk,
      reset => reset,
      RW => RW,
      address => wire1,
      data_in => this_data_in,
      data_out => data_from_memory
    );

end architecture;


