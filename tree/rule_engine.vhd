library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;


entity rule_engine is
    generic (
        address_width : integer;
        codeword_length : integer;
        tree_depth : integer;

        tree0_key_length : integer:= 16;
        tree0_address_width : integer:= 8;
        tree1_key_length : integer:= 16;
        tree1_address_width : integer:= 8;
        tree2_key_length : integer:= 16;
        tree2_address_width : integer:= 8;
        tree3_key_length : integer:= 16;
        tree3_address_width : integer:= 8;
        tree4_key_length : integer:= 16;
        tree4_address_width : integer:= 8
      );

    port (
        cmd_in : in std_logic_vector(4 downto 0);
        data_in : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
        data_out : out std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
        RW : out std_logic;
        sel : out std_logic_vector(2 downto 0) := "000";
        address : out std_logic_vector(address_width - 1 downto 0);

        rdy : out std_logic;
        vld : in std_logic;

        clk   : in std_logic;
        reset : in std_logic
    );
end entity rule_engine;

architecture rtl of rule_engine is
    signal tree_cnt : natural range 0 to 2 ** tree0_address_width - 1 := 0; -- address with has to be the largest

    signal num_tree_cnt : natural range 0 to 4 := 0;

    signal sel_reg : integer range 0 to 15 := 0;
    

    
begin

    sel <=  std_logic_vector(to_unsigned(sel_reg, 3));
    
    process (clk, reset)
    begin
        data_out <= data_in;
            if reset = '1' then
                rdy <= '0';
                sel_reg <= 0;
            elsif rising_edge(clk) then
                
                if cmd_in = "00001" and vld = '1' then
                    RW <= '1';

                    if tree_cnt < 2 ** tree0_address_width - 1 then
                        tree_cnt <= tree_cnt + 1;
                    else
                        tree_cnt <= 0;
                        sel_reg <= sel_reg + 1;
                        

                    end if;



                    -- if tree_cnt < 2 ** tree0_address_width - 1 and sel_reg = "000" then
                    --     tree_cnt <= tree_cnt + 1;
                    -- else
                    --     tree_cnt <= 0;
                    --     sel_reg <= "001";
                    -- end if;

                    -- if tree_cnt < 2 ** tree1_address_width - 1 and sel_reg = "001" then
                    --     tree_cnt <= tree_cnt + 1;
                    -- else
                    --     tree_cnt <= 0;
                    --     sel_reg <= "010";
                    -- end if;

                    -- if tree_cnt < 2 ** tree2_address_width - 1 and sel_reg = "010" then
                    --     tree_cnt <= tree_cnt + 1;
                    -- else
                    --     tree_cnt <= 0;
                    --     sel_reg <= "011";
                    -- end if;

                    -- if tree_cnt < 2 ** tree3_address_width - 1 and sel_reg = "011" then
                    --     tree_cnt <= tree_cnt + 1;
                    -- else
                    --     tree_cnt <= 0;
                    --     sel_reg <= "100";
                    -- end if;

                    -- if tree_cnt < 2 ** tree4_address_width - 1 and sel_reg = "100" then
                    --     tree_cnt <= tree_cnt + 1;
                    -- else
                    --     tree_cnt <= 0;
                    --     -- sel_reg <= "000";
                    --     rdy <= '0';
                    -- end if;
                    


                    
                else
                    rdy <= '1';
                    RW <= '0';

                end if;





            end if;


        end process;
    

end architecture;

    