// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;


contract PoRX
{
// UINT256 MANAGMENT ///////////////////////////////////////////
	function max(uint256 a, uint256 b) private pure returns (uint256)
	{
		return a > b ? a : b;
	}

	function min(uint256 a, uint256 b) private pure returns (uint256)
	{
		return a < b ? a : b;
	}
////////////////////////////////////////////////////////////////

// BOOL MANAGMENT //////////////////////////////////////////////
	function xor3(bool a, bool b, bool c) private pure returns(bool)
	{
		return ( a && !b && !c   ||   !a && b && !c   ||  !a && !b && c   ||   a && b && c );
	}

	function maj3(bool a, bool b, bool c) private pure returns(bool)
	{
		return ( !a && b && c   ||   a && !b && c   ||  a && b && !c   ||   a && b && c );
	}
////////////////////////////////////////////////////////////////

// UNSIGNED FIXED MANAGMENT ////////////////////////////////////
	struct unsignedfixed {
		uint256 						integer;
		uint256 						decimal;
	}

	function eval(unsignedfixed memory op) private pure returns(uint256)
	{
		require (op.integer!=2**256-1 || op.decimal < 2**255, "Math overflow : eval-00");
		if (op.decimal < 2**255)
		{
			return(op.integer);
		}
		else
		{
			return(op.integer + 1);
		}
	}

	function cmp(unsignedfixed memory op1, uint256 op2) private pure returns(int8)
	{
		if (op1.integer > op2 || op1.integer == op2 && op1.decimal > 0)
		{
			return 1;
		}
		else if (op1.integer == op2 && op1.decimal == 0)
		{
			return 0;
		}
		else
		{
			return -1;
		}
	}

	function cmp(unsignedfixed memory op1, unsignedfixed memory op2) private pure returns(int8)
	{
		if (op1.integer > op2.integer || op1.integer == op2.integer && op1.decimal > op2.decimal)
		{
			return 1;
		}
		else if (op1.integer == op2.integer && op1.decimal == op2.decimal)
		{
			return 0;
		}
		else
		{
			return -1;
		}
	}

	function sub(unsignedfixed memory op1, uint256 op2) private pure returns(uint256, uint256)
	{
		require(cmp(op1,op2) >= 0, "Math overflow : sub-00");
		return (op1.integer - op2 , op1.decimal);
	}

	function sub(unsignedfixed memory op1, unsignedfixed memory op2) private pure returns(uint256, uint256)
	{
		require(cmp(op1,op2) >= 0, "Math overflow : sub-01");
		uint256 	td = op1.decimal - op2.decimal;
		if (td > op1.decimal)
		{
			return(op1.integer - op2.integer - 1 , td);
		}
		else
		{
			return(op1.integer - op2.integer , td);
		}
	}
	
	function add(unsignedfixed memory op1, uint256 op2) private pure returns(uint256, uint256)
	{
		uint256 i = op1.integer + op2;
		require(i >= op1.integer, "Math overflow : add-00");
		return (i , op1.decimal);
	}

	function add(unsignedfixed memory op1, unsignedfixed memory op2) private pure returns(uint256, uint256)
	{
		uint256 i = op1.integer + op2.integer;
		require(i >= op1.integer, "Math overflow : add-01");

		uint256 d = op1.decimal + op2.decimal;
		if (d < op1.decimal)
		{
			i += 1;
			require(i > 0, "Maths overflow : add-02");
		}
		return (i , d);
	}

	function mul(unsignedfixed memory op1, uint256 op2) private pure returns(uint256, uint256)
	{
		uint256 				d = op2;
		uint256 				ti;
		uint256 				td;
		unsignedfixed memory 	m = op1;
		unsignedfixed memory 	r = unsignedfixed(0,0);

		while (d > 0)
		{
			if (d % 2 == 1)
			{
				(ti,td) = add(r,m);
				r = unsignedfixed(ti,td);
			}
			(ti,td) = add(m,m);
			m = unsignedfixed(ti,td);
			d = d/2;
		}
		return ( r.integer, r.decimal );
	}

	function mul(unsignedfixed memory op1, unsignedfixed memory op2) private pure returns(uint256,uint256)
	{
		uint256 					ad = op1.decimal;
		unsignedfixed memory 	aTruncted = unsignedfixed(0,ad);
		uint256 					bd = op2.decimal;
		unsignedfixed memory 	bTruncted = unsignedfixed(0,bd);
		uint256 					ti = 0;
		uint256 					td = 0;
		unsignedfixed memory 	r = unsignedfixed(0,0);
		unsignedfixed memory 	t;
		//////////////////////
		if (op1.integer != 0 && op2.integer != 0)
		{
			ti = op1.integer * op2.integer;
			require(ti/op1.integer == op2.integer , "Math overflow : mul-00");
			r = unsignedfixed(ti,0);
		}
		//////////////////////
		(ti, td) = mul(aTruncted,op2.integer);
		t = unsignedfixed(ti, td);
		(ti, td) = add(r, t);
		r = unsignedfixed(ti, td);
		//////////////////////
		(ti, td) = mul(bTruncted,op1.integer);
		t = unsignedfixed(ti, td);
		(ti, td) = add(r, t);
		r = unsignedfixed(ti, td);
		//////////////////////
		bool[256] memory 	boolad;
		bool[256] memory 	boolbd;
		bool[512] memory 	boolr;
		bool 				c;
		bool 				m;
		for (uint16 i = 0 ; i < 512 ; i++)
		{
			boolr[i] = false;
		}
		for (uint16 i = 0 ; i < 256 ; i++)
		{
			boolad[i] = (ad % 2 == 1);
			boolbd[i] = (bd % 2 == 1);
			ad /= 2;
			bd /= 2;
		}
		for (uint16 j = 0 ; j < 256 ; j++)
		{
			if (boolbd[j] == true)
			{
				c = false;
				for (uint16 i = 0 ; i < 256 ; i++)
				{
					m = maj3( boolr[i+j] , boolad[i] , c );
					boolr[i+j] = xor3( boolr[i+j] , boolad[i] , c );
					c = m;
				}
				boolr[j+256] = c;
			}
		}
		td = 0;
		ad = 1;
		for (uint16 i = 256 ; i < 512 ; i++)
		{
			if (boolr[i] == true)
			{
				td += ad;
			}
			ad *=2;
		}
		t = unsignedfixed(0, td);
		(ti, td) = add(r, t);
		r = unsignedfixed(ti, td);
		//////////////////////
		return ( r.integer, r.decimal );
	}

	function exp(unsignedfixed memory op1, uint256 op2) private pure returns(uint256, uint256)
	{
		uint256 				d = op2;
		uint256 				ti;
		uint256 				td;
		unsignedfixed memory 	m = op1;
		unsignedfixed memory 	r = unsignedfixed(1,0);

		while (d > 0)
		{
			if (d % 2 == 1)
			{
				(ti,td) = mul(r,m);
				r = unsignedfixed(ti,td);
			}
			(ti,td) = mul(m,m);
			m = unsignedfixed(ti,td);
			d = d/2;
		}
		return ( r.integer, r.decimal );
	}
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
//////             ____             _                     //////
//////            | __ )  ___  __ _(_)_ __                //////
//////            |  _ \ / _ \/ _` | | '_ \               //////
//////            | |_) |  __/ (_| | | | | |              //////
//////            |____/ \___|\__, |_|_| |_|              //////
//////                        |___/                       //////
//////                                                    //////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////

// EVENTS DEFINITIONS //////////////////////////////////////////
	event SubmitNonce(
		address 	miner,
		uint256 	nonce,
		bool 		valid
	);

	event MinerAdded(
		address 	authority,
		address 	miner
	);

	event MinerRevoked(
		address 	authority,
		address 	miner
	);
////////////////////////////////////////////////////////////////

// STRUCTURES DEFINITIONS //////////////////////////////////////
	struct user {
		mapping(uint256 => uint256)		reputation;
		uint256 						lastUpdate;
	}

	struct infos {
		address[] 						miner;
		uint256[] 						nonce;
		uint256 						C_DURATION; 	// MINER_NUMBER * 2
		uint256 						C_REWARD; 		// C_DURATION * 2
		uint256 						C_DECAY; 		// C_DURATION * 3
		uint256 						S_REWARD; 		// C_DURATION * 2/3
		uint256 						S_DECAY; 		// C_DURATION * 1/5
		uint256 						DIFFICULTY;

	}


	uint256 							REPUTATION_INIT;
	uint256								REPUTATION_MIN;
	uint256 							REPUTATION_MAX;
	unsignedfixed 						REPUTATION_RATIO;
	unsignedfixed 						EXP_BASE;

	uint256 							lastDurationsUpdate;
	uint256 							lastDifficultyUpdate;

	uint256 							D_REWARD; 		// 100
	uint256 							D_DECAY; 		// 30



	uint256 							blockNumberDeployement;
	address 							deployerAddress;

	address[] 							miners;
	mapping(address => user) 			users;
	mapping(uint256 => infos) 			blocksInfos;
////////////////////////////////////////////////////////////////


	constructor() public
	{
		blockNumberDeployement		= block.number;
		deployerAddress				= msg.sender;

		REPUTATION_INIT 			= 1000000;
		REPUTATION_MIN 				= 0;
		REPUTATION_MAX 				= 2000000;
		REPUTATION_RATIO 			= unsignedfixed(0,81054462466121331654297947877312653763010293774228066756570728700602117783552); // 70% must be < 100%
		EXP_BASE 					= unsignedfixed(1,34737626771194857341520860095414151922411321526762087194074880176139670650880); // 1.3
		D_REWARD 					= 100;
		D_DECAY 					= 30;
		update_duration();
		update_difficulty();
    }


// AUTHORITY FUNCTIONs /////////////////////////////////////////
	function add_miner(address a) public
	{
		require(msg.sender == deployerAddress, "unauthorized user");
		miners.push(a);
		users[a].lastUpdate = block.number;
		users[a].reputation[users[msg.sender].lastUpdate] = REPUTATION_INIT;
		update_duration();
		emit MinerAdded(msg.sender, a);
	}

	function revoke_miner(address a) public
	{
		require(msg.sender == deployerAddress, "unauthorized user");
		for(uint256 i = 0 ; i < miners.length ; i++)
		{
			if (miners[i] == a)
			{
				miners[i] = miners[miners.length - 1];
				miners.pop();
				delete users[a];
				update_duration();
				emit MinerRevoked(msg.sender, a);
				return;
			}
		}
		require(false, "miner not found");
	}
////////////////////////////////////////////////////////////////

// DURATION FUNCTIONs //////////////////////////////////////////
	function update_duration() public
	{
		blocksInfos[block.number].C_DURATION			= miners.length * 2;
		blocksInfos[block.number].C_REWARD 				= blocksInfos[block.number].C_DURATION * 2;
		blocksInfos[block.number].C_DECAY 				= blocksInfos[block.number].C_DURATION * 3;

		blocksInfos[block.number].S_REWARD 				= max(1, blocksInfos[block.number].C_DURATION * 2 / 3);
		blocksInfos[block.number].S_DECAY 				= max(1, blocksInfos[block.number].C_DURATION * 1 / 5);

		lastDurationsUpdate = block.number;
	}

	function get_C_DURATION() public view returns(uint256) //private
	{
		return blocksInfos[lastDurationsUpdate].C_DURATION;
	}

	function get_C_REWARD() public view returns(uint256) // private
	{
		return blocksInfos[lastDurationsUpdate].C_REWARD;
	}

	function get_C_DECAY() public view returns(uint256) // private
	{
		return blocksInfos[lastDurationsUpdate].C_DECAY;
	}

	function get_S_REWARD() public view returns(uint256) // private
	{
		return blocksInfos[lastDurationsUpdate].S_REWARD;
	}

	function get_S_DECAY() public view returns(uint256) // private
	{
		return blocksInfos[lastDurationsUpdate].S_DECAY;
	}
////////////////////////////////////////////////////////////////

// DIFFICULTY FUNCTIONs ////////////////////////////////////////
	function update_difficulty() public
	{
		blocksInfos[block.number].DIFFICULTY = 1000;
		lastDifficultyUpdate = block.number;
	}

	function get_DIFFICULTY() public view returns(uint256)
	{
		return blocksInfos[lastDifficultyUpdate].DIFFICULTY;
	}
////////////////////////////////////////////////////////////////


	function is_miner(address a) public view returns(bool)
	{
		for(uint256 i = 0 ; i < miners.length ; i++)
		{
			if (miners[i] == a)
			{
				return true;
			}
		}
		return false;
	}

	function get_miner_of(uint256 b, uint256 n) public view returns (address)
	{
		if(n>=blocksInfos[b].miner.length)
		{
			return 0x0000000000000000000000000000000000000000;
		}		
		return blocksInfos[b].miner[n];
	} 

	function previous_header() public view returns(bytes32) 
	{
		return sha256(abi.encode(get_miner_of(block.number, 0) , get_C_DURATION() , get_DIFFICULTY()));
	}
	
	function hash(uint256 nonce) private view returns(bytes32)
	{
		return sha256(abi.encode(previous_header(),nonce));
	}

// SELF FUNCTIONS //////////////////////////////////////////////
	function self_reputation() private view returns(uint256)
	{
		return users[msg.sender].reputation[users[msg.sender].lastUpdate];
	}

	function self_usable_reputation() private view returns(uint256)
	{
		uint256 				count = self_count_block_on(get_C_DURATION());
		//uint256 				ti;
		//uint256 				td;
		//unsignedfixed memory	t;

		//(ti, td) = exp(EXP_BASE, count);
		//t = unsignedfixed(ti, td);

		// division implementation needed
		//return self_reputation() / eval(t);
		return division_by_exp_base_pow_count(self_reputation(),count);
	}

	function self_threshold() public view returns(bytes32)
	{
		uint256 				usableReputation;
		uint256 				ti;
		uint256 				td;
		unsignedfixed memory 	t;

		usableReputation = self_usable_reputation();

		(ti, td) = mul(REPUTATION_RATIO, get_DIFFICULTY());
		t = unsignedfixed(ti, td);

		if (REPUTATION_INIT >= usableReputation)
		{
			(ti, td) = mul(t, REPUTATION_INIT - usableReputation);
			t = unsignedfixed(ti, td);
			ti = get_DIFFICULTY() + eval(t)/REPUTATION_INIT;
		}
		else
		{
			(ti, td) = mul(t, usableReputation - REPUTATION_INIT);
			t = unsignedfixed(ti, td);
			ti = get_DIFFICULTY() - eval(t)/REPUTATION_INIT;
		}

		return bytes32((2**256 - 1)/ti);
	}

	function self_miner_of(uint256 b) private view returns(bool)
	{
		uint256 	n = blocksInfos[b].miner.length;
		for(uint256 i = 0 ; i < n ; i++)
		{
			if (msg.sender == blocksInfos[b].miner[i])
			{
				return true;
			}
		}
		return false;
	}
	
	function self_count_block_on(uint256 duration) private view returns(uint256)
	{
		uint256 	count = 0;
		uint256 	tested;

		for(uint256 i=0 ; i<duration ; i++)
		{
			tested = block.number - i;
			if (tested < blockNumberDeployement)
			{
				break;
			}
			if (self_miner_of(tested))
			{
				count += 1;
			}
		}
		return count;
	}

	function self_submit(uint256 nonce) public
	{
		require(is_miner(msg.sender),"miner not initialized");
		if (hash(nonce) <= self_threshold())
		{
			blocksInfos[block.number].miner.push(msg.sender);
			blocksInfos[block.number].nonce.push(nonce);
			emit SubmitNonce(msg.sender, nonce, true);
		}
		else
		{
			emit SubmitNonce(msg.sender, nonce, false);
		}
	}
	

	function division_by_exp_base_pow_count(uint256 rep, uint256 count) private pure returns(uint256)
	{

		unsignedfixed memory invExp = unsignedfixed(0,89070837874858603953205770577807803372855841293999929151814172152337679777792); // 1/1.3
		uint256 				ti;
		uint256 				td;
		unsignedfixed memory	t;

		if (count == 0)
		{
			return rep;
		}
		else if (count == 1)
		{
			(ti, td) = mul(invExp, rep);
			t = unsignedfixed(ti, td);
			return eval(t);
		}
		else
		{
			(ti, td) = exp(invExp, count);
			t = unsignedfixed(ti, td);
			(ti, td) = mul(t, rep);
			t = unsignedfixed(ti, td);
			return eval(t);
		}
	}
////////////////////////////////////////////////////////////////





// DEBUG ///////////////////////////////////////////////////////

	function debug_get_reputation(address to) public view returns (uint256)
	{
		return users[to].reputation[users[to].lastUpdate];
	} 

	function debug_get_reputation(address to, uint256 b) public view returns (uint256)
	{
		return users[to].reputation[b];
	} 
////////////////////////////////////////////////////////////////


}
