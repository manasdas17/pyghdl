library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library ahir;
use ahir.Types.all;
use ahir.Subprograms.all;
use ahir.Utilities.all;
use ahir.BaseComponents.all;

entity SplitCallArbiter is
  generic(num_reqs: integer;
	  call_data_width: integer;
	  return_data_width: integer;
	  caller_tag_length: integer;
          callee_tag_length: integer);
  port ( -- ready/ready handshake on all ports
    -- ports for the caller
    call_reqs   : in  std_logic_vector(num_reqs-1 downto 0);
    call_acks   : out std_logic_vector(num_reqs-1 downto 0);
    call_data   : in  std_logic_vector((num_reqs*call_data_width)-1 downto 0);
    call_tag    : in  std_logic_vector((num_reqs*caller_tag_length)-1 downto 0);
    -- call port connected to the called module
    call_mreq   : out std_logic;
    call_mack   : in  std_logic;
    call_mdata  : out std_logic_vector(call_data_width-1 downto 0);
    call_mtag   : out std_logic_vector(callee_tag_length+caller_tag_length-1 downto 0);
    -- similarly for return, initiated by the caller
    return_reqs : in  std_logic_vector(num_reqs-1 downto 0);
    return_acks : out std_logic_vector(num_reqs-1 downto 0);
    return_data : out std_logic_vector((num_reqs*return_data_width)-1 downto 0);
    return_tag  : out std_logic_vector((num_reqs*caller_tag_length)-1 downto 0);
    -- return from function
    return_mreq : out std_logic;
    return_mack : in std_logic;
    return_mdata : in  std_logic_vector(return_data_width-1 downto 0);
    return_mtag : in  std_logic_vector(callee_tag_length+caller_tag_length-1 downto 0);
    clk: in std_logic;
    reset: in std_logic);
end SplitCallArbiter;


architecture Struct of SplitCallArbiter is
   signal pe_call_reqs, pe_call_reqs_reg: std_logic_vector(num_reqs-1 downto 0);
   signal return_acks_sig: std_logic_vector(num_reqs-1 downto 0);

   type TwordArray is array (natural range <>) of std_logic_vector(return_mdata'length-1 downto 0);
   signal return_data_sig : TwordArray(num_reqs-1 downto 0);

   type TagwordArray is array (natural range <>) of std_logic_vector(caller_tag_length-1 downto 0);
   signal return_tag_sig : TagwordArray(num_reqs-1 downto 0);

   type CallStateType is (idle, busy);
   signal call_state: CallStateType;


   signal latch_call_data : std_logic;
   signal call_mdata_prereg  : std_logic_vector(call_data_width-1 downto 0);
   signal callee_mtag_prereg, callee_mtag_reg  : std_logic_vector(callee_tag_length-1 downto 0);
   signal caller_mtag_reg  : std_logic_vector(caller_tag_length-1 downto 0);

   signal fair_call_reqs, fair_call_acks: std_logic_vector(num_reqs-1 downto 0);
   
begin
  -----------------------------------------------------------------------------
  -- "fairify" the call-reqs.
  -----------------------------------------------------------------------------
  fairify: NobodyLeftBehind generic map (num_reqs => num_reqs)
		port map (clk => clk, reset => reset, reqIn => call_reqs, ackOut => call_acks,
					reqOut => fair_call_reqs, ackIn => fair_call_acks);

  -----------------------------------------------------------------------------
  -- priority encode incoming
  -----------------------------------------------------------------------------
   pe_call_reqs <= PriorityEncode(fair_call_reqs);

   ----------------------------------------------------------------------------
   -- process to handle call_reqs  --> call_mreq muxing
   ----------------------------------------------------------------------------
   process(clk,pe_call_reqs,call_state,reset)
        variable nstate: CallStateType;
        variable there_is_a_call : std_logic;
   begin
	nstate := call_state;
        there_is_a_call := OrReduce(pe_call_reqs);
	latch_call_data <= '0';
	call_mreq <= '0';

	if(call_state = idle) then
		if(there_is_a_call = '1') then
			latch_call_data <=  '1';
			nstate := busy;
		end if;
	elsif (call_state = busy) then
		call_mreq <= '1';
		if(call_mack = '1') then
			if(there_is_a_call = '1') then
				latch_call_data <=  '1';
                        else
				nstate := idle;
			end if;
		end if;
	end if;
	
	if(clk'event and clk = '1') then
		if(reset = '1') then
			call_state <= idle;
			pe_call_reqs_reg <= (others => '0');
		else
			call_state <= nstate;
		end if;
	end if;
   end process;



   -- combinational process.. generate fair_call_acks, and also
   -- mux to input of call data register.
   process(pe_call_reqs,latch_call_data,call_data)
	variable out_data : std_logic_vector(call_data_width-1 downto 0);
   begin
	fair_call_acks <= (others => '0');
	out_data := (others => '0');
       	for I in num_reqs-1 downto 0 loop
       		if(pe_call_reqs(I) = '1') then
       			Extract(call_data,I,out_data);
			if(latch_call_data = '1') then
				fair_call_acks(I) <= '1';
			end if;
       		end if;
	end loop;
	call_mdata_prereg <= out_data;
   end process;

   -- call data register.
   process(clk)
   begin
     if(clk'event and clk = '1') then
     	if(latch_call_data = '1') then
		call_mdata <= call_mdata_prereg;
		callee_mtag_reg <= callee_mtag_prereg;
        end if;  -- I
     end if;
   end process;
 

   -- tag generation.
   tagGen : BinaryEncoder generic map (iwidth => num_reqs,
                                       owidth => callee_tag_length)
     port map (din => pe_call_reqs, dout => callee_mtag_prereg);

   -- on a successful call, register the tag from the caller
   -- side..
   process(clk)
	variable tvar : std_logic_vector(caller_tag_length-1 downto 0);
   begin
       if(clk'event and clk = '1') then
	for T in 0 to num_reqs-1 loop
         if(pe_call_reqs(T) = '1' and latch_call_data = '1') then
           tvar := call_tag(((T+1)*caller_tag_length)-1 downto T*caller_tag_length);
         end if;
        end loop;
	caller_mtag_reg <= tvar;
       end if;
   end process;     

   -- call tag.
   call_mtag <= callee_mtag_reg & caller_mtag_reg;


   ----------------------------------------------------------------------------
   -- reverse path
   ----------------------------------------------------------------------------
   -- pack registers into return data array
   process(return_data_sig)
     variable lreturn_data : std_logic_vector((num_reqs*return_data_width)-1 downto 0);
   begin
     for J in return_data_sig'high(1) downto return_data_sig'low(1) loop
       Insert(lreturn_data,J,return_data_sig(J));
     end loop;  -- J
     return_data <= lreturn_data;
   end process;
 
   -- 2D to 1D packing.
   process(return_tag_sig)
     variable lreturn_tag : std_logic_vector((num_reqs*caller_tag_length)-1 downto 0);
   begin
     for J in return_tag_sig'high(1) downto return_tag_sig'low(1) loop
       Insert(lreturn_tag,J,return_tag_sig(J));
     end loop;  -- J
     return_tag <= lreturn_tag;
   end process;

   -- always ready to accept return data!
   return_mreq <= '1';

   -- return to caller.
   return_acks <= return_acks_sig;
   
   -- incoming data written into appropriate register.
   RetGen: for I in return_reqs'high downto return_reqs'low generate

     fsm: block
       signal ack_reg, valid_flag : std_logic;
       signal data_reg : std_logic_vector(return_mdata'length-1 downto 0);
       signal tag_reg  : std_logic_vector(caller_tag_length-1 downto 0);
     begin  -- block fsm

       -- valid = '1' implies this index is incoming
       valid_flag <= '1' when return_mack = '1' and (I = To_Integer(To_Unsigned(return_mtag(caller_tag_length+callee_tag_length-1 downto caller_tag_length)))) else '0';

       --------------------------------------------------------------------------
       -- ack ff
       --------------------------------------------------------------------------
       -- set if mack_sig is asserted, else clear if return_reqs is asserted
       -- and register is already set.
       process(clk)
       begin
         if clk'event and clk= '1' then
           if(reset = '1') then
             ack_reg <= '0';
           elsif valid_flag = '1' then
             ack_reg <= '1';
           elsif return_reqs(I) = '1' and ack_reg = '1' then
             ack_reg <= '0';
           end if;

           -- register data when you send mack
           if(valid_flag = '1') then
             data_reg <= return_mdata;
             tag_reg  <= return_mtag(caller_tag_length-1 downto 0);
           end if;
         end if;
       end process;

       -- pass info out of the generate
       return_acks_sig(I) <= ack_reg;
       return_data_sig(I) <= data_reg;
       return_tag_sig(I)  <= tag_reg;

     end block fsm;
     
   end generate RetGen;

end Struct;
