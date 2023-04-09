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
    
    fileinput       : in std_logic_vector(size downto 0);
    readprotocol    : in std_logic_vector(7 downto 0);
    
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
    tcp_flags       : out std_logic_vector(7 downto 0);   -- Bits 100-107, Flags (URG, ACK, PSH, RST, SYN, FIN)
    tcp_window_size : out std_logic_vector(15 downto 0);  -- Bits 108-123, Window size
    L4checksum      : out std_logic_vector(15 downto 0);  -- Bits 124-139, Checksum
    tcp_urgent_ptr  : out std_logic_vector(15 downto 0);  -- Bits 140-155, Urgent pointer

    udp_len         : out std_logic_vector(15 downto 0)

    );

end entity;

architecture arch_Collect_header of Collect_header is
begin

  process (clk)
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
        tcp_flags       <= (others => '0');
        tcp_window_size <= (others => '0');
        L4checksum      <= (others => '0');
        tcp_urgent_ptr  <= (others => '0');

        udp_len         <= (others => '0');
      else -- IF RESET = '0'
        
        ip_version      <= fileinput(size downto size-3);
        ip_header_len   <= fileinput(size-4 downto size-7);
        ip_TOS          <= fileinput(size-8 downto size-15);
        ip_total_len    <= fileinput(size-16 downto size-31);
        ip_ID           <= fileinput(size-32 downto size-47);
        ip_flags        <= fileinput(size-48 downto size-50);
        ip_fragmt_offst <= fileinput(size-51 downto size-63);
        ip_ttl          <= fileinput(size-64 downto size-71);
        ip_protocol     <= fileinput(size-72 downto size-79);
        ip_checksum     <= fileinput(size-80 downto size-95);
        ip_src_addr     <= fileinput(size-96 downto size-127);
        ip_dest_addr    <= fileinput(size-128 downto size-159);
      
        if readprotocol = x"06" then -- TCP protocol
          src_port        <= fileinput(size-160 downto size-175);
          dest_port       <= fileinput(size-176 downto size-191);
          tcp_seq_num     <= fileinput(size-192 downto size-223);
          tcp_ack_num     <= fileinput(size-224 downto size-255);
          tcp_data_offset <= fileinput(size-256 downto size-259);
          tcp_flags       <= fileinput(size-260 downto size-267);
          tcp_window_size <= fileinput(size-268 downto size-283);
          L4checksum      <= fileinput(size-284 downto size-299);
          tcp_urgent_ptr  <= fileinput(size-300 downto size-315);

        elsif readprotocol = x"11" then -- UDP protocol
          src_port        <= fileinput(size-160 downto size-175);
          dest_port       <= fileinput(size-176 downto size-191);
          udp_len         <= fileinput(size-192 downto size-207);
          L4checksum      <= fileinput(size-208 downto size-223);
      
        end if; -- Protocol if. Add another protocol if needed
      
      end if;
    end if;
  end process;

end architecture;