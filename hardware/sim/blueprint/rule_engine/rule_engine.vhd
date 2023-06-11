library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.my_types_pkg.all;


entity rule_engine is
    generic (
        number_of_trees : integer := 5;
        tree_depth : integer := 16;

        address_width : tree_array := (8,8,8,16,8);
        total_address_width : integer := 48;
        address_width_cumsum : tree_array := (0,8,16,24,40,48);

        largest_address_width : integer := 16;

        key_in_lengths : tree_array:=(16,16,16,32,16);
        total_key_in_length : integer := 96; 

        tree_cumsum : tree_array :=  (0,16,32,48,80,96); 

        codeword_length : tree_array := (16,16,16,16,16);
        largest_codeword : integer := 16;
        codeword_sum : integer := 80
      );

    port (
        cmd_in : in std_logic_vector(4 downto 0);

        codeword_in : in std_logic_vector(largest_codeword - 1 downto 0);
        zero_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);
        one_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);

        codeword_out : out std_logic_vector(largest_codeword - 1 downto 0);
        zero_pointer_out : out std_logic_vector(largest_address_width - 1 downto 0);
        one_pointer_out : out std_logic_vector(largest_address_width - 1 downto 0);

        RW : out std_logic_vector(number_of_trees - 1 downto 0) := (others => '0');
        address : out std_logic_vector(largest_address_width - 1 downto 0);

        rdy_driver : out std_logic;
        vld_driver : in std_logic;



        cuckoo_select : out std_logic := '0';
        cuckoo_cmd : out std_logic_vector(1 downto 0);
        cuckoo_key_out : out std_logic_vector(codeword_sum + 8 - 1 downto 0) := (others => '0');

        cuckoo_key_in : in std_logic_vector(codeword_sum + 8 - 1 downto 0);

        cuckoo_rdy : in std_logic;
        cuckoo_vld : out std_logic := '0';
        cuckoo_set_rule : out std_logic := '0';
        clk   : in std_logic;
        reset : in std_logic
    );
end entity rule_engine;

architecture rtl of rule_engine is
    signal rw_reg : std_logic_vector(number_of_trees - 1 + 1 downto 0) := (number_of_trees downto 1 => '0') & '1';
    signal zeros : std_logic_vector(largest_codeword + largest_address_width * 2 - 1 downto 0) := (others => '0') ;
    signal debug : boolean;
    signal address_cnt : natural range 0 to 2**largest_address_width := 0;
    
begin

    RW <= rw_reg(number_of_trees downto 1);

    codeword_out <= codeword_in;
    zero_pointer_out <= zero_pointer_in;
    one_pointer_out <= one_pointer_in;
    address <= std_logic_vector(to_unsigned(address_cnt, largest_address_width));
    cuckoo_key_out <= cuckoo_key_in;

    process (clk, reset)
    begin
            if reset = '1' then
                rdy_driver <= '1';
                rw_reg <= (others => '0') ;
            elsif rising_edge(clk) then
                
                if cmd_in = "00001" and vld_driver = '1' then
                    debug <= (codeword_in & zero_pointer_in & one_pointer_in) = zeros;
                    

                    if (codeword_in & zero_pointer_in & one_pointer_in) = zeros then
                        rw_reg <= rw_reg(rw_reg'high - 1 downto rw_reg'low) & rw_reg(rw_reg'high);
                        address_cnt <= 0;
                        if rw_reg(rw_reg'high) = '1' then
                            rdy_driver <= '0';
                        end if;
                    else 
                        address_cnt <= address_cnt + 1;
                    end if;

                elsif cmd_in = "00010" and vld_driver = '1' then
                    if cuckoo_rdy = '1' then
                        rdy_driver <= '1';
                    else
                        rdy_driver <= '0';
                    end if;
                    cuckoo_cmd <= "01";
                    cuckoo_set_rule <= '1';
                    cuckoo_vld <= '1';
                    
                else
                    cuckoo_set_rule <= '0';
                    cuckoo_cmd <= "11";
                    rdy_driver <= '1';
                    cuckoo_vld <= '0';
                end if;


           
            end if;


        end process;
    

end architecture;

    