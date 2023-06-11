library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity hardware_trie_tree_logic is
    generic (
        key_length : integer := 16;
        address_width : integer := 8;
        codeword_length : integer := 16;
        max_iterations : integer := 1;
        address_offset : integer := 4;
        ismiddle : boolean := false;
        islast : boolean := false
    );

    port (
        key_in : in std_logic_vector(key_length - 1 downto  0); -- Maybe flip?
        codeword : out std_logic_vector(codeword_length - 1 downto 0);
        address : out std_logic_vector(address_width - 1 downto 0):= (others => '0') ;
        data_from_memory : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
        RW : in std_logic;
        
        rdy_collect_header : out std_logic;
        vld_collect_header : in std_logic;

        rdy_codeword_concatinator : in std_logic;
        vld_codeword_concatinator : out std_logic;

        input_address : in std_logic_vector(address_width - 1 downto 0);
        output_address : out std_logic_vector(address_width - 1 downto 0):= (others => '0');

        input_codeword : in std_logic_vector(codeword_length - 1 downto 0);

        key_out : out std_logic_vector(key_length - 1 downto 0);
        
        key_cnt_out : out std_logic_vector(4 downto 0 );
        
        key_cnt_in : in std_logic_vector(4 downto 0);

        clk   : in std_logic;
        reset : in std_logic
    );
end entity ;

architecture rtl of hardware_trie_tree_logic is
    type State_type is (
        idle_state,
        buffer_read_state,
        output_state,
        read_state,
        fetch_state);

    signal current_state, next_state : State_type;

    signal eof_key_flag, eof_key_flag_next : std_logic:= '0';
    signal key_cnt : natural range 0 to key_length - 1 := 0;
    signal zeros : std_logic_vector(address_width - 1 downto 0) := (others => '0');
    alias codeword_from_memory : std_logic_vector is data_from_memory(codeword_length + address_width*2 - 1 downto address_width*2);
    alias zeroPointer : std_logic_vector is data_from_memory(address_width*2 - 1 downto address_width);
    alias onePointer : std_logic_vector is data_from_memory(address_width - 1 downto 0);
    -- alias DEBUG_seq0 : std_logic_vector is data_from_memory(1 downto 0);
    
    signal codeword_zeros : std_logic_vector(codeword_length -1 downto 0) := (others => '0') ;
    
    signal best_codeword, final_codeword, best_codeword_next : std_logic_vector(codeword_length -1 downto 0);
    signal DEBUG_bool, DEBUG_bool_max_iter : boolean;
    signal DEBUG_bool_00, DEBUG_bool_01, DEBUG_bool_02 : std_logic;
    signal debug_key_in : std_logic;
    signal lock,lock_next : std_logic:= '0';
    signal output_codeword : std_logic_vector(codeword_length -1 downto 0);
    
    signal key_reg, key_reg_next : std_logic_vector(key_length - 1 downto 0);
    signal address_reg, address_reg_next : std_logic_vector(address_width - 1 downto 0);
    signal reg, reg_next : std_logic := '0';
    
    signal rdy_collect_header_next, vld_codeword_concatinator_next : std_logic;

    signal codeword_next : std_logic_vector(codeword_length - 1 downto 0);
    signal address_next : std_logic_vector(address_width - 1 downto 0);
    signal key_cnt_next : natural range 0 to key_length - 1 := 0;
    signal key_out_next : std_logic_vector(key_length - 1 downto 0);
    signal key_cnt_out_next : std_logic_vector(4 downto 0 );
    signal output_address_next : std_logic_vector(address_width - 1 downto 0);
begin


  debug_key_in <= key_in(key_cnt);
    STATE_MEMORY_LOGIC : process (clk, reset, RW)
    begin
      

      if reset = '1' or RW = '1' then -- if reset or read write is high, pause the state machine
        current_state <= idle_state;

      elsif rising_edge(clk) then
        current_state <= next_state;
        lock <= lock_next;
        reg <= reg_next;
        address_reg <= address_reg_next;
        key_reg <= key_reg_next;
        best_codeword <= best_codeword_next;

      end if;
    end process;
  
    NEXT_STATE_LOGIC : process (current_state, vld_collect_header, rdy_codeword_concatinator, eof_key_flag_next,lock, reg,lock_next)
    begin
      next_state <= current_state;
      case(current_state) is
  
      when idle_state =>
        if (vld_collect_header = '1') and lock_next = '0' then
          next_state <= buffer_read_state;
     
        end if;
      when buffer_read_state =>next_state <= fetch_state;
      when output_state => 
      if rdy_codeword_concatinator = '1'  then
        next_state <= idle_state;
      else
        next_state <= output_state;
      end if;


      when read_state =>
      if (eof_key_flag_next = '1' ) then
        next_state <= output_state;
      else
        next_state <= fetch_state;
        end if;
      when fetch_state =>
          next_state <= read_state;
        
      when others => next_state <= idle_state;
  
    end case;
  
    end process;
    OUTPUT_LOGIC : process (current_state, data_from_memory, eof_key_flag, key_cnt_in, input_address, key_in,
                            reg, input_codeword,lock,address_reg, key_reg,codeword_zeros,best_codeword,eof_key_flag_next,
									 key_cnt, zeros)
    begin
      eof_key_flag_next <= eof_key_flag;
      lock_next <= lock;
      reg_next <= reg;
      address_reg_next <= address_reg;
      key_reg_next <= key_reg;
      best_codeword_next <= best_codeword;
      key_cnt_next <= key_cnt;
      
      
      

      case(current_state) is
        when idle_state => 
          rdy_collect_header_next <= '1';
          reg_next <= '0';
          eof_key_flag_next <= '0';
          address_next <= input_address; 
          
          vld_codeword_concatinator_next <= '0';
          
          if ismiddle then
              key_cnt_next <= to_integer(unsigned(key_cnt_in));
              best_codeword_next <= input_codeword;
              codeword_next <= input_codeword;            
          else
            key_cnt_next <= 0;

            if codeword_from_memory /= codeword_zeros then
              best_codeword_next <= codeword_from_memory;
              codeword_next <= best_codeword;
            else
              best_codeword_next <= best_codeword;
              codeword_next <= best_codeword;
  
            end if;
          end if;

          


        when buffer_read_state => 
          rdy_collect_header_next <= '0';
          key_reg_next <= key_in;
          
        when output_state => 
        vld_codeword_concatinator_next <= '1';
        codeword_next <= best_codeword;
        output_codeword <= best_codeword;
        key_out_next <= key_reg;
        output_address_next <= address_reg;
        reg_next <= reg;
        if islast then
          reg_next <= '0';
        end if;

        when read_state =>
        if islast then
          reg_next <= '1';
        else
          reg_next <= '0';
        end if;



        
        DEBUG_bool <= ((codeword_from_memory /= best_codeword) and ((codeword_from_memory /= codeword_zeros)) );
        if ((codeword_from_memory /= best_codeword) and ((codeword_from_memory /= codeword_zeros)))  then
          best_codeword_next <= codeword_from_memory;
        else 
          best_codeword_next <= best_codeword;
        end if; 
        
        if  eof_key_flag = '1' then
          rdy_collect_header_next <= '1';
        else
          rdy_collect_header_next <= '0';
            

          end if;   


        when fetch_state =>
          
          rdy_collect_header_next <= '0';
          codeword_next <= best_codeword;
          DEBUG_bool_max_iter <= key_cnt = key_length - 1 or key_cnt = max_iterations -1;
          if key_cnt = key_length - 1 or key_cnt = max_iterations -1 then
            eof_key_flag_next <= '1';

            key_cnt_out_next <= std_logic_vector(to_unsigned(key_cnt, 5));
            report "key_cnt_out = " & integer'image(key_cnt);

          else
            eof_key_flag_next <= '0';
            key_cnt_next <= key_cnt +1; 
          end if;
          if zeroPointer = zeros and onePointer = zeros then
            address_reg_next <= zeroPointer;
            eof_key_flag_next <= '1';
          elsif key_in(key_cnt) = '0'  then
            address_next <= zeroPointer;
            address_reg_next <= zeroPointer;
            if zeroPointer = zeros then
              eof_key_flag_next <= '1';
            end if;
          elsif key_in(key_cnt) = '1' then
            DEBUG_bool_02 <= '1';
            address_next <= onePointer;
            address_reg_next <= onePointer;
            if onePointer = zeros then
              eof_key_flag_next <= '1';
            end if;
          else
            address_reg_next <= address_reg;
            eof_key_flag_next <= '0';
          end if;

        when others => report "ERROR IN OUTPUT LOGIC" severity failure;
    
      end case;
    end process;

end architecture;