// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.6.0;

contract PoRX
{

	struct user {
		bool 							isInit;
		mapping(uint256 => uint256)		reputation;
		uint256 						lastUpdate;
	}


	uint256 							blockNumberDeployement;
	address 							deployerAddress;
	uint256 							defaultReputation;
	mapping(address => user) 			users;


    constructor() public
    {
        blockNumberDeployement		= block.number;
        deployerAddress				= msg.sender;
        defaultReputation			= 1000;
    }




	function init() public
	{
		users[msg.sender].isInit = true;
		users[msg.sender].lastUpdate = block.number;
		users[msg.sender].reputation[users[msg.sender].lastUpdate] = defaultReputation;
	}



	function is_init(address to) public view returns(bool)
	{
		return (users[to].lastUpdate != 0);
	}


	function vote(address to, bool v) public returns (bool)
	{
		if (is_init(to))
		{
			if (v)
			{
				users[to].reputation[block.number] = users[to].reputation[users[to].lastUpdate] + 1;
			}
			else
			{
				users[to].reputation[block.number] = users[to].reputation[users[to].lastUpdate] - 1;
			}
			users[to].lastUpdate = block.number;
			return true;
		}
		else
		{
			return false;
			// address not init
		}
	}



	function get_reputation(address to) public view returns (uint256)
	{
		return users[to].reputation[users[to].lastUpdate];
	} 

	function get_reputation(address to, uint256 b) public view returns (uint256)
	{
		return users[to].reputation[b];
	} 

}
