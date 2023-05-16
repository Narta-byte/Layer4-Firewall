library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

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
  

  constant lenpack : integer := 10;
  constant zpack : integer := lenpack -7;
  

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
  logic_proc : process (clk, bytenum, CH_vld, SoP, packet_in, vld_collect_header_reg, CH_key_sent)
  begin
    if rising_edge(clk) then

      if reset = '1' then -- RESET
        ip_version      <= (others => '0');
        ip_header_len   <= (others => '0');
        ip_TOS          <= (others => '0');
        ip_total_len    <= (others => '0');
        ip_ID           <= (others => '0');
        ip_flags        <= (others => '0');
        ip_fragmt_offst <= (others => '0');
        ip_ttl          <= (others => '0');
        ip_protocol     <= (others => '0');
        ip_checksum     <= (others => '0');
        ip_src_addr     <= (others => '0');
        ip_dest_addr    <= (others => '0');
        src_port        <= (others => '0');
        dest_port       <= (others => '0');

        tcp_seq_num     <= (others => '0');
        tcp_ack_num     <= (others => '0');
        tcp_data_offset <= (others => '0');
        tcp_reserved    <= (others => '0');
        tcp_flags       <= (others => '0');
        tcp_window_size <= (others => '0');
        L4checksum      <= (others => '0');
        tcp_urgent_ptr  <= (others => '0');

        udp_len         <= (others => '0');

        tcp_flag <= '0';
        udp_flag <= '0';
        collect_header_key_out_to_tree_collection <= (others => '0');

      else -- IF RESET = '0'
        if wait_start <= '0' then
          bytenum <= 0;
        else
          if CH_vld <= '1' then
            bytenum <= bytenum +1;
            -- packet_forward <= packet_in;
          end if;
          if vld_collect_header_reg = "11111" and CH_key_sent = '0' then
            collect_header_key_out_to_tree_collection <= sig_collect_header_key_out_to_tree_collection;
            CH_key_sent <= '1';
          end if;
        end if;
        if EoP = '1' then
          wait_start <= '1';
          
        end if;
        if SoP = '1' then
          bytenum <= 0;
          ip_version      <= (others => '0');
          ip_header_len   <= (others => '0');
          ip_TOS          <= (others => '0');
          ip_total_len    <= (others => '0');
          ip_ID           <= (others => '0');
          ip_flags        <= (others => '0');
          ip_fragmt_offst <= (others => '0');
          ip_ttl          <= (others => '0');
          ip_protocol     <= (others => '0');
          ip_checksum     <= (others => '0');
          ip_src_addr     <= (others => '0');
          ip_dest_addr    <= (others => '0');
          src_port        <= (others => '0');
          dest_port       <= (others => '0');
  
          tcp_seq_num     <= (others => '0');
          tcp_ack_num     <= (others => '0');
          tcp_data_offset <= (others => '0');
          tcp_reserved    <= (others => '0');
          tcp_flags       <= (others => '0');
          tcp_window_size <= (others => '0');
          L4checksum      <= (others => '0');
          tcp_urgent_ptr  <= (others => '0');
          tcp_flag   <= '0';
          udp_flag   <= '0';
          collect_header_key_out_to_tree_collection <= (others => '0');
          sig_collect_header_key_out_to_tree_collection <= (others => '0');
          vld_collect_header_reg <= (others => '0');
          CH_key_sent <= '0';
        end if;


        case bytenum is
          when 0 =>
            ip_version                  <= packet_in(lenpack downto 7);
            ip_header_len               <= packet_in(5 downto 2);
          when 1 =>   ip_TOS            <= packet_in(lenpack downto zpack);
          when 2 =>   storebyte         <= packet_in(lenpack downto zpack);
          when 3 =>   ip_total_len      <= storebyte & packet_in(lenpack downto zpack);
          when 4 =>   storebyte         <= packet_in(lenpack downto zpack);
          when 5 =>   ip_ID             <= storebyte & packet_in(lenpack downto zpack);
          when 6 =>
            ip_flags                    <= packet_in(lenpack downto 8);
            storebyte                   <= packet_in(7 downto 3) & "000";
          when 7 => ip_fragmt_offst     <= storebyte(7 downto 3) & packet_in(lenpack downto zpack);
          when 8 => ip_ttl              <= packet_in(lenpack downto zpack);
          when 9 => ip_protocol         <= packet_in(lenpack downto zpack);
          sig_collect_header_key_out_to_tree_collection(103 downto 96) <= packet_in(lenpack downto zpack);
          vld_collect_header_reg(4 downto 4)<= "1";
          case packet_in(lenpack downto zpack) is -- ADD CASES FOR DIFFERENT PROTOCOLS
            when x"06" => tcp_flag<= '1';
            when x"11" => udp_flag<= '1';
            when others => null;
          end case;
          when 10 =>    storebyte       <= packet_in(lenpack downto zpack);
          when 11 =>    ip_checksum     <= storebyte & packet_in(lenpack downto zpack);
          when 12 =>    storebyte       <= packet_in(lenpack downto zpack);
          when 13 =>    storebyte2      <= packet_in(lenpack downto zpack);
          when 14 =>    storebyte3      <= packet_in(lenpack downto zpack);
          when 15 =>    ip_src_addr     <= storebyte & storebyte2 & storebyte3 & packet_in(lenpack downto zpack);
          sig_collect_header_key_out_to_tree_collection(95 downto 64) <= storebyte & storebyte2 & storebyte3 & packet_in(lenpack downto zpack);
          vld_collect_header_reg(3 downto 3)<= "1";
          when 16 =>    storebyte       <= packet_in(lenpack downto zpack);
          when 17 =>    storebyte2      <= packet_in(lenpack downto zpack);
          when 18 =>    storebyte3      <= packet_in(lenpack downto zpack);
          when 19 =>    ip_dest_addr    <= storebyte & storebyte2 & storebyte3 & packet_in(lenpack downto zpack);
          sig_collect_header_key_out_to_tree_collection(63 downto 32) <= storebyte & storebyte2 & storebyte3 & packet_in(lenpack downto zpack);
          vld_collect_header_reg(2 downto 2)<= "1";
          when others =>  null;
        end case;
    
        if tcp_flag <= '0' then
        else
          case bytenum is
            when 20 =>  storebyte       <= packet_in(lenpack downto zpack);
            when 21 =>  src_port        <= storebyte & packet_in(lenpack downto zpack);
            sig_collect_header_key_out_to_tree_collection(31 downto 16) <= storebyte & packet_in(lenpack downto zpack);
            vld_collect_header_reg(1 downto 1)<= "1";
            when 22 =>  storebyte       <= packet_in(lenpack downto zpack);
            when 23 =>  dest_port       <= storebyte & packet_in(lenpack downto zpack);
            sig_collect_header_key_out_to_tree_collection(15 downto 0) <= storebyte & packet_in(lenpack downto zpack);
            vld_collect_header_reg(0 downto 0)<= "1";
            when 24 =>  storebyte       <= packet_in(lenpack downto zpack);
            when 25 =>  storebyte2      <= packet_in(lenpack downto zpack);
            when 26 =>  storebyte3      <= packet_in(lenpack downto zpack);
            when 27 =>  tcp_seq_num     <= storebyte & storebyte2 & storebyte3 & packet_in(lenpack downto zpack);
            when 28 =>  storebyte       <= packet_in(lenpack downto zpack);
            when 29 =>  storebyte2      <= packet_in(lenpack downto zpack);
            when 30 =>  storebyte3      <= packet_in(lenpack downto zpack);
            when 31 =>  tcp_ack_num     <= storebyte & storebyte2 & storebyte3 & packet_in(lenpack downto zpack);
            when 32 =>
              tcp_data_offset           <= packet_in(lenpack downto 7);
              tcp_reserved              <= packet_in(6 downto 4);
              storebyte                 <= packet_in(3) & "0000000";
            when 33 =>  tcp_flags       <= storebyte (7) & packet_in(lenpack downto zpack);
            when 34 =>  storebyte       <= packet_in(lenpack downto zpack);
            when 35 =>  tcp_window_size <= storebyte & packet_in(lenpack downto zpack);
            when 36 =>  storebyte       <= packet_in(lenpack downto zpack);
            when 37 =>  L4checksum      <= storebyte & packet_in(lenpack downto zpack);
            when 38 =>  storebyte       <= packet_in(lenpack downto zpack);
            when 39 =>  tcp_urgent_ptr  <= storebyte & packet_in(lenpack downto zpack);
            when others =>
            --packet_forward              <= packet_in;
            -- do nothing
          end case;
        end if; --TCP flag

        if udp_flag <= '0' then
        else
          case bytenum is
            when 20 =>  storebyte       <= packet_in(lenpack downto zpack);
            when 21 =>  src_port        <= storebyte & packet_in(lenpack downto zpack);
            sig_collect_header_key_out_to_tree_collection(31 downto 16) <= storebyte & packet_in(lenpack downto zpack);
            vld_collect_header_reg(1 downto 1)<= "1";
            when 22 =>  storebyte       <= packet_in(lenpack downto zpack);
            when 23 =>  dest_port       <= storebyte & packet_in(lenpack downto zpack);
            sig_collect_header_key_out_to_tree_collection(15 downto 0) <= storebyte & packet_in(lenpack downto zpack);
            vld_collect_header_reg(0 downto 0)<= "1";
            when 24 =>  storebyte       <= packet_in(lenpack downto zpack);
            --collect_header_key_out_to_tree_collection <= src_port & dest_port & ip_src_addr & ip_dest_addr;
            when 25 =>  udp_len         <= storebyte & packet_in(lenpack downto zpack);
            when 26 =>  storebyte       <= packet_in(lenpack downto zpack);
            when 27 =>  L4checksum      <= storebyte & packet_in(lenpack downto zpack);
            when others =>
            -- do nothing
          end case;
        end if; --UDP flag

      end if;

    end if;
  end process;

end architecture;