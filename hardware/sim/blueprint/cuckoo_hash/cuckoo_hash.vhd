library IEEE;
library std;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use ieee.std_logic_unsigned.all;
use std.textio.all;
use STD.textio.all;
use IEEE.std_logic_textio.all;
use work.my_types_pkg.all;


entity Cuckoo_Hashing is
  generic (
    number_of_trees : integer;
    tree_depth : integer;
    address_width : tree_array;
    total_address_width : integer;
    address_width_cumsum : tree_array;
    largest_address_width : integer;
    key_in_lengths : tree_array;
    total_key_in_length : integer;
    tree_cumsum : tree_array;
    codeword_length : tree_array;
    largest_codeword : integer;
    codeword_sum : integer
  );
  port (
    clk : in std_logic;
    reset : in std_logic;

    set_rule : in std_logic;
    cmd_in : in std_logic_vector(1 downto 0);
    key_in : in std_logic_vector(codeword_sum + 8 - 1 downto 0);

    header_data : in std_logic_vector(codeword_sum - 1 downto 0);
    vld_hdr : in std_logic;
    rdy_hash : out std_logic;

    vld_firewall_hash : in std_logic;
    rdy_firewall_hash : out std_logic;

    acc_deny_hash : out std_logic := '0';
    vld_ad_hash : out std_logic;
    rdy_ad_hash : in std_logic;
    decision_ad : out std_logic_vector(7 downto 0)
  );
end Cuckoo_Hashing;

architecture Cuckoo_Hashing_tb of Cuckoo_Hashing is

  type State_type is (
    -- flush and control
    command_state,
    flush_memory,
    -- insert
    rdy_hash_matching,
    lookup_hash1,
    lookup_hash2,
    insert_key,
    remember_and_replace,
    ERROR, is_occupied,
    rdy_key,
    -- match
    rdy_for_match,
    search_hash1,
    search_hash2,
    matching,
    AD_communication,
    -- delete
    rdy_delete,
    find_hashfun1,
    find_hashfun2,
    match_for_delete,
    delete_from_memory
  );

  signal current_state, next_state : State_type;

  signal exits_cuckoo, insert_flag, hashfun, flip, flush_flag, eq_key, delete_flag : std_logic := '0';
  
  -- CONSTANTS
  constant MAX_ITER : integer range 0 to 31:= 31;
  signal MAX : integer range 0 to MAX_ITER := 0;

  -- Hash matching signals
  signal exits_matching, previous_search : std_logic := '0';
  signal insertion_key : std_logic_vector(codeword_sum + 8 - 1 downto 0) := (others => '0');

  component cuckoo_SRAM
    generic (
      number_of_trees : integer;
      tree_depth : integer;
      address_width : tree_array;
      total_address_width : integer;
      address_width_cumsum : tree_array;
      largest_address_width : integer;
      key_in_lengths : tree_array;
      total_key_in_length : integer;
      tree_cumsum : tree_array;
      codeword_length : tree_array;
      largest_codeword : integer;
      codeword_sum : integer
    );
    port (
      clk : in std_logic;
      reset : in std_logic;
      flush_sram : in std_logic;
      occupied : in std_logic;
      RW : in std_logic;
      address : in std_logic_vector(8 downto 0);
      data_in : in std_logic_vector(codeword_sum  + 8 -1 downto 0);
      data_out : out std_logic_vector(codeword_sum + 8 + 1 downto 0)
    );
  end component;

  signal flush_cuckoo_sram : std_logic := '0';
  signal occupied : std_logic := '0';
  signal RW : std_logic := '0';
  signal address : std_logic_vector(8 downto 0) := (others => '0');
  signal data_in : std_logic_vector(codeword_sum + 8 - 1 downto 0) := (others => '0');
  signal data_out : std_logic_vector(codeword_sum + 8 - 1 + 1 downto 0) := (others => '0');

  --debug

  --crc fun
  constant g1 : std_logic_vector(8 downto 0) := "100101111";
  constant g2 : std_logic_vector(8 downto 0) := "101001001";

  --Next signals
  signal flush_flag_next : std_logic;
  signal delete_flag_next : std_logic;
  signal insert_flag_next : std_logic;
  signal flush_cuckoo_SRAM_next : std_logic;
  signal flip_next : std_logic;
  signal rdy_firewall_hash_next : std_logic;
  signal insertion_key_next : std_logic_vector (codeword_sum + 8 - 1 downto 0);
  signal MAX_next : integer range 0 to MAX_ITER;
  signal eq_key_next : std_logic;
  signal occupied_next : std_logic;
  signal address_next : std_logic_vector (8 downto 0);
  signal exits_cuckoo_next : std_logic;
  signal rdy_hash_next : std_logic;
  signal previous_search_next : std_logic;
  signal vld_ad_hash_next : std_logic;
  signal exits_matching_next : std_logic;
  signal acc_deny_hash_next : std_logic;
  signal DEBUG_OK_CNT_next, DEBUG_KO_CNT_next : integer range 0 to 200;
  signal rdy_firewall_hash_read : std_logic;
  signal rdy_hash_read : std_logic;
  signal vld_ad_hash_read : std_logic;
  signal acc_deny_hash_read : std_logic;

  signal DEBUG_crc0 : std_logic_vector(8 downto 0);
  signal DEBUG_crc1 : std_logic_vector(8 downto 0);
  signal DEBUG_BOOL : boolean;
  
  signal DEBUG_decision0 : natural range 0 to 2**16 := 0;
  signal DEBUG_decision1 : natural range 0 to 2**16 := 0;
  signal DEBUG_decision2 : natural range 0 to 2**16 := 0;
  signal DEBUG_decision3 : natural range 0 to 2**16 := 0;
  signal DEBUG_decision4 : natural range 0 to 2**16 := 0;
  signal DEBUG_decision5 : natural range 0 to 2**16 := 0;
  signal DEBUG_decision6 : natural range 0 to 2**16 := 0;
  signal DEBUG_decision7 : natural range 0 to 2**16 := 0;
  
  alias decision_ki : std_logic_vector(7 downto 0) is key_in(7 downto 0);
  alias alias_key_ki : std_logic_vector(codeword_sum -1 +8 downto 7) is key_in(codeword_sum - 1 + 8 downto 7);
  
  
  alias decision_do : std_logic_vector(7 downto 0) is data_out(7 downto 0);
  alias alias_key_do : std_logic_vector(codeword_sum -1 +8 downto 7) is data_out(codeword_sum - 1 + 8 downto 7);

  signal hashing_key : std_logic_vector(codeword_sum -1 downto 0) := (others => '0') ;
  signal decision_out :std_logic_vector(7 downto 0);
  
-- 000000000000000000000000000000010000000000000000000000000000011000000000000000000000000000000011000000000000000000000000000001000000000000000000000000000000010100000001

-- 00000000000000000000000000000001000000000000000000000000000001100000000000000000000000000000001100000000000000000000000000000100000000000000000000000000000001010


  function src_hash (M : std_logic_vector; g : std_logic_vector)
    return std_logic_vector is
    variable crc : std_logic_vector(7 downto 0) := (others => '0');
    type R_array is array (0 to 7) of std_logic;
    variable R : R_array := (others => '0');
    variable connect : std_logic;

  begin
    REST : for i in 0 to codeword_sum - 1 loop
      if (i > codeword_sum - 1) then
        connect := R(7);
      else
        connect := M(i) xor R(7);
      end if;
      for j in 7 downto 1 loop
        if g(j) = '1' then
          R(j) := connect xor R(j - 1);
        else
          R(j) := R(j - 1);
        end if;
      end loop;
      R(0) := connect;
    end loop;
    crc := R(7) & R(6) & R(5) & R(4) & R(3) & R(2) & R(1) & R(0);
    return std_logic_vector(crc);

  end function src_hash;


begin
  decision_ad <= decision_do;
  hashing_key <= key_in(codeword_sum -1 + 8 downto 8);
  rdy_firewall_hash <= rdy_firewall_hash_next;
  rdy_hash <= rdy_hash_next;
  vld_ad_hash <= vld_ad_hash_next;
  acc_deny_hash <= acc_deny_hash_next;

  cuckoo_SRAM_inst : cuckoo_SRAM
  generic map (
    number_of_trees => number_of_trees,
    tree_depth => tree_depth,
    address_width => address_width,
    total_address_width => total_address_width,
    address_width_cumsum => address_width_cumsum,
    largest_address_width => largest_address_width,
    key_in_lengths => key_in_lengths,
    total_key_in_length => total_key_in_length,
    tree_cumsum => tree_cumsum,
    codeword_length => codeword_length,
    largest_codeword => largest_codeword,
    codeword_sum => codeword_sum
  )
  port map(
    clk => clk,
    reset => reset,
    flush_sram => flush_cuckoo_sram,
    occupied => occupied,
    RW => RW,
    address => address_next,
    data_in => data_in,
    data_out => data_out
  );
  STATE_MEMORY_LOGIC : process (clk, reset)
  begin
    if reset = '1' then
      current_state <= command_state;
    elsif rising_edge(clk) then
      current_state <= next_state;
      flush_flag <= flush_flag_next;
      delete_flag <= delete_flag_next;
      insert_flag <= insert_flag_next;
      flush_cuckoo_sram <= flush_cuckoo_sram_next;
      rdy_firewall_hash_read <= rdy_firewall_hash_next;
      flip <= flip_next;
      insertion_key <= insertion_key_next;
      MAX <= MAX_next;
      eq_key <= eq_key_next;
      occupied <= occupied_next;
      address <= address_next;
      rdy_hash_read <= rdy_hash_next;
      previous_search <= previous_search_next;
      vld_ad_hash_read <= vld_ad_hash_next;
      exits_matching <= exits_matching_next;
      acc_deny_hash_read <= acc_deny_hash_next;
      exits_cuckoo <= exits_cuckoo_next;

    end if;
  end process;

  NEXT_STATE_LOGIC : process (current_state, insert_flag_next, set_rule, vld_firewall_hash, exits_cuckoo_next, MAX_next, flip_next, flush_flag_next,
    previous_search_next, exits_matching_next, vld_hdr, rdy_ad_hash, delete_flag_next, eq_key_next)
  begin
    next_state <= current_state;
    case(current_state) is

      when command_state =>
      if flush_flag_next = '1' then
        next_state <= flush_memory;
      elsif delete_flag_next = '1' then
        next_state <= rdy_delete;
      elsif insert_flag_next = '1' then
        next_state <= rdy_key;
      elsif set_rule = '0' then
        next_state <= rdy_hash_matching;
      end if;

      when rdy_key =>
      if insert_flag_next = '0' then
        next_state <= command_state;
      elsif vld_firewall_hash = '1' then
        next_state <= lookup_hash1;
      end if;

      when flush_memory => next_state <= command_state;

      when rdy_hash_matching =>
      if set_rule = '1' then
        next_state <= command_state;
      elsif vld_hdr = '1' then
        next_state <= search_hash1;
      end if;

      when lookup_hash1 => next_state <= is_occupied;

      when is_occupied =>
      if eq_key_next = '1' then
        next_state <= rdy_key;
      elsif exits_cuckoo_next = '1' then
        next_state <= remember_and_replace;
      else
        next_state <= insert_key;
      end if;

      when lookup_hash2 => next_state <= is_occupied;
      when remember_and_replace => if MAX_next = MAX_ITER then
      next_state <= ERROR;
    elsif flip_next = '1' then
      next_state <= lookup_hash1;
    else
      next_state <= lookup_hash2;
    end if;

    when insert_key => next_state <= rdy_key;

    when ERROR => next_state <= ERROR;

    when search_hash1 => next_state <= matching;

    when search_hash2 => next_state <= matching;

    when matching =>
    if previous_search_next = '0' and exits_matching_next = '0' then
      next_state <= search_hash2;
    elsif (exits_matching_next = '1') or (previous_search_next = '1') then
      next_state <= AD_communication;
    end if;

    when AD_communication =>
    if rdy_ad_hash = '1' then
      next_state <= rdy_hash_matching;
    end if;

    when rdy_delete =>
    if delete_flag_next = '0' then
      next_state <= command_state;
    elsif vld_firewall_hash = '1' then
      next_state <= find_hashfun1;
    end if;

    when find_hashfun1 => next_state <= match_for_delete;

    when find_hashfun2 => next_state <= match_for_delete;

    when match_for_delete =>
    if previous_search_next = '0' and exits_matching_next = '0' then
      next_state <= find_hashfun2;
    elsif (exits_matching_next = '1') or (previous_search_next = '1') then
      next_state <= delete_from_memory;
    end if;

    when delete_from_memory => next_state <= rdy_delete;
    when others => next_state <= rdy_hash_matching;

  end case;

end process;

OUTPUT_LOGIC : process (current_state, cmd_in, flush_flag, delete_flag, insert_flag,
  flush_cuckoo_sram, flip, rdy_firewall_hash_read, insertion_key, MAX,
  occupied, address, exits_cuckoo, rdy_hash_read, previous_search,
  vld_ad_hash_read, exits_matching, acc_deny_hash_read,
  eq_key, data_out, header_data, key_in)
begin
  flush_flag_next <= flush_flag;
  delete_flag_next <= delete_flag;
  insert_flag_next <= insert_flag;
  flush_cuckoo_SRAM_next <= flush_cuckoo_sram;
  flip_next <= flip;
  rdy_firewall_hash_next <= rdy_firewall_hash_read;
  insertion_key_next <= insertion_key;
  MAX_next <= MAX;
  eq_key_next <= eq_key;
  address_next <= address;
  exits_cuckoo_next <= exits_cuckoo;
  rdy_hash_next <= rdy_hash_read;
  occupied_next <= occupied;
  vld_ad_hash_next <= vld_ad_hash_read;
  previous_search_next <= previous_search;
  exits_matching_next <= exits_matching;
  acc_deny_hash_next <= acc_deny_hash_read;
  RW <= '0';
  data_in <= (others => '0');

  case(current_state) is
    when command_state =>
    flush_cuckoo_sram_next <= '0';

    case(cmd_in) is
      when "00" => --flush
      flush_flag_next <= '1';
      when "01" => --insert
      insert_flag_next <= '1';
      when "10" => -- delete
      delete_flag_next <= '1';
      when "11" => --hash match
      delete_flag_next <= '0';
      insert_flag_next <= '0';
      flush_flag_next <= '0';
      when others => 

    end case;
    when flush_memory => 
    flush_cuckoo_sram_next <= '1';
    flush_flag_next <= '0';

    when insert_key =>
    RW <= '1';
    data_in <= insertion_key;
    flip_next <= '1';

    when rdy_key =>
    if not (cmd_in = "01") then
      insert_flag_next <= '0';
    end if;
    rdy_firewall_hash_next <= '1';
    insertion_key_next <= key_in;
    MAX_next <= 0;
    eq_key_next <= '0';
    occupied_next <= '1';

    when lookup_hash1 =>
    rdy_firewall_hash_next <= '0';
    RW <= '0';
    -- DEBUG_crc0 <= src_hash(insertion_key(codeword_sum -1 + 8 downto 7), g1);
    DEBUG_crc0 <= '0' & src_hash(hashing_key, g1);

    -- address_next <= '0' & src_hash(insertion_key(codeword_sum -1 downto 0), g1);
    address_next <= '0' & src_hash(hashing_key, g1);
    report "address_next = " & integer'image(to_integer(unsigned(address_next)));
   -- Find ud af hvor src ikke er korrekt
    

    when lookup_hash2 =>
    RW <= '0';
    address_next <= src_hash(hashing_key, g2) + "100000000";
    
    when is_occupied =>
    if data_out(codeword_sum - 1 downto 0) = insertion_key then
      eq_key_next <= '1';
    elsif data_out(data_out'left) = '1' then
      exits_cuckoo_next <= '1';
    else
      exits_cuckoo_next <= '0';
    end if;

    when remember_and_replace =>
    RW <= '1';
    data_in <= insertion_key;
    insertion_key_next <= data_out(codeword_sum - 1 + 8 downto 0);
    MAX_next <= MAX + 1;
    if flip = '1' then
      flip_next <= '0';
    else
      flip_next <= '1';
    end if;

    when ERROR =>

    when rdy_hash_matching =>
    rdy_hash_next <= '1';
    previous_search_next <= '0';
    vld_ad_hash_next <= '0';
    when search_hash1 =>
    rdy_hash_next <= '0';
    RW <= '0';
    address_next <= '0' & src_hash(header_data, g1);
    when search_hash2 =>
    RW <= '0';
    address_next <= src_hash(header_data, g2) + "100000000";
    previous_search_next <= '1';

    when matching =>
    DEBUG_BOOL <= data_out(codeword_sum - 1 +8 downto 8) = header_data;
    if data_out(codeword_sum - 1 +8 downto 8) = header_data then
      exits_matching_next <= '1';
      acc_deny_hash_next <= '0';
      decision_out <= data_out(7 downto 0);
    else
      if previous_search = '1' then
        acc_deny_hash_next <= '1';
      end if;
      exits_matching_next <= '0';
    end if;

    when AD_communication =>
    vld_ad_hash_next <= '1';
    when rdy_delete =>
    if not (cmd_in = "10") then
      delete_flag_next <= '0';
    end if;
    rdy_firewall_hash_next <= '1';
    previous_search_next <= '0';
    RW <= '0';
    occupied_next <= '0';
    



    when find_hashfun1 =>
    rdy_firewall_hash_next <= '0';
    --rdy_hash_next <= '0';
    RW <= '0';
    -- address_next <= '0' & src_hash(key_in(codeword_sum -1 downto 0), g1);
    address_next <= '0' & src_hash(hashing_key, g1);
    when find_hashfun2 =>
    RW <= '0';
    -- address_next <= src_hash(key_in(codeword_sum -1 downto 0), g2) + "100000000";
    address_next <= src_hash(hashing_key, g2) + "100000000";
    previous_search_next <= '1';
    when match_for_delete =>
    if data_out(codeword_sum - 1 downto 0) = key_in then
      exits_matching_next <= '1';
    else
      if previous_search = '1' then
      end if;
      exits_matching_next <= '0';
    end if;

    when delete_from_memory =>
    RW <= '1';
    data_in <= (others => '0');

    when others => report "ERROR IN OUTPUT LOGIC" severity failure;

  end case;

end process;

process (vld_ad_hash_next)
  begin
    if vld_ad_hash_next = '1' then
      case decision_do is
        when "00000000" => DEBUG_decision0<=DEBUG_decision0+1;
        when "00000001" => DEBUG_decision1<=DEBUG_decision1+1;
        when "00000010" => DEBUG_decision2<=DEBUG_decision2+1;
        when "00000011" => DEBUG_decision3<=DEBUG_decision3+1;
        when "00000100" => DEBUG_decision4<=DEBUG_decision4+1;
        when "00000101" => DEBUG_decision5<=DEBUG_decision5+1;
        when "00000110" => DEBUG_decision6<=DEBUG_decision6+1;
        when "00000111" => DEBUG_decision7<=DEBUG_decision7+1;
        when others =>
          null;
      end case;
    end if;
end process;

end architecture; -- Cuckoo_Hashing