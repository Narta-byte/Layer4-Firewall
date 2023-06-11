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

        rdy_tree : out std_logic_vector(number_of_trees - 1 downto 0) := (others => '0');
        vld_tree : in std_logic_vector(number_of_trees - 1 downto 0);

        rdy_cuckoo_hash : in std_logic;
        vld_cuckoo_hash : out std_logic := '0';

        clk   : in std_logic;
        reset : in std_logic
        
    );
end entity codeword_concatinator;

architecture rtl of codeword_concatinator is
    
    signal flag, wait_signal : std_logic_vector(number_of_trees - 1 downto 0) := (others => '0');
    constant total_code_word_length : integer := largest_codeword * number_of_trees;
    constant ones : std_logic_vector(number_of_trees - 1 downto 0) := (others => '1');

    signal lock : std_logic := '0';
    signal reg : std_logic := '1';
begin
    -- codeword_out <= codeword_seg;

    process (clk, reset)
    begin
        if rising_edge(clk) then
            for i in 0 to number_of_trees - 1 loop
                if vld_tree(i) = '1'  then
                    if lock = '1' then
                        flag(i) <= '1';
                    end if;
                    lock <= '1';
                    wait_signal(i) <= '1';
                    -- if wait_signal(i) = '1' then
                        rdy_tree(i) <= '0';
                        -- wait_signal(i) <= '0';
                    -- end if;

                    -- flag(i) <= '1';
                    vld_cuckoo_hash <= '0';
                    codeword_out(total_code_word_length - largest_codeword * i - 1 downto total_code_word_length - largest_codeword*(i+1)) <= 
                    codeword_in (total_code_word_length - largest_codeword * i - 1 downto total_code_word_length - largest_codeword*(i+1));
                else 
                    
                
                end if;
            end loop;
            if flag = "11111" and rdy_cuckoo_hash = '1'  then
                flag <= (others => '0');
                rdy_tree <= (others => '1');
                vld_cuckoo_hash <= '1';
                lock <= '0';
                wait_signal <= (others => '0');
                
                
            -- elsif and_reduce(flag) = '1' and rdy_cuckoo_hash = '0' then
                -- flag <= (others => '0');
                -- rdy_tree <= (others => '0');
                -- vld_cuckoo_hash <= '0';
                -- lock <= '0';
                -- wait_signal <= (others => '0');
            end if;

        elsif reset = '1' then
            flag <= (others => '0');

        end if;
    end process;

end architecture;