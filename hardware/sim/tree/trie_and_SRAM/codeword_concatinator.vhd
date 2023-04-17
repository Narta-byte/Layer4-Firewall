library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;
use work.my_types_pkg.all;
use ieee.std_logic_misc.and_reduce;

entity codeword_concatinator is
    generic (
        number_of_trees : integer := 5;
        tree_depth : integer := 16;
        address_width : tree_array := (8,8,8,16,8);
        total_address_width : integer := 48;
        address_width_cumsum : tree_array := (0,8,16,24,40,48);
        largest_address_width : integer := 16;
        key_in_lengths : tree_array:=(16,16,16,32,16);
        total_key_in_length : integer := 96; 
        tree_cumsum : tree_array :=  (0,16,32,48,80,96); -- ,96);
        codeword_length : tree_array := (16,16,16,16,16);
        largest_codeword : integer := 16
    );
    port (
        codeword_in :   in std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
        codeword_out : out std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);

        rdy_tree : out std_logic_vector(number_of_trees - 1 downto 0) := (others => '1');
        vld_tree : in std_logic_vector(number_of_trees - 1 downto 0);

        rdy_cuckoo_hash : in std_logic;
        vld_cuckoo_hash : out std_logic := '0';

        clk   : in std_logic;
        reset : in std_logic
        
    );
end entity codeword_concatinator;

architecture rtl of codeword_concatinator is
    
    signal flag : std_logic_vector(number_of_trees - 1 downto 0) := (others => '0');
    constant total_code_word_length : integer := largest_codeword * number_of_trees;
    constant ones : std_logic_vector(number_of_trees - 1 downto 0) := (others => '1');
begin
    -- codeword_out <= codeword_seg;

    process (clk, reset)
    begin
        if rising_edge(clk) then
            for i in 0 to number_of_trees - 1 loop
                if vld_tree(i) = '1' then
                    rdy_tree(i) <= '0';
                    flag(i) <= '1';
                    vld_cuckoo_hash <= '0';
                    codeword_out(total_code_word_length - largest_codeword * i - 1 downto total_code_word_length - largest_codeword*(i+1)) <= 
                    codeword_in (total_code_word_length - largest_codeword * i - 1 downto total_code_word_length - largest_codeword*(i+1));
                end if;
            end loop;
            if and_reduce(flag) = '1' and rdy_cuckoo_hash = '1'  then
                flag <= (others => '0');
                rdy_tree <= (others => '1');
                vld_cuckoo_hash <= '1';
            end if;

        elsif reset = '1' then
            flag <= (others => '0');

        end if;
    end process;

end architecture;