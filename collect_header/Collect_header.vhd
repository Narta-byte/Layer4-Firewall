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
    
    packet_in       : in std_logic_vector(9 downto 0);
    SoP             : in std_logic;
    EoP             : in std_logic;
    vld_firewall    : in std_logic;
    rdy_FIFO        : in std_logic;
    rdy_hash        : in std_logic;
    
    rdy_collecthdr  : out std_logic;
    vld_hdr         : out std_logic;
    vld_hdr_FIFO    : out std_logic;
    hdr_SoP         : out std_logic;
    hdr_EoP         : out std_logic;
    
    packet_forward  : out std_logic_vector(9 downto 0);
    
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

begin

  logic_proc : process (clk, bytenum, SoP, packet_in)
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
      else -- IF RESET = '0'
        if wait_start <= '0' then
          bytenum <= 0;
        else
          bytenum <= bytenum +1;
          packet_forward <= packet_in;
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
        end if;


        case bytenum is
          when 0 =>
            ip_version                  <= packet_in(9 downto 6);
            ip_header_len               <= packet_in(5 downto 2);
          when 1 =>   ip_TOS            <= packet_in(9 downto 2);
          when 2 =>   storebyte         <= packet_in(9 downto 2);
          when 3 =>   ip_total_len      <= storebyte & packet_in(9 downto 2);
          when 4 =>   storebyte         <= packet_in(9 downto 2);
          when 5 =>   ip_ID             <= storebyte & packet_in(9 downto 2);
          when 6 =>
            ip_flags                    <= packet_in(9 downto 7);
            storebyte                   <= packet_in(6 downto 2) & "000";
          when 7 => ip_fragmt_offst     <= storebyte(7 downto 3) & packet_in(9 downto 2);
          when 8 => ip_ttl              <= packet_in(9 downto 2);
          when 9 => ip_protocol         <= packet_in(9 downto 2);
          case packet_in(9 downto 2) is -- ADD CASES FOR DIFFERENT PROTOCOLS
            when x"06" => tcp_flag<= '1';
            when x"11" => udp_flag<= '1';
            when others => null;
          end case;
          when 10 =>    storebyte       <= packet_in(9 downto 2);
          when 11 =>    ip_checksum     <= storebyte & packet_in(9 downto 2);
          when 12 =>    storebyte       <= packet_in(9 downto 2);
          when 13 =>    storebyte2      <= packet_in(9 downto 2);
          when 14 =>    storebyte3      <= packet_in(9 downto 2);
          when 15 =>    ip_src_addr     <= storebyte & storebyte2 & storebyte3 & packet_in(9 downto 2);
          when 16 =>    storebyte       <= packet_in(9 downto 2);
          when 17 =>    storebyte2      <= packet_in(9 downto 2);
          when 18 =>    storebyte3      <= packet_in(9 downto 2);
          when 19 =>    ip_dest_addr    <= storebyte & storebyte2 & storebyte3 & packet_in(9 downto 2);
          when others =>  null;
        end case;
    
        if tcp_flag <= '0' then
        else
          case bytenum is
            when 20 =>  storebyte       <= packet_in(9 downto 2);
            when 21 =>  src_port        <= storebyte & packet_in(9 downto 2);
            when 22 =>  storebyte       <= packet_in(9 downto 2);
            when 23 =>  dest_port       <= storebyte & packet_in(9 downto 2);
            when 24 =>  storebyte       <= packet_in(9 downto 2);
            when 25 =>  storebyte2      <= packet_in(9 downto 2);
            when 26 =>  storebyte3      <= packet_in(9 downto 2);
            when 27 =>  tcp_seq_num     <= storebyte & storebyte2 & storebyte3 & packet_in(9 downto 2);
            when 28 =>  storebyte       <= packet_in(9 downto 2);
            when 29 =>  storebyte2      <= packet_in(9 downto 2);
            when 30 =>  storebyte3      <= packet_in(9 downto 2);
            when 31 =>  tcp_ack_num     <= storebyte & storebyte2 & storebyte3 & packet_in(9 downto 2);
            when 32 =>
              tcp_data_offset           <= packet_in(9 downto 6);
              tcp_reserved              <= packet_in(5 downto 3);
              storebyte                 <= packet_in(2) & "0000000";
            when 33 =>  tcp_flags       <= storebyte (7) & packet_in(9 downto 2);
            when 34 =>  storebyte       <= packet_in(9 downto 2);
            when 35 =>  tcp_window_size <= storebyte & packet_in(9 downto 2);
            when 36 =>  storebyte       <= packet_in(9 downto 2);
            when 37 =>  L4checksum      <= storebyte & packet_in(9 downto 2);
            when 38 =>  storebyte       <= packet_in(9 downto 2);
            when 39 =>  tcp_urgent_ptr  <= storebyte & packet_in(9 downto 2);
            when others =>
            --packet_forward              <= packet_in;
            -- do nothing
          end case;
        end if; --TCP flag

        if udp_flag <= '0' then
        else
          case bytenum is
            when 20 =>  storebyte       <= packet_in(9 downto 2);
            when 21 =>  src_port        <= storebyte & packet_in(9 downto 2);
            when 22 =>  storebyte       <= packet_in(9 downto 2);
            when 23 =>  dest_port       <= storebyte & packet_in(9 downto 2);
            when 24 =>  storebyte       <= packet_in(9 downto 2);
            when 25 =>  udp_len         <= storebyte & packet_in(9 downto 2);
            when 26 =>  storebyte       <= packet_in(9 downto 2);
            when 27 =>  L4checksum      <= storebyte & packet_in(9 downto 2);
            when others =>
            -- do nothing
          end case;
        end if; --UDP flag


      end if;


    end if;
  end process;

end architecture;