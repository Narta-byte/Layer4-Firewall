library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;
use work.my_types_pkg.all;


entity NEW_tree_collection is
    generic (
        number_of_trees : integer := 5;
        address_width : integer := 8;
        tree_depth : integer := 16;

        tree_atributes : tree_array:=(16,16,16,16,32);
        total_tree_attributes : integer := 96;  
        -- total_tree_address : integer := number_of_trees * address_width ;

        codeword_length : integer := 16

    );
    port (
        data_in : in std_logic_vector(
            total_tree_attributes - 1 +                                   --key_in
            (codeword_length + address_width * 2 - 1) * number_of_trees + --data_in
            (address_width - 1) * number_of_trees +                       -- address
            number_of_trees                                               -- RW (select)
        downto 0);

        data_out : out std_logic_vector(
            number_of_trees -- rdy_collect_header
        downto 0);
        vld_collect_header : in std_logic_vector(number_of_trees -1 downto 0); -- vld_collect_header;

        clk   : in std_logic;
        reset : in std_logic
        
    );
end entity NEW_tree_collection;

architecture rtl of NEW_tree_collection is
  component new_tree_and_sram
    generic (
      key_length : integer;
      address_width : integer;
      codeword_length : integer;
      tree_depth : integer
    );
      port (
      data_in : in std_logic_vector(
              key_length - 1 +                              -- key
              codeword_length - 1 + address_width * 2 - 1 + -- SRAM_data
              address_width - 1 +                           -- address
              1                                             -- select
              
              downto 0);
      codeword : out std_logic_vector(codeword_length - 1 downto 0);
      rdy_collect_header : out std_logic;
      vld_collect_header : in std_logic;
      rdy_codeword_concatinator : in std_logic;
      vld_codeword_concatinator : out std_logic;
      clk : in std_logic;
      reset : in std_logic
    );
  end component;
  
      
      component test is 
        port (
          data_in : in std_logic_vector(31 downto 0);
          data_out : out std_logic_vector(31 downto 0);
          clk : in std_logic;
          reset : in std_logic
        );
      end component;


      constant offset : natural := total_tree_attributes - 1 +                                  --key_in
                                  (codeword_length + address_width * 2 - 1) * number_of_trees + --data_in
                                  (address_width - 1) * number_of_trees +                       -- address
                                  number_of_trees;                                              -- RW (select);
      
      signal lower_bound : tree_array(0 to number_of_trees ) := (0) & (tree_atributes);

      signal codeword_o : std_logic_vector((codeword_length - 1) * number_of_trees downto 0);


      signal offset_key_in : integer := -- tree_atributes(i) +
                                 (codeword_length + address_width * 2 - 1) +
                                 address_width +
                                 1 +
                                 1;

      signal offset_data_in : integer := -- tree_atributes(i) +
                                 (codeword_length + address_width * 2 - 1) +
                                 address_width +
                                 1 +
                                 1;

                 
       signal w_rdy_concatinator : std_logic_vector(number_of_trees - 1 downto 0);
       signal w_vld_concatinator : std_logic_vector(number_of_trees - 1 downto 0);

    begin
    tree_gen : for i in 0 to number_of_trees generate

      new_tree_and_sram_inst : new_tree_and_sram
      generic map (
        key_length => tree_atributes(i),
        address_width => address_width,
        codeword_length => codeword_length,
        tree_depth => tree_depth
      )
      port map (
        data_in => data_in((i+1)*offset - 1 downto i*offset),
        codeword => codeword_o((i + 1)*(codeword_length - 1) downto i*(codeword_length - 1)),
        rdy_collect_header => data_out(i),
        vld_collect_header => vld_collect_header(i),
        rdy_codeword_concatinator => w_rdy_concatinator(i),
        vld_codeword_concatinator => w_vld_concatinator(i),
        clk => clk,
        reset => reset
      );
    
    end generate;

      








    -- asdf : for i in 0 to 5 generate
    --   inst : test
    --     port map (
    --       data_in => data_in((i+1)*31 downto (i)*31),
    --       data_out => data_out((i+1)*31 downto (i)*31),
    --       clk => clk,
    --       reset => reset
    --     );
    -- end generate;

end architecture;