library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;
use ieee.std_logic_misc.and_reduce;
use IEEE.std_logic_textio.all;


entity Collect_header is
  generic (
    size : integer := 10000 --max size of a line/length of a packet
  );
  
  port (
    clk : in std_logic;
    reset : in std_logic;
    fileinput : in std_logic_vector(size downto 0);
    
    packet_in       : in std_logic_vector(10 downto 0);
    SoP             : in std_logic;
    EoP             : in std_logic;
    CH_vld          : in std_logic;
    vld_firewall    : in std_logic;
    rdy_FIFO        : in std_logic;
    rdy_hash        : in std_logic;
    
    rdy_collecthdr  : out std_logic;
    vld_hdr         : out std_logic;
    vld_hdr_FIFO    : out std_logic:='1';
    hdr_SoP         : out std_logic;
    hdr_EoP         : out std_logic;
    
    packet_forward  : out std_logic_vector(10 downto 0);
    
    ip_version      : out std_logic_vector(3 downto 0);   -- Bits 0-3, IP version
    ip_header_len   : out std_logic_vector(3 downto 0);   -- Bits 4-7, IP header length
    ip_TOS          : out std_logic_vector (7 downto 0);  -- Bits 8-15, Type of Service
    ip_total_len    : out std_logic_vector(15 downto 0);  -- Bits 16-31, Total length
    ip_ID           : out std_logic_vector(15 downto 0);  -- Bits 32-47, Identification
    ip_flags        : out std_logic_vector(2 downto 0);   -- Bits 48-50, Flags
    ip_fragmt_offst : out std_logic_vector(12 downto 0);  -- Bits 51-63, Fragment offset
    ip_ttl          : out std_logic_vector(7 downto 0);   -- Bits 64-71, Time to live
    ip_protocol     : out std_logic_vector(7 downto 0);   -- Bits 72-79, Protocol
    ip_checksum     : out std_logic_vector(15 downto 0);  -- Bits 80-95, Header checksum
    ip_src_addr     : out std_logic_vector(31 downto 0);  -- Bits 96-127, Source IP address
    ip_dest_addr    : out std_logic_vector(31 downto 0);  -- Bits 128-159, Destination IP address

    src_port        : out std_logic_vector(15 downto 0);  -- Bits 0-15, Source port
    dest_port       : out std_logic_vector(15 downto 0);  -- Bits 16-31, Destination port

    tcp_seq_num     : out std_logic_vector(31 downto 0);  -- Bits 32-63, Sequence number
    tcp_ack_num     : out std_logic_vector(31 downto 0);  -- Bits 64-95, Acknowledgment number
    tcp_data_offset : out std_logic_vector(3 downto 0);   -- Bits 96-99, Data offset (header length)
    tcp_reserved    : out std_logic_vector(2 downto 0);   -- Bits 3
    tcp_flags       : out std_logic_vector(8 downto 0);   -- Bits 100-107, Flags (URG, ACK, PSH, RST, SYN, FIN)
    tcp_window_size : out std_logic_vector(15 downto 0);  -- Bits 108-123, Window size
    L4checksum      : out std_logic_vector(15 downto 0);  -- Bits 124-139, Checksum
    tcp_urgent_ptr  : out std_logic_vector(15 downto 0);  -- Bits 140-155, Urgent pointer

    collect_header_key_out_to_tree_collection : out std_logic_vector(103 downto 0);
    vld_collect_header : out std_logic_vector(4 downto 0);
    rdy_collecthdr_to_tree_collection : in std_logic_vector(4 downto 0);
    udp_len         : out std_logic_vector(15 downto 0)

    );

end entity;

architecture arch_Collect_header of Collect_header is
  signal bytenum    : integer range 0 to 100000 := 0;
  signal storebyte  : std_logic_vector(7 downto 0) :=(others => '0');
  signal storebyte2 : std_logic_vector(7 downto 0) :=(others => '0');
  signal storebyte3 : std_logic_vector(7 downto 0) :=(others => '0');
  signal tcp_flag   : std_logic := '0';
  signal udp_flag   : std_logic := '0';
  signal wait_start : std_logic := '0';
  signal vld_collect_header_reg : std_logic_vector(4 downto 0) := (others => '0');
  signal sig_collect_header_key_out_to_tree_collection : std_logic_vector(103 downto 0) := (others => '0');
  signal CH_key_sent : std_logic := '0';
  signal debug_bool : boolean := false;

  constant lenpack : integer := 10;
  constant zpack : integer := lenpack -7;
  
  signal i, number_of_packets : integer := 0;
  signal lock, go : std_logic := '0';
begin

  vld_collect_header <= vld_collect_header_reg;

  -- packet_to_fifo : process (rdy_FIFO)
  -- begin
  --   if rdy_FIFO = '1' then
  --     packet_forward <= packet_in;
  --   else
  --     packet_forward <= (others => '0');
  --   end if;
  -- end process;

  packet_forward <= packet_in;
  collect_header_key_out_to_tree_collection <= sig_collect_header_key_out_to_tree_collection;
  
  process (clk)
    file input0 : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/hardware/sim/blueprint/protocol.txt";
    variable protocol_line : line;
    variable protocol_reader : std_logic_vector(7 downto 0);

    file input1 : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/hardware/sim/blueprint/dstport.txt";
    variable dstport_line : line;
    variable dstport_reader : std_logic_vector(15 downto 0);

    file input2 : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/hardware/sim/blueprint/srcport.txt";
    variable srcport_line : line;
    variable srcport_reader : std_logic_vector(15 downto 0);
    
    file input4 : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/hardware/sim/blueprint/srcip.txt";
    variable srcip_line : line;
    variable srcip_reader : std_logic_vector(31 downto 0);

    file input3 : TEXT open READ_MODE is "C:/Users/Mig/Desktop/Layer4-Firewall/hardware/sim/blueprint/dstip.txt";
    variable dstip_line : line;
    variable dstip_reader : std_logic_vector(31 downto 0);

    
  begin
    if rising_edge(clk) and CH_vld = '1' then

      
      i <= i + 1;
      -- if rdy_collecthdr_to_tree_collection(0) = '1' and vld_collect_header_reg(0) <= '1' then
      --   if not ENDFILE(input0) then
      --     readline(input0, protocol_line);
      --     hread(protocol_line, protocol_reader);
  
      --     sig_collect_header_key_out_to_tree_collection(103 downto 96) <= protocol_reader(7 downto 0);

      --   end if;

      --   vld_collect_header_reg(0) <= '0';
      -- end if;

      -- if rdy_collecthdr_to_tree_collection(1) = '1' and vld_collect_header_reg(1) <= '1' then
      --   if not ENDFILE(input2) then

      --     readline(input2, srcport_line);
      --     hread(srcport_line, srcport_reader);

      --     sig_collect_header_key_out_to_tree_collection(95 downto 80) <= srcport_reader(15 downto 0); 
      --   end if;

      --   vld_collect_header_reg(1) <= '0';
      -- end if;

      -- if rdy_collecthdr_to_tree_collection(2) = '1' and vld_collect_header_reg(2) <= '1' then

      --   if not ENDFILE(input1) then
          
      --     readline(input1, dstport_line);
      --     hread(dstport_line, dstport_reader);
  
      --     sig_collect_header_key_out_to_tree_collection(79 downto 64) <= dstport_reader(15 downto 0);

      --   end if;


      --   vld_collect_header_reg(2) <= '0';
      -- end if;

      -- if rdy_collecthdr_to_tree_collection(3) = '1' and vld_collect_header_reg(3) <= '1' then
      --   if not ENDFILE(input4) then
      --     readline(input4, srcip_line);
      --     hread(srcip_line, srcip_reader);
  
      --     sig_collect_header_key_out_to_tree_collection(63 downto 32) <= srcip_reader(31 downto 0);

      --   end if;

      --   vld_collect_header_reg(3) <= '0';
      -- end if;
      -- -- MANGLER AT MAN IKKE TÆLLER DOPPELT 

      -- if rdy_collecthdr_to_tree_collection(4) = '1' and vld_collect_header_reg(4) <= '1' then
      --   if not ENDFILE(input3) then
      --     readline(input3, dstip_line);
      --     hread(dstip_line, dstip_reader);

      --     sig_collect_header_key_out_to_tree_collection(31 downto 0) <= dstip_reader(31 downto 0);
      --   end if;
      --   vld_collect_header_reg(4) <= '0';
      -- end if;
      -- if rdy_collecthdr_to_tree_collection = "11111" then
      --   vld_collect_header_reg <= (others => '1');
      -- end if;


      if go = '1' and lock = '0' then --
        lock <= '1';
        -- vld_collect_header_reg <= (others => '0');
        number_of_packets <= number_of_packets + 1;
        if not ENDFILE(input0) then
              readline(input0, protocol_line);
              hread(protocol_line, protocol_reader);
      
              sig_collect_header_key_out_to_tree_collection(103 downto 96) <= protocol_reader(7 downto 0);
    
            end if;
            if not ENDFILE(input2) then

              readline(input2, srcport_line);
              hread(srcport_line, srcport_reader);
    
              sig_collect_header_key_out_to_tree_collection(95 downto 80) <= srcport_reader(15 downto 0); 
            end if;
            if not ENDFILE(input1) then
          
              readline(input1, dstport_line);
              hread(dstport_line, dstport_reader);
      
              sig_collect_header_key_out_to_tree_collection(79 downto 64) <= dstport_reader(15 downto 0);
    
            end if;
            if not ENDFILE(input4) then
              readline(input4, srcip_line);
              hread(srcip_line, srcip_reader);
      
              sig_collect_header_key_out_to_tree_collection(63 downto 32) <= srcip_reader(31 downto 0);
    
            end if;
            if not ENDFILE(input3) then
              readline(input3, dstip_line);
              hread(dstip_line, dstip_reader);
    
              sig_collect_header_key_out_to_tree_collection(31 downto 0) <= dstip_reader(31 downto 0);
            end if;
            
            
          end if;
          if lock ='1' then
            lock <= '0';
          end if;
          -- if rdy_collecthdr_to_tree_collection = "00000" then --maybe nor gate
          --   lock <= '0';
          -- end if;
        


        if rdy_collecthdr_to_tree_collection = "11111" then
          vld_collect_header_reg <= (others => '1');
          go <= '1';
        else 
          vld_collect_header_reg <= (others => '0');
          go <= '0';
        end if;

        debug_bool <= rdy_collecthdr_to_tree_collection = "11111"; --find ud af vld logic
      -- debug_bool <=  rdy_collecthdr_to_tree_collection = "11111" and vld_collect_header_reg = "00000";
      -- if rdy_collecthdr_to_tree_collection = "11111" and vld_collect_header_reg = "00000" then
      --   vld_collect_header_reg <= (others => '1');
      -- end if;


    --   for j in 0 to 4 loop
    --     if rdy_collecthdr_to_tree_collection(j) = '1' then
    --       readline(packet_file, current_read_line2);

    --     end if;
    -- end loop;
      


    end if;
  end process;


    



end architecture;