library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;


entity codeword_concatinator is
    generic (
        codeword_length : integer := 16;
        num_of_codewords : integer := 3
    );
    port (
        codeword_in0 : in std_logic_vector(codeword_length - 1 downto 0);
        codeword_in1 : in std_logic_vector(codeword_length - 1 downto 0);
        codeword_in2 : in std_logic_vector(codeword_length - 1 downto 0);
        
        codeword_out : out std_logic_vector((codeword_length * num_of_codewords) - 1 downto 0);

        rdy0  : out std_logic := '1';
        vld0  : in std_logic;

        rdy1  : out std_logic := '1';
        vld1  : in std_logic;

        rdy2  : out std_logic := '1';
        vld2  : in std_logic;

        rdy_cuckoo_hash : in std_logic;
        vld_cuckoo_hash : out std_logic := '0';

        clk   : in std_logic;
        reset : in std_logic
        
    );
end entity codeword_concatinator;

architecture rtl of codeword_concatinator is
    signal codeword_seg0 : std_logic_vector(codeword_length-1 downto 0) := (others => '0');
    signal codeword_seg1 : std_logic_vector(codeword_length-1 downto 0) := (others => '0');
    signal codeword_seg2 : std_logic_vector(codeword_length-1 downto 0) := (others => '0');
    
    signal flag0 : std_logic := '0';
    signal flag1 : std_logic := '0';
    signal flag2 : std_logic := '0';
    

begin

    rdy0 <= not flag0;
    rdy1 <= not flag1;
    rdy2 <= not flag2;

    process (clk, reset)
    begin
        if rising_edge(clk) then

            if vld0 = '1' then
               codeword_seg0 <= codeword_in0;
               flag0 <= '1';
            end if;

            if vld1 = '1' then
               codeword_seg1 <= codeword_in1;
               flag1 <= '1';
            end if;

            if vld2 = '1' then
               codeword_seg2 <= codeword_in2;
               flag2 <= '1';
            end if;
            if (flag0 and flag1 and flag2) = '1' then
                flag0 <= '0';
                flag1 <= '0';
                flag2 <= '0';
                
                codeword_out <= (codeword_seg0 & codeword_seg1 & codeword_seg2);
            end if;
            

            if reset = '1' then
                flag0 <= '1';
                flag1 <= '1';
                flag2 <= '1';
            end if;

        end if;
    end process;

end architecture;