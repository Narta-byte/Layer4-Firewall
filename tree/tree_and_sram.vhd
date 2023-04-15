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
        -- key_in : in std_logic_vector(key_length - 1 downto 0);
        -- data_in : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
        -- address : in std_logic_vector(address_width - 1 downto 0);
        -- RW : in std_logic;

        data_in : in std_logic_vector(
            key_length  +                              -- key
            codeword_length  + address_width * 2  + -- SRAM_data
            address_width  +                           -- address
            1 +                                              -- select
            (-1)
            downto 0);
        -- data_in : in std_logic_vector(
        --       16 - 1 +                              -- key
        --       16 - 1 + 8 * 2 - 1 + -- SRAM_data
        --       8 - 1 +                           -- address
        --       1                                             -- select
              
        --       downto 0);


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

  -- signal data_from_memory : std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
  -- alias key_in : std_logic_vector is data_in(key_length - 1 downto 
  --   codeword_length - 1 + address_width * 2 - 1 + 
  --   address_width - 1 +                         
  --   1);
  -- alias data_in0 : std_logic_vector is data_in(codeword_length - 1 + address_width * 2 - 1 +
  --   address_width - 1 +                         
  --   1 downto address_width - 1 +                         
  --   1);
  -- alias address : std_logic_vector is data_in(address_width - 1 +                        
  --   1 downto 1);
  -- alias RW : std_logic is data_in(0);
  constant total_length : integer:=key_length  +                             
                                   codeword_length  + address_width * 2  +
                                   address_width  +                          
                                   1;                     
                                   
                                   
  alias key_in :std_logic_vector is data_in(total_length - 1 downto total_length - key_length);

  alias data_in0 :std_logic_vector is data_in(total_length - key_length - 1 downto
                                             (total_length - key_length - 1) - (codeword_length + address_width * 2) + 1);

  alias address : std_logic_vector is data_in((total_length - key_length - 1) - (codeword_length + address_width * 2)  downto
                                              1);
  alias RW : std_logic is data_in(0);
  
  


  signal wire0, wire1 : std_logic_vector(address_width - 1 downto 0);
  signal data_from_memory : std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);



begin
    process (clk, RW)
    begin
      if rising_edge(clk) then
        if RW = '1' then
          wire1 <= address;
        else
          wire1 <= wire0;
        end if;
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
      data_in => data_in0,
      data_out => data_from_memory
    );

end architecture;


