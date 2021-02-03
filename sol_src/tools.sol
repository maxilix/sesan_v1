// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;


contract tools
{




// INT256 MANAGMENT ////////////////////////////////////////////
	function max(int256 a, int256 b) private pure returns (int256)
	{
		return a > b ? a : b;
	}

	function max(int256[] memory t) private pure returns (int256)
	{
		require(t.length > 0 , "Math error, empty table : max-00");
		if (t.length == 1)
		{
			return t[0];
		}
		else
		{
			int256 m = max(t[0],t[1]);
			for(uint256 i = 2 ; i < t.length ; i++)
			{
				m = max(m,t[i]);
			}
			return m;
		}
	}
////////////////////////////////////////////////////////////////

}
