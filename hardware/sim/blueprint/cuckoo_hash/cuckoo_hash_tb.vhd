library IEEE;
library std;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use ieee.std_logic_unsigned.all;
use std.textio.all;
use STD.textio.all;
use IEEE.std_logic_textio.all;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Cuckoo_Hashing_tb is
end;

architecture bench of Cuckoo_Hashing_tb is

  component Cuckoo_Hashing
      port (
      clk : in std_logic;
      reset : in std_logic;
      set_rule : in std_logic;
      cmd_in : in std_logic_vector(1 downto 0);
      key_in : in std_logic_vector(95 downto 0);
      header_data : in std_logic_vector(95 downto 0);
      vld_hdr : in std_logic;
      rdy_hash : out std_logic;
      vld_firewall_hash : in std_logic;
      rdy_firewall_hash : out std_logic;
      acc_deny_hash : out std_logic;
      vld_ad_hash : out std_logic;
      rdy_ad_hash : in std_logic
    );
  end component;

  

  -- Ports
  signal clk : std_logic;
  signal reset : std_logic;
  signal set_rule : std_logic;
  signal cmd_in : std_logic_vector(1 downto 0);
  signal key_in : std_logic_vector(95 downto 0);
  signal header_data : std_logic_vector(95 downto 0);
  signal vld_hdr : std_logic;
  signal rdy_hash : std_logic;
  signal vld_firewall_hash : std_logic;
  signal rdy_firewall_hash : std_logic;
  signal acc_deny_hash : std_logic;
  signal vld_ad_hash : std_logic;
  signal rdy_ad_hash : std_logic;

 
  -- constants
  constant data_length : integer := 513;
  
  -- fsm logic
  type State_type is (setup_rulesearch,set_key,wait_for_ready_insert,send_key,terminate_insertion, wipe_memory,wait_for_last_calc_to_finish,
                      goto_cmd_state, start_hash_matching, send_match_key, wait_for_ready_match,terminate_match,test_a_wrong_header,
                      wait_for_match_to_fin, wait_for_wrong_calc_to_fin);
  signal current_state, next_state : State_type;

  signal data_end,done_looping,last_rdy,calc_is_done : std_logic :='0';

  --maybe make theese varibles in output logic  
  signal cnt : integer;
  type data_array is array (0 to data_length) of std_logic_vector(95 downto 0);
  signal data_array_sig : data_array;

  --signals in hashmatching
  signal match_done : std_logic := '0'; 
  signal cnt_calc_fin : integer := 0;

  --signals for ac
  signal ok_cnt,ko_cnt : integer := 0;
  
begin

  Cuckoo_Hashing_inst : Cuckoo_Hashing
  port map (
    clk => clk,
    reset => reset,
    set_rule => set_rule,
    cmd_in => cmd_in,
    key_in => key_in,
    header_data => header_data,
    vld_hdr => vld_hdr,
    rdy_hash => rdy_hash,
    vld_firewall_hash => vld_firewall_hash,
    rdy_firewall_hash => rdy_firewall_hash,
    acc_deny_hash => acc_deny_hash,
    vld_ad_hash => vld_ad_hash,
    rdy_ad_hash => rdy_ad_hash
  );

  
 

CLK_PROCESS : process 
begin
  clk <= '1';
  wait for 10 ns;
  clk <= '0';
    wait for 10 ns;
    end process;


    STATE_MEMORY_LOGIC : process (clk, reset)
    begin
        if reset = '1' then
            current_state <= setup_rulesearch;
        elsif rising_edge(clk) then
            current_state <= next_state;
        end if ;
    end process;  


  NEXT_STATE_LOGIC : process (current_state, done_looping, rdy_firewall_hash, vld_firewall_hash, data_end,calc_is_done,
                              rdy_hash, vld_hdr, cnt_calc_fin, rdy_ad_hash)
  begin
    next_state <= current_state; -- måske sus
      case current_state is
        when setup_rulesearch =>
          next_state <= wipe_memory;

        when wipe_memory => next_state <= set_key;

        when set_key => if done_looping = '1' then
          next_state <= wait_for_ready_insert;
        end if ;

        next_state <= send_key;
        when wait_for_ready_insert => if data_end = '1' then
          next_state <= wait_for_last_calc_to_finish;
        elsif  rdy_firewall_hash = '1' and vld_firewall_hash = '1'then
          next_state <= send_key;
        end if ;
        
        when send_key =>
          next_state <= wait_for_ready_insert;
        
        when terminate_insertion => 
          if not (cnt_calc_fin = 2) and rdy_firewall_hash = '1' then
            cnt_calc_fin <= cnt_calc_fin +1;
          elsif (cnt_calc_fin = 2)  then
            next_state <= goto_cmd_state;
          end if;
          
         when wait_for_last_calc_to_finish => 
          if rdy_firewall_hash = '1' then
            next_state <= terminate_insertion;
          end if;

        when goto_cmd_state => next_state <= start_hash_matching;

        when start_hash_matching => --next_state <= wait_for_ready_match;
          next_state <= send_match_key;


        when send_match_key => 
          next_state <= wait_for_ready_match;
        
        when wait_for_ready_match => 
          if match_done = '1' then
            next_state <= wait_for_match_to_fin;
          elsif  (rdy_hash = '1') and (vld_hdr = '1')  then
            next_state <= send_match_key;
          end if ;
        when terminate_match => next_state <= terminate_match;

        when test_a_wrong_header => next_state <= wait_for_wrong_calc_to_fin;
            
        when wait_for_match_to_fin => 
          if rdy_hash = '1' then
            next_state <= test_a_wrong_header;
          end if;
        
        when wait_for_wrong_calc_to_fin =>
          if rdy_hash = '1' then
            next_state <= terminate_match;
          end if;
        when others =>
          next_state <= setup_rulesearch;
      end case;
  end process;

  OUTPUT_LOGIC : process (current_state)
  file input : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/hardware/sim/blueprint/cuckoo_hash/large_input_file_increment.txt";
  variable current_read_line : line;
  variable hex_reader : std_logic_vector(95 downto 0);
  
  file output : text open WRITE_MODE is "DEBUG_OUTPUT.txt";
  variable write_line : line;
  begin     
      case current_state is
      when setup_rulesearch => 
        set_rule <= '1';
	      cnt <= 0;
      
      when wipe_memory => cmd_in <= "00";
      when set_key =>
       
          READ_ARRAY : for i in 0 to data_length loop
            if not ENDFILE(input) then
              
              readline(input, current_read_line);
              READ(current_read_line, hex_reader);
              
              data_array_sig(i) <= hex_reader;
              end if ;
          
          end loop ; -- READ_ARRAY
          -- READ_ARRAY : for i in 0 to data_length-1 loop
          --   --   if not ENDFILE(input) then
                
          --   --     readline(input, current_read_line);
          --   --     READ(current_read_line, hex_reader);
                
          --   --     data_array_sig(i) <= hex_reader;
          --   --     end if ;
          --   data_array_sig(i) <= std_logic_vector(to_unsigned(i,96));
          -- end loop ; -- READ_ARRAY

        done_looping <= '1';
        cmd_in <= "01";
        vld_firewall_hash <= '1';
      when wait_for_ready_insert => 
            
      when send_key =>
          key_in <= data_array_sig(cnt);
          cnt <= cnt+1;
          if cnt = data_length then
            data_end <= '1';
            
          end if ;
          -- DEBUG_LOOP : for i in 0 to 160 loop
          --   write(write_line,data_array_sig(i));
          --   writeline(output,write_line);
          -- end loop ; -- DEBUG_LOOP
      when terminate_insertion => 
              vld_firewall_hash <= '0';
              cmd_in <= "11";

      when wait_for_last_calc_to_finish => --vld_firewall_hash <= '0';
      
      when goto_cmd_state => 

      when start_hash_matching => 
          cmd_in <= "11";
          cnt <= 0;
          vld_hdr <= '1';
          rdy_ad_hash <= '1'; --this simulates that the accept deny block is always ready
          --header_data <= "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000" & data_array_sig(cnt); 
          
         
          
      when send_match_key => 
          header_data <=  data_array_sig(cnt); 
          cnt <= cnt +1;            
          if cnt = data_length then
            match_done <= '1';
          end if ;

      when wait_for_ready_match => 
            --vld_hdr<= '1';
            set_rule <= '0';
          if acc_deny_hash = '1' then
              ok_cnt <= ok_cnt +1;
          elsif acc_deny_hash = '0' then
              ko_cnt <= ko_cnt +1;
          end if;
            

      when terminate_match => vld_hdr <= '0';

      when test_a_wrong_header => 
        --header_data <= "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000" & "00011111";
        --header_data <= "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000" & "11111111";
        header_data <= "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111" & "11111111";

      when wait_for_match_to_fin => 
      
      
      when wait_for_wrong_calc_to_fin =>
      

      when others => report "FAILURE" severity failure;
          
      end case;
   
  end process;

 end;