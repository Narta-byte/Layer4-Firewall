library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

library std;
use IEEE.std_logic_textio.all;

entity Collect_header_tb is
end;

architecture arch_Collect_header_tb of Collect_header_tb is
  constant size : integer := 10000;
  --65536

  component Collect_header
    port (
      clk : in std_logic;
      reset : in std_logic;

      fileinput       : in std_logic_vector(size downto 0);
     -- payload         : out std_logic_vector(size -224 downto 0);
      --readprotocol    : in std_logic_vector(7 downto 0);

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

      ip_version      : out std_logic_vector(3 downto 0);
      ip_header_len   : out std_logic_vector(3 downto 0);
      ip_TOS          : out std_logic_vector (7 downto 0);
      ip_total_len    : out std_logic_vector(15 downto 0);
      ip_ID           : out std_logic_vector(15 downto 0);
      ip_flags        : out std_logic_vector(2 downto 0);
      ip_fragmt_offst : out std_logic_vector(12 downto 0);
      ip_ttl          : out std_logic_vector(7 downto 0);
      ip_protocol     : out std_logic_vector(7 downto 0);
      ip_checksum     : out std_logic_vector(15 downto 0);
      ip_src_addr     : out std_logic_vector(31 downto 0);
      ip_dest_addr    : out std_logic_vector(31 downto 0);
      
      src_port        : out std_logic_vector(15 downto 0);
      dest_port       : out std_logic_vector(15 downto 0);
      tcp_seq_num     : out std_logic_vector(31 downto 0);
      tcp_ack_num     : out std_logic_vector(31 downto 0);
      tcp_data_offset : out std_logic_vector(3 downto 0);
      tcp_flags       : out std_logic_vector(8 downto 0);
      tcp_window_size : out std_logic_vector(15 downto 0);
      L4checksum      : out std_logic_vector(15 downto 0);
      tcp_urgent_ptr  : out std_logic_vector(15 downto 0);
      
      udp_len         : out std_logic_vector(15 downto 0)


      -- new!
      


    );
  end component;

  -- Clock period
  constant clk_period : time := 2 ns;

  -- Ports
  signal clk : std_logic;
  signal reset : std_logic;

  signal fileinput        : std_logic_vector(size downto 0) := (others => '0');
  -- signal readprotocol     : std_logic_vector(7 downto 0) := (others => '0');

  signal ip_version       : std_logic_vector(3 downto 0) := (others => '0');
  signal ip_header_len    : std_logic_vector(3 downto 0) := (others => '0');
  signal ip_TOS           : std_logic_vector (7 downto 0) := (others => '0');
  signal ip_total_len     : std_logic_vector(15 downto 0) := (others => '0');
  signal ip_ID            : std_logic_vector(15 downto 0) := (others => '0');
  signal ip_flags         : std_logic_vector(2 downto 0) := (others => '0');
  signal ip_fragmt_offst  : std_logic_vector(12 downto 0) := (others => '0');
  signal ip_ttl           : std_logic_vector(7 downto 0) := (others => '0');
  signal ip_protocol      : std_logic_vector(7 downto 0) := (others => '0');
  signal ip_checksum      : std_logic_vector(15 downto 0) := (others => '0');
  signal ip_src_addr      : std_logic_vector(31 downto 0) := (others => '0');
  signal ip_dest_addr     : std_logic_vector(31 downto 0) := (others => '0');

    
  -- TCP header s ignals
  signal src_port         : std_logic_vector(15 downto 0) := (others => '0');
  signal dest_port        : std_logic_vector(15 downto 0) := (others => '0');
  signal tcp_seq_num      : std_logic_vector(31 downto 0) := (others => '0');
  signal tcp_ack_num      : std_logic_vector(31 downto 0) := (others => '0');
  signal tcp_data_offset  : std_logic_vector(3 downto 0) := (others => '0');
  signal tcp_flags        : std_logic_vector(8 downto 0) := (others => '0');
  signal tcp_window_size  : std_logic_vector(15 downto 0) := (others => '0');
  signal L4checksum       : std_logic_vector(15 downto 0) := (others => '0');
  signal tcp_urgent_ptr   : std_logic_vector(15 downto 0) := (others => '0');
 
  signal udp_len          : std_logic_vector(15 downto 0);
  
  -- Payload signal
  --signal payload : std_logic_vector(size -224 downto 0) := (others => '0');


  -- New version!
  signal packet_in : std_logic_vector (9 downto 0);
  signal packet_start : std_logic := '0';
  signal bytenm : integer := 0;


  signal SoP : std_logic;
  signal EoP : std_logic;

  signal packet_data : std_logic_vector(7 downto 0);


  signal vld_firewall : std_logic;
  signal rdy_FIFO : std_logic;
  signal rdy_hash : std_logic;

  signal ready_hdr : std_logic;

  signal vld_hdr : std_logic;
  signal hdr_SoP : std_logic;
  signal hdr_EoP : std_logic;
  signal filedone : std_logic;

begin

  DUT : Collect_header
  port map(
    clk => clk,
    reset => reset,

    packet_in => packet_in,
    SoP             => SoP,
    EoP             => EoP,
    vld_firewall    => vld_firewall,
    rdy_FIFO        =>rdy_FIFO,
    rdy_hash        => rdy_hash,
    
    -- rdy_collecthdr  => rdy_collecthdr,
    -- vld_hdr         => vld_hdr,
    -- vld_hdr_FIFO    =>vld_hdr_FIFO,
    -- hdr_SoP         =>hdr_SoP,
    -- hdr_EoP         =>hdr_EoPm,
    
    -- packet_forward  => packet_forward,
    
    fileinput       => fileinput,
    -- payload         => payload,
     --readprotocol    => readprotocol,

    ip_version      => ip_version,
    ip_header_len   => ip_header_len,
    ip_TOS          => ip_TOS,
    ip_total_len    => ip_total_len,
    ip_ID           => ip_ID,
    ip_flags        => ip_flags,
    ip_fragmt_offst => ip_fragmt_offst,
    ip_ttl          => ip_ttl,
    ip_protocol     => ip_protocol,
    ip_checksum     => ip_checksum,
    ip_src_addr     => ip_src_addr,
    ip_dest_addr    => ip_dest_addr,

    src_port        => src_port,
    dest_port       => dest_port,
    tcp_seq_num     => tcp_seq_num,
    tcp_ack_num     => tcp_ack_num,
    tcp_data_offset => tcp_data_offset,
    tcp_flags       => tcp_flags,
    tcp_window_size => tcp_window_size,
    L4checksum      => L4checksum,
    tcp_urgent_ptr  => tcp_urgent_ptr,

    udp_len         => udp_len

  );

  Read_file :  process (clk)
    file input : TEXT open READ_MODE is "C:/Users/Asger/OneDrive/Skrivebord/Layer4-Firewall/collect_header/input_packets.txt";

    variable current_read_line : line;
    variable current_read_field	: std_logic_vector (7 downto 0);
    variable current_write_line : std_logic;
  begin

      if rising_edge(clk) then

        if filedone = '1' then
          -- do nothing
        elsif rdy_FIFO = '0' or rdy_hash = '0' or vld_firewall = '0' then
          -- niemand

        elsif vld_firewall = '1' and rdy_hash = '1' and rdy_FIFO = '1' then --and SoP = '1' then
          if not ENDFILE(input) then 

            packet_start <= '1';
            bytenm <= bytenm + 1;
            readline(input, current_read_line);
            hread(current_read_line, current_read_field);
            packet_data <= current_read_field;
        

            read(current_read_line, current_write_line);
            SoP <= current_write_line;
        
            read(current_read_line, current_write_line);
            EoP <= current_write_line;

            packet_in <= packet_data & SoP & EoP;

          else
            filedone <= '1';

          end if;
        end if;

      end if;
    
  end process;

  --readprotocol <= fileinput(size-72 downto size-79);
  --payload    <= fileinput(size-316 downto 0); --rest is paylaod



  TestInputs : process 
  begin
--     rdy_FIFO <= '1'; wait for 5 ns;
-- --    rdy_FIFO <= '1'; wait for 10000 ns;
--     rdy_FIFO <= '0'; wait for 10 ns;  
    rdy_FIFO <= '1'; wait;

  end process;

  Testcuckoo : process
  begin
    -- rdy_hash <= '0'; wait for 10 ns;
    -- rdy_hash <= '1'; wait for 2033 ns;
    -- rdy_hash <= '0'; wait for 6 ns;
    -- rdy_hash <= '1'; wait for 2 ns;
    -- rdy_hash <= '0'; wait for 6 ns;
    rdy_hash <= '1'; wait;
  end process;

  testvld : process 
  begin
    vld_firewall <= '1'; wait;
    
  end process;


  clk_proc : process --clk proc
  begin
    while now < 100000 ns loop
      clk <= '1'; wait for clk_period/2;
      clk <= '0'; wait for clk_period/2;
    end loop;
  end process;

  reset_proc : process -- reset proc
  begin
    reset <= '1'; wait for clk_period;
    reset <= '0'; wait;  
  end process;

end;