library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;


entity codeword_concatinator is
    generic (
        number_of_trees : integer := 5;
        codeword_length : integer := 16
    );
    port (
        codeword_in :   in std_logic_vector(codeword_length * number_of_trees - 1 downto 0);
        codeword_out : out std_logic_vector(codeword_length * number_of_trees - 1 downto 0);

        rdy_tree : out std_logic_vector(number_of_trees - 1 downto 0) := (others => '1');
        vld_tree : in std_logic_vector(number_of_trees - 1 downto 0);

        rdy_cuckoo_hash : in std_logic;
        vld_cuckoo_hash : out std_logic := '0';

        clk   : in std_logic;
        reset : in std_logic
        
    );
end entity codeword_concatinator;

architecture rtl of codeword_concatinator is
    
    signal flag : std_logic_vector(number_of_trees - 1 downto 0) := (others => '1');
    signal codeword_seg : std_logic_vector(codeword_length * number_of_trees - 1 downto 0);

begin

    process (clk, reset)
    begin
        if rising_edge(clk) then

            -- if vld0 = '1' then
            --    codeword_seg0 <= codeword_in0;
            --    flag0 <= '1';
            -- end if;

            -- if vld1 = '1' then
            --    codeword_seg1 <= codeword_in1;
            --    flag1 <= '1';
            -- end if;

            -- if vld2 = '1' then
            --    codeword_seg2 <= codeword_in2;
            --    flag2 <= '1';
            -- end if;
            -- if (flag0 and flag1 and flag2) = '1' then
            --     flag0 <= '0';
            --     flag1 <= '0';
            --     flag2 <= '0';
                
            --     codeword_out <= (codeword_seg0 & codeword_seg1 & codeword_seg2);
            -- end if;

        elsif reset = '1' then
                flag <= (others => '1');

        end if;
    end process;

end architecture;