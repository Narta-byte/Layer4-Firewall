library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


entity trie_tree_logic is
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
end entity trie_tree_logic;

architecture rtl of trie_tree_logic is
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
    
    signal best_codeword, final_codeword : std_logic_vector(codeword_length -1 downto 0);
    signal DEBUG_bool, DEBUG_bool_max_iter : boolean;
    signal DEBUG_bool_00, DEBUG_bool_01, DEBUG_bool_02 : std_logic;
    signal debug_key_in : std_logic;
    signal lock,lock_next : std_logic:= '0';
    signal output_codeword : std_logic_vector(codeword_length -1 downto 0);
    
    signal key_reg : std_logic_vector(key_length - 1 downto 0);
    signal address_reg : std_logic_vector(address_width - 1 downto 0);
    signal reg, reg_next : std_logic := '0';
    -- signal iterations : integer range 0 to max_iterations := 0;
begin


  debug_key_in <= key_in(key_cnt);
    STATE_MEMORY_LOGIC : process (clk, reset, RW)
    begin
      

      if reset = '1' or RW = '1' then -- if reset or read write is high, pause the state machine
        current_state <= idle_state;

      elsif rising_edge(clk) then
        -- eof_key_flag <= eof_key_flag_next; --FIX ME
        current_state <= next_state;
      end if;
    end process;
  
    NEXT_STATE_LOGIC : process (current_state, vld_collect_header, rdy_codeword_concatinator, eof_key_flag_next,lock, reg)
    begin
      next_state <= current_state;
      lock_next <= lock;
      case(current_state) is
  
      when idle_state =>
        if (vld_collect_header = '1') and lock_next = '0' then
          next_state <= buffer_read_state;
          lock<= '0';
        -- elsif (vld_collect_header = '1') and lock_next = '1' then
        --   next_state <= idle_state;

        --   lock<= '1';
        end if;
      when buffer_read_state =>next_state <= fetch_state;
      when output_state => 
      if rdy_codeword_concatinator = '1'  then
        next_state <= idle_state;
      -- elsif rdy_codeword_concatinator = '1'  then
      --   next_state <= output_state;
      else
        next_state <= output_state;
      end if;


      when read_state =>
      if (eof_key_flag_next = '1' ) then--and rdy_codeword_concatinator = '1' then
        -- next_state <= idle_state;
        -- rdy_collect_header <= '1';
      -- elsif (eof_key_flag_next = '1' ) and rdy_codeword_concatinator = '0' then
        next_state <= output_state;
      else
        next_state <= fetch_state;
        end if;
      when fetch_state =>
        -- if eof_key_flag_next = '1' then
        --   next_state <= idle_state;
        -- else
          next_state <= read_state;
        -- end if;
        
      when others => next_state <= idle_state;
  
    end case;
  
    end process;
    OUTPUT_LOGIC : process (current_state, data_from_memory, eof_key_flag, key_cnt_in, input_address, key_in)
    begin
      eof_key_flag_next <= eof_key_flag;
    
      case(current_state) is
        when idle_state => 
          -- if rdy_codeword_concatinator = '1' then
          --   rdy_collect_header <= '1';
          -- else
          --   rdy_collect_header <= '0';
          -- end if;
          rdy_collect_header <= '1';
          reg <= '0';
          -- codeword <= (others => '0');
          eof_key_flag <= '0';
          -- address_reg <= input_address;
          address <= input_address; -- address get transfered incorrectly 
          -- address <= (others => '0');
          -- key_cnt <= 0;
          
          vld_codeword_concatinator <= '0';
          
          if ismiddle then
              key_cnt <= to_integer(unsigned(key_cnt_in));
              best_codeword <= input_codeword;
              codeword <= input_codeword;            
          else
            key_cnt <= 0;

            if codeword_from_memory /= codeword_zeros then
              best_codeword <= codeword_from_memory;
              codeword <= best_codeword;
            else
              best_codeword <= best_codeword;
              codeword <= best_codeword;
  
            end if;
          end if;

          


          -- output_codeword <= codeword_from_memory;
          -- iterations <= 0;
        when buffer_read_state => 
          rdy_collect_header <= '0';
          -- address <= address_reg;
          key_reg <= key_in;
          
        when output_state => 
        vld_codeword_concatinator <= '1';
        codeword <= best_codeword;
        -- key_cnt <= key_cnt;
        output_codeword <= best_codeword;
        key_out <= key_reg;
        output_address <= address_reg;
        -- rdy_collect_header <= '1'; -- maybe this should be here
        reg <= reg_next;
        if islast then
          reg_next <= '0';
        end if;

        when read_state =>
        eof_key_flag_next <= eof_key_flag_next;
        if islast then
          reg <= '1';
          reg_next <= '1';
        else
          reg <= '0';
          reg_next <= '0';
        end if;



        
        DEBUG_bool <= ((codeword_from_memory /= best_codeword) and ((codeword_from_memory /= codeword_zeros)) );
        if ((codeword_from_memory /= best_codeword) and ((codeword_from_memory /= codeword_zeros)))  then
          best_codeword <= codeword_from_memory;
        else 
          best_codeword <= best_codeword;
        end if; 
        
        if  eof_key_flag_next = '1' then
          -- vld_codeword_concatinator <= '1';
          -- codeword <= best_codeword;
          -- -- key_cnt <= key_cnt;
          -- output_codeword <= best_codeword;
          -- key_out <= key_reg;
          -- rdy_collect_header <= '1';
          -- address_reg <= address;
        else
          rdy_collect_header <= '0';
          -- elsif (iterations = max_iterations - 1) then
          --   codeword <= best_codeword;
          --   key_out <= key_in;
            

          end if;   


        when fetch_state =>
          -- iterations <= iterations + 1; -- why not just reuse keycount?

          rdy_collect_header <= '0';
          codeword <= best_codeword;
          -- output_codeword <= best_codeword; -- jeg tror at hvis man tilføjer et delay så virker det

          DEBUG_bool_max_iter <= key_cnt = key_length - 1 or key_cnt = max_iterations -1;
          if key_cnt = key_length - 1 or key_cnt = max_iterations -1 then
            -- report "max iterations reached";
            eof_key_flag_next <= '1';
            -- vld_codeword_concatinator <= '1';

            -- output_address
            key_cnt_out <= std_logic_vector(to_unsigned(key_cnt, 5)); -- this could be improved
            report "key_cnt_out = " & integer'image(key_cnt);

          else

            key_cnt <= key_cnt +1; 
          end if;
          DEBUG_bool_00 <= '0';
          DEBUG_bool_01 <= '0';
          DEBUG_bool_02 <= '0';
          -- report "key_in(key_cnt) = " & std_logic'image(key_in(key_cnt));
          if zeroPointer = zeros and onePointer = zeros then
            address_reg <= zeroPointer;
            DEBUG_bool_00 <= '1';
            -- codeword <= best_codeword;
            -- vld_codeword_concatinator <= '1';
            eof_key_flag_next <= '1';
          elsif key_in(key_cnt) = '0'  then
            address <= zeroPointer;
            address_reg <= zeroPointer;
            if zeroPointer = zeros then
              DEBUG_bool_01 <= '1';
              -- codeword <= best_codeword;
              -- vld_codeword_concatinator <= '1';
              eof_key_flag_next <= '1';
            end if;
          elsif key_in(key_cnt) = '1' then
            DEBUG_bool_02 <= '1';
            address <= onePointer;
            address_reg <= onePointer;
            if onePointer = zeros then
              -- codeword <= best_codeword;
              -- vld_codeword_concatinator <= '1';
              eof_key_flag_next <= '1';
            end if;
          end if;
          -- codeword <= (others => '0');

        when others => report "ERROR IN OUTPUT LOGIC" severity failure;
    
      end case;
    end process;

end architecture;