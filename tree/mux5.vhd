library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;

entity mux5 is
    generic (
        address_width : integer;
        codeword_length : integer
      );
    port(
      c0      : out  std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      c1      : out  std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      c2      : out  std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      c3      : out  std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      c4      : out  std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
      
      r0      : out  std_logic;
      r1      : out  std_logic;
      r2      : out  std_logic;
      r3      : out  std_logic;
      r4      : out  std_logic;

      a0      : out std_logic_vector(address_width - 1 downto 0);
      a1      : out std_logic_vector(address_width - 1 downto 0);
      a2      : out std_logic_vector(address_width - 1 downto 0);
      a3      : out std_logic_vector(address_width - 1 downto 0);
      a4      : out std_logic_vector(address_width - 1 downto 0);

      sel     : in  std_logic_vector(2 downto 0);
      address_in : in  std_logic_vector(address_width - 1 downto 0);
      r_in    : in  std_logic;
      b       : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0));
      
end mux5;
architecture rtl of mux5 is
begin
  c0 <= b;
  c1 <= b;
  c2 <= b;
  c3 <= b;
  c4 <= b;

  a0 <= address_in;
  a1 <= address_in;
  a2 <= address_in;
  a3 <= address_in;
  a4 <= address_in;
  
    process (sel)
    begin
      
        case sel is
        when "000" => r0 <= r_in; r1 <= '0'; r2 <= '0'; r3 <= '0'; r4 <= '0';
        when "001" => r1 <= r_in; r0 <= '0'; r2 <= '0'; r3 <= '0'; r4 <= '0';
        when "010" => r2 <= r_in; r0 <= '0'; r1 <= '0'; r3 <= '0'; r4 <= '0';
        when "011" => r3 <= r_in; r0 <= '0'; r1 <= '0'; r2 <= '0'; r4 <= '0';
        when "100" => r4 <= r_in; r0 <= '0'; r1 <= '0'; r2 <= '0'; r3 <= '0';

        when others => null;
        
    
    
    end case;
    end process;
   

end architecture rtl;

