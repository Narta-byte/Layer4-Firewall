library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;
use ieee.math_real.all;
use work.my_types_pkg.all;



entity system_blueprint is
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
    cmd_in : in std_logic_vector(4 downto 0);

    key_in : in std_logic_vector(total_key_in_length - 1 downto 0);
    codeword_in : in std_logic_vector(largest_codeword - 1 downto 0);
    zero_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);
    one_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);


    rdy_driver : out std_logic;
    vld_driver : in std_logic;

    rdy_collect_header : out std_logic_vector(number_of_trees - 1 downto 0);
    vld_collect_header : in std_logic_vector(number_of_trees -1 downto 0);

    cuckoo_key_in : in std_logic_vector(codeword_sum - 1 downto 0);
    
    -- rdy_cuckoo_hash : in std_logic;
    -- vld_cuckoo_hash : out std_logic;
    SoP : in std_logic;
    Eop : in std_logic;
    CH_vld : in std_logic;
    packet_in : in std_logic_vector(10 downto 0);

    clk : in std_logic;
    reset : in std_logic
  );
end;

architecture rtl of system_blueprint is

  component tree_collection
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
      largest_codeword : integer
    );
      port (
      key_in : in std_logic_vector(total_key_in_length - 1 downto 0);
      codeword_in : in std_logic_vector(largest_codeword - 1 downto 0);
      zero_pointer : in std_logic_vector(largest_address_width - 1 downto 0);
      one_pointer : in std_logic_vector(largest_address_width - 1 downto 0);
      address : in std_logic_vector(largest_address_width - 1 downto 0);
      RW : in std_logic_vector(number_of_trees - 1 downto 0);
      rdy_collect_header : out std_logic_vector(number_of_trees - 1 downto 0);
      vld_collect_header : in std_logic_vector(number_of_trees -1 downto 0);
      codeword_out : out std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
      cuckoo_codeword : out std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
      rdy_cuckoo_hash : in std_logic;
      vld_cuckoo_hash : out std_logic;
      clk : in std_logic;
      reset : in std_logic
    );
  end component;
  
  component rule_engine
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
      cmd_in : in std_logic_vector(4 downto 0);
      codeword_in : in std_logic_vector(largest_codeword - 1 downto 0);
      zero_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);
      one_pointer_in : in std_logic_vector(largest_address_width - 1 downto 0);
      codeword_out : out std_logic_vector(largest_codeword - 1 downto 0);
      zero_pointer_out : out std_logic_vector(largest_address_width - 1 downto 0);
      one_pointer_out : out std_logic_vector(largest_address_width - 1 downto 0);
      RW : out std_logic_vector(number_of_trees - 1 downto 0);
      address : out std_logic_vector(largest_address_width - 1 downto 0);
      rdy_driver : out std_logic;
      vld_driver : in std_logic;
      cuckoo_select : out std_logic;
      cuckoo_cmd : out std_logic_vector(1 downto 0);
      cuckoo_key_out : out std_logic_vector(codeword_sum - 1 downto 0);
      cuckoo_key_in : in std_logic_vector(codeword_sum - 1 downto 0);
      cuckoo_rdy : in std_logic;
      cuckoo_vld : out std_logic;
      cuckoo_set_rule : out std_logic;
      clk : in std_logic;
      reset : in std_logic
    );
  end component;
  component Cuckoo_Hashing
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
      key_in : in std_logic_vector(codeword_sum - 1 downto 0);
      header_data : in std_logic_vector(codeword_sum - 1 downto 0);
      vld_hdr : in std_logic;
      rdy_hash : out std_logic;
      vld_firewall_hash : in std_logic;
      rdy_firewall_hash : out std_logic;
      acc_deny_hash : out std_logic;
      vld_ad_hash : out std_logic;
      rdy_ad_hash : in std_logic
    );
  end component;
  component Collect_header
    generic (
      size : integer
    );
      port (
      clk : in std_logic;
      reset : in std_logic;
      fileinput : in std_logic_vector(size downto 0);
      packet_in : in std_logic_vector(10 downto 0);
      SoP : in std_logic;
      EoP : in std_logic;
      CH_vld : in std_logic;
      vld_firewall : in std_logic;
      rdy_FIFO : in std_logic;
      rdy_hash : in std_logic;
      rdy_collecthdr : out std_logic;
      vld_hdr : out std_logic;
      vld_hdr_FIFO : out std_logic;
      hdr_SoP : out std_logic;
      hdr_EoP : out std_logic;
      packet_forward : out std_logic_vector(10 downto 0);
      ip_version : out std_logic_vector(3 downto 0);
      ip_header_len : out std_logic_vector(3 downto 0);
      ip_TOS : out std_logic_vector (7 downto 0);
      ip_total_len : out std_logic_vector(15 downto 0);
      ip_ID : out std_logic_vector(15 downto 0);
      ip_flags : out std_logic_vector(2 downto 0);
      ip_fragmt_offst : out std_logic_vector(12 downto 0);
      ip_ttl : out std_logic_vector(7 downto 0);
      ip_protocol : out std_logic_vector(7 downto 0);
      ip_checksum : out std_logic_vector(15 downto 0);
      ip_src_addr : out std_logic_vector(31 downto 0);
      ip_dest_addr : out std_logic_vector(31 downto 0);
      src_port : out std_logic_vector(15 downto 0);
      dest_port : out std_logic_vector(15 downto 0);
      tcp_seq_num : out std_logic_vector(31 downto 0);
      tcp_ack_num : out std_logic_vector(31 downto 0);
      tcp_data_offset : out std_logic_vector(3 downto 0);
      tcp_reserved : out std_logic_vector(2 downto 0);
      tcp_flags : out std_logic_vector(8 downto 0);
      tcp_window_size : out std_logic_vector(15 downto 0);
      L4checksum : out std_logic_vector(15 downto 0);
      tcp_urgent_ptr : out std_logic_vector(15 downto 0);
      collect_header_key_out_to_tree_collection : out std_logic_vector(103 downto 0);
      vld_collect_header : out std_logic_vector(4 downto 0);
      udp_len : out std_logic_vector(15 downto 0)
    );
  end component;

  component Accept_Deny
    port (
    clk : in std_logic;
    reset : in std_logic;
    data_firewall : out std_logic_vector(10 downto 0);
    ok_cnt : out std_logic_vector(7 downto 0);
    ko_cnt : out std_logic_vector(7 downto 0);
    packet_forward_FIFO : in std_logic_vector(10 downto 0);
    vld_fifo : in std_logic;
    rdy_ad_FIFO : out std_logic;
    acc_deny_hash : in std_logic;
    vld_ad_hash : in std_logic;
    rdy_ad_hash : out std_logic
  );
end component;
component packet_fifo
  port (
  clock : in STD_LOGIC;
  data : in STD_LOGIC_VECTOR (10 DOWNTO 0);
  rdreq : in STD_LOGIC;
  wrreq : in STD_LOGIC;
  empty : out STD_LOGIC;
  full : out STD_LOGIC;
  q : out STD_LOGIC_VECTOR (10 DOWNTO 0);
  usedw : out STD_LOGIC_VECTOR (7 DOWNTO 0)
);
end component;

  constant size : integer := 10000;

  signal fileinput : std_logic_vector(size downto 0);

  signal vld_firewall : std_logic;
  signal rdy_FIFO : std_logic:='1';
  -- signal rdy_hash : std_logic;
  signal rdy_collecthdr : std_logic;
  -- signal vld_hdr : std_logic;
  signal vld_hdr_FIFO : std_logic:='0';
  signal hdr_SoP : std_logic;
  signal hdr_EoP : std_logic;
  signal packet_forward : std_logic_vector(10 downto 0);
  signal ip_version : std_logic_vector(3 downto 0);
  signal ip_header_len : std_logic_vector(3 downto 0);
  signal ip_TOS : std_logic_vector (7 downto 0);
  signal ip_total_len : std_logic_vector(15 downto 0);
  signal ip_ID : std_logic_vector(15 downto 0);
  signal ip_flags : std_logic_vector(2 downto 0);
  signal ip_fragmt_offst : std_logic_vector(12 downto 0);
  signal ip_ttl : std_logic_vector(7 downto 0);
  signal ip_protocol : std_logic_vector(7 downto 0);
  signal ip_checksum : std_logic_vector(15 downto 0);
  signal ip_src_addr : std_logic_vector(31 downto 0);
  signal ip_dest_addr : std_logic_vector(31 downto 0);
  signal src_port : std_logic_vector(15 downto 0);
  signal dest_port : std_logic_vector(15 downto 0);
  signal tcp_seq_num : std_logic_vector(31 downto 0);
  signal tcp_ack_num : std_logic_vector(31 downto 0);
  signal tcp_data_offset : std_logic_vector(3 downto 0);
  signal tcp_reserved : std_logic_vector(2 downto 0);
  signal tcp_flags : std_logic_vector(8 downto 0);
  signal tcp_window_size : std_logic_vector(15 downto 0);
  signal L4checksum : std_logic_vector(15 downto 0);
  signal tcp_urgent_ptr : std_logic_vector(15 downto 0);
  signal udp_len : std_logic_vector(15 downto 0);

  signal collect_header_key_out_to_tree_collection : std_logic_vector(103 downto 0);
  signal vld_collect_header_wire : std_logic_vector(4 downto 0);

  signal set_rule : std_logic;
  signal header_data : std_logic_vector(codeword_sum - 1 downto 0);
  signal vld_hdr : std_logic;
  signal rdy_hash : std_logic;
  signal vld_firewall_hash : std_logic;
  signal rdy_firewall_hash : std_logic;
  signal acc_deny_hash : std_logic;
  signal vld_ad_hash : std_logic;
  signal rdy_ad_hash : std_logic;

  signal address : std_logic_vector(largest_address_width - 1 downto 0);
  signal RW : std_logic_vector(number_of_trees - 1 downto 0);

  signal codeword_out : std_logic_vector(largest_codeword - 1 downto 0);
  signal zero_pointer_out : std_logic_vector(largest_address_width - 1 downto 0);
  signal one_pointer_out : std_logic_vector(largest_address_width - 1 downto 0);

  signal codeword_to_concat : std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);

  signal cuckoo_codeword : std_logic_vector(largest_codeword * number_of_trees - 1 downto 0);
  signal cuckoo_select : std_logic;
  signal cuckoo_cmd : std_logic_vector(1 downto 0);
  signal cuckoo_key_out: std_logic_vector(codeword_sum - 1 downto 0);
  signal rule_cuckoo_rdy : std_logic;
  signal rule_cuckoo_vld : std_logic;


  signal trees_to_cuckoo_hash_vld : std_logic;
  signal trees_to_cuckoo_hash_rdy : std_logic;

  signal data_firewall : std_logic_vector(10 downto 0);
  signal ok_cnt : std_logic_vector(7 downto 0);
  signal ko_cnt : std_logic_vector(7 downto 0);
  signal packet_forward_FIFO : std_logic_vector(10 downto 0);
  signal vld_fifo : std_logic;
  signal rdy_ad_FIFO : std_logic := '0';

  signal data : STD_LOGIC_VECTOR (10 DOWNTO 0);
  signal rdreq : STD_LOGIC;
  signal wrreq : STD_LOGIC := '0';
  signal empty : STD_LOGIC;
  signal full : STD_LOGIC;
  signal q : STD_LOGIC_VECTOR (10 DOWNTO 0);
  signal usedw : STD_LOGIC_VECTOR (7 DOWNTO 0);



begin

  rule_engine_inst : rule_engine
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
    port map (
      cmd_in => cmd_in,
      codeword_in => codeword_in,
      zero_pointer_in => zero_pointer_in,
      one_pointer_in => one_pointer_in,
      codeword_out => codeword_out,
      zero_pointer_out => zero_pointer_out,
      one_pointer_out => one_pointer_out,
      RW => RW,
      address => address,
      rdy_driver => rdy_driver,
      vld_driver => vld_driver,
      cuckoo_select => cuckoo_select,
      cuckoo_cmd => cuckoo_cmd,
      cuckoo_key_out => cuckoo_key_out,
      cuckoo_key_in => cuckoo_key_in,
      cuckoo_rdy => rule_cuckoo_rdy,
      cuckoo_vld => rule_cuckoo_vld,
      cuckoo_set_rule => set_rule,
      clk => clk,
      reset => reset
    );
  tree_collection_inst : tree_collection
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
    largest_codeword => largest_codeword
  )
  port map (
    key_in => collect_header_key_out_to_tree_collection,
    codeword_in => codeword_out,
    zero_pointer => zero_pointer_out,
    one_pointer => one_pointer_out,
    address => address,
    RW => RW,
    rdy_collect_header => rdy_collect_header,
    vld_collect_header => vld_collect_header_wire,
    codeword_out => codeword_to_concat,
    cuckoo_codeword => cuckoo_codeword,
    rdy_cuckoo_hash => trees_to_cuckoo_hash_rdy,
    vld_cuckoo_hash => trees_to_cuckoo_hash_vld,
    clk => clk,
    reset => reset
  );
  Cuckoo_Hashing_inst : Cuckoo_Hashing
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
    port map (
      clk => clk,
      reset => reset,
      set_rule => set_rule,
      cmd_in => cuckoo_cmd,
      key_in => cuckoo_key_out,
      header_data => codeword_to_concat, -- change the name to something like codeword out
      vld_hdr => trees_to_cuckoo_hash_vld, 
      rdy_hash => trees_to_cuckoo_hash_rdy, --rdy_hash,
      vld_firewall_hash => rule_cuckoo_vld,
      rdy_firewall_hash => rule_cuckoo_rdy,
      acc_deny_hash => acc_deny_hash,
      vld_ad_hash => vld_ad_hash,
      rdy_ad_hash => rdy_ad_hash
    );
    Collect_header_inst : Collect_header
    generic map (
      size => size
    )
    port map (
      clk => clk,
      reset => reset,
      fileinput => fileinput,
      packet_in => packet_in,
      SoP => SoP,
      EoP => EoP,
      CH_vld => CH_vld,
      vld_firewall => vld_firewall,
      rdy_FIFO => rdy_FIFO,
      rdy_hash => rdy_hash,
      rdy_collecthdr => rdy_collecthdr,
      vld_hdr => vld_hdr,
      vld_hdr_FIFO => vld_hdr_FIFO,
      hdr_SoP => hdr_SoP,
      hdr_EoP => hdr_EoP,
      packet_forward => packet_forward,
      ip_version => ip_version,
      ip_header_len => ip_header_len,
      ip_TOS => ip_TOS,
      ip_total_len => ip_total_len,
      ip_ID => ip_ID,
      ip_flags => ip_flags,
      ip_fragmt_offst => ip_fragmt_offst,
      ip_ttl => ip_ttl,
      ip_protocol => ip_protocol,
      ip_checksum => ip_checksum,
      ip_src_addr => ip_src_addr,
      ip_dest_addr => ip_dest_addr,
      src_port => src_port,
      dest_port => dest_port,
      tcp_seq_num => tcp_seq_num,
      tcp_ack_num => tcp_ack_num,
      tcp_data_offset => tcp_data_offset,
      tcp_reserved => tcp_reserved,
      tcp_flags => tcp_flags,
      tcp_window_size => tcp_window_size,
      L4checksum => L4checksum,
      tcp_urgent_ptr => tcp_urgent_ptr,
      collect_header_key_out_to_tree_collection => collect_header_key_out_to_tree_collection,
      vld_collect_header => vld_collect_header_wire,
      udp_len => udp_len
    );

    Accept_Deny_inst : Accept_Deny
    port map (
      clk => clk,
      reset => reset,
      data_firewall => data_firewall,
      ok_cnt => ok_cnt,
      ko_cnt => ko_cnt,
      packet_forward_FIFO => packet_forward_FIFO,
      vld_fifo => vld_fifo,
      rdy_ad_FIFO => rdy_ad_FIFO,
      acc_deny_hash => acc_deny_hash,
      vld_ad_hash => vld_ad_hash,
      rdy_ad_hash => rdy_ad_hash
    );
    packet_fifo_inst : packet_fifo
    port map (
      clock => clk,
      data => packet_forward,
      rdreq => rdreq,
      wrreq => wrreq,
      empty => empty,
      full => full,
      q => packet_forward_FIFO,
      usedw => usedw
    );

    -- rdreq <= rdy_ad_FIFO and (not empty);
    -- wrreq <= vld_hdr_FIFO and (not full);
    -- rdy_FIFO <= '1'

    vld_fifo <= not full;
    rdreq <= rdy_ad_FIFO and (not empty);
    wrreq <= vld_hdr_FIFO and (not full);
    rdy_collecthdr <= not full;
    data <= packet_forward;
end;
