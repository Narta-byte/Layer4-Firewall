library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


entity trie_tree_logic is
    generic (
        key_length : integer := 16;
        address_width : integer := 8;
        codeword_length : integer := 16
    );

    port (
        key_in : in std_logic_vector(0 to key_length - 1);
        codeword : out std_logic_vector(codeword_length - 1 downto 0);
        address : out std_logic_vector(address_width - 1 downto 0);
        data_from_memory : in std_logic_vector(codeword_length + address_width * 2 - 1 downto 0);
        RW : in std_logic;
        
        rdy_collect_header : out std_logic;
        vld_collect_header : in std_logic;

        rdy_codeword_concatinator : in std_logic;
        vld_codeword_concatinator : out std_logic;

        clk   : in std_logic;
        reset : in std_logic
    );
end entity trie_tree_logic;

architecture rtl of trie_tree_logic is
    type State_type is (
        idle_state,
        read_state,
        fetch_state);

    signal current_state, next_state : State_type;

    signal eof_key_flag, eof_key_flag_next : std_logic:= '0';
    signal key_cnt : integer range 0 to key_length - 1 := 0;
    signal zeros : std_logic_vector(address_width - 1 downto 0) := (others => '0');
    alias codeword_from_memory : std_logic_vector is data_from_memory(codeword_length + address_width*2 - 1 downto address_width*2);
    alias zeroPointer : std_logic_vector is data_from_memory(address_width*2 - 1 downto address_width);
    alias onePointer : std_logic_vector is data_from_memory(address_width - 1 downto 0);
    -- alias DEBUG_seq0 : std_logic_vector is data_from_memory(1 downto 0);
    
    signal codeword_zeros : std_logic_vector(codeword_length -1 downto 0) := (others => '0') ;
    
    signal best_codeword, final_codeword : std_logic_vector(codeword_length -1 downto 0);
    signal DEBUG_bool : boolean;
begin
    STATE_MEMORY_LOGIC : process (clk, reset, RW)
    begin
      

      if reset = '1' or RW = '1' then -- if reset or read write is high, pause the state machine
        current_state <= idle_state;

      elsif rising_edge(clk) then
        -- eof_key_flag <= eof_key_flag_next; --FIX ME
        current_state <= next_state;
      end if;
    end process;
  
    NEXT_STATE_LOGIC : process (current_state, vld_collect_header, rdy_codeword_concatinator, eof_key_flag_next)
    begin
      next_state <= current_state;
      case(current_state) is
  
      when idle_state =>
        if vld_collect_header = '1' and rdy_codeword_concatinator = '1' then
          next_state <= fetch_state;
        end if;
  
      when read_state =>
      if eof_key_flag_next = '1' then
        next_state <= idle_state;
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
    OUTPUT_LOGIC : process (current_state, data_from_memory, eof_key_flag)
    begin
      eof_key_flag_next <= eof_key_flag;
    
      case(current_state) is
        when idle_state => 
          rdy_collect_header <= '1';
          -- codeword <= (others => '0');
          eof_key_flag <= '0';
          address <= (others => '0');
          key_cnt <= 0;
          vld_codeword_concatinator <= '0';
          best_codeword <= codeword_from_memory;


        when read_state =>
          rdy_collect_header <= '0';
          eof_key_flag_next <= eof_key_flag_next;
          
          
          DEBUG_bool <= (codeword_from_memory /= best_codeword) and ((codeword_from_memory = codeword_zeros));
          if ((codeword_from_memory /= best_codeword) and ((codeword_from_memory /= codeword_zeros)))   then
            best_codeword <= codeword_from_memory;
          end if; 
          
          if  eof_key_flag_next = '1' then
            codeword <= codeword_from_memory;
        
          end if; 
        when fetch_state =>
          rdy_collect_header <= '0';
          codeword <= best_codeword;
          if key_cnt = key_length - 1 then
            eof_key_flag_next <= '1';
            vld_codeword_concatinator <= '1';
            key_cnt <= key_cnt;
          
          else
            key_cnt <= key_cnt +1; 
          end if;
          
          -- report "key_in(key_cnt) = " & std_logic'image(key_in(key_cnt));
          
          if key_in(key_cnt) = '0' then
            address <= zeroPointer;
            if zeroPointer = zeros then
              -- codeword <= best_codeword;
              vld_codeword_concatinator <= '1';
              eof_key_flag_next <= '1';
            end if;
          else
            address <= onePointer;
            if onePointer = zeros then
              -- codeword <= best_codeword;
              vld_codeword_concatinator <= '1';
              eof_key_flag_next <= '1';
            end if;
          end if;
          -- codeword <= (others => '0');

        when others => report "ERROR IN OUTPUT LOGIC" severity failure;
    
      end case;
    end process;

end architecture;