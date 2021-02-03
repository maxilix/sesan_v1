// SPDX-License-Identifier: GPL-3.0


pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;


contract UnsignedFixedPoint
{


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
	struct ufp
	{
		uint256 		I;
		uint256 		D;
	}

	function eval(ufp memory op) public pure returns(uint256)
	{
		require (op.I!=2**256-1 || op.D < 2**255, "Math overflow : eval-00");
		if (op.D < 2**255)
		{
			return(op.I);
		}
		else
		{
			return(op.I + 1);
		}
	}

	function cmp(ufp memory op1, uint256 op2) public pure returns(int8)
	{
		if (op1.I > op2 || op1.I == op2 && op1.D > 0)
		{
			return 1;
		}
		else if (op1.I == op2 && op1.D == 0)
		{
			return 0;
		}
		else
		{
			return -1;
		}
	}

	function cmp(ufp memory op1, ufp memory op2) public pure returns(int8)
	{
		if (op1.I > op2.I || op1.I == op2.I && op1.D > op2.D)
		{
			return 1;
		}
		else if (op1.I == op2.I && op1.D == op2.D)
		{
			return 0;
		}
		else
		{
			return -1;
		}
	}

	function sub(ufp memory op1, uint256 op2) public pure returns(ufp memory)
	{
		require(cmp(op1,op2) >= 0, "Math overflow : sub-00");
		return ufp(op1.I - op2 , op1.D);
	}

	function sub(ufp memory op1, ufp memory op2) public pure returns(ufp memory)
	{
		require(cmp(op1,op2) >= 0, "Math overflow : sub-01");
		uint256 	td = op1.D - op2.D;
		if (td > op1.D)
		{
			return ufp(op1.I - op2.I - 1 , td);
		}
		else
		{
			return ufp(op1.I - op2.I , td);
		}
	}
	
	function add(ufp memory op1, uint256 op2) public pure returns(ufp memory)
	{
		uint256 i = op1.I + op2;
		require(i >= op1.I, "Math overflow : add-00");
		return ufp(i , op1.D);
	}

	function add(ufp memory op1, ufp memory op2) public pure returns(ufp memory)
	{
		uint256 i = op1.I + op2.I;
		require(i >= op1.I, "Math overflow : add-01");

		uint256 d = op1.D + op2.D;
		if (d < op1.D)
		{
			i += 1;
			require(i > 0, "Maths overflow : add-02");
		}
		return ufp(i , d);
	}

	function mul(ufp memory op1, uint256 op2) public pure returns(ufp memory) // use double and add
	{
		uint256 				d = op2;
		uint256 				ti;
		uint256 				td;
		ufp memory 	m = op1;
		ufp memory 	r = ufp(0,0);

		while (d > 0)
		{
			if (d % 2 == 1)
			{
				r = add(r,m);
			}
			m = add(m,m);
			d = d/2;
		}
		return ufp(r.I , r.D);
	}

	function mul(ufp memory op1, ufp memory op2) public pure returns(ufp memory) // use previous mul()
	{
		uint256 		ad = op1.D;
		ufp memory 		aTruncted = ufp(0,ad);
		uint256 		bd = op2.D;
		ufp memory 		bTruncted = ufp(0,bd);
		uint256 		t = 0;
		ufp memory 		r = ufp(0,0);
		//////////////////////
		if (op1.I != 0 && op2.I != 0)
		{
			t = op1.I * op2.I;
			require(t/op1.I == op2.I , "Math overflow : mul-00");
			r = ufp(t,0);
		}
		//////////////////////
		r = add(r, mul(aTruncted,op2.I));
		//////////////////////
		r = add(r, mul(bTruncted,op1.I));
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
		t = 0;
		ad = 1;
		for (uint16 i = 256 ; i < 512 ; i++)
		{
			if (boolr[i] == true)
			{
				t += ad;
			}
			ad *=2;
		}
		r = add(r, ufp(0, t));
		//////////////////////
		return ufp(r.I , r.D);
	}

	function div(ufp memory op1, uint256 op2) public pure returns(ufp memory) // use native division and modulo
	{
		require(op2 > 0, "Math div by zero : div-00");
		if (op2 == 1)
		{
			return op1;
		}
		uint256 			i = 0;
		ufp memory 			r = op1;
		bool[256] memory 	boold;
		uint256 			d = 0;
		uint256 			t = 0;

		i = op1.I/op2;
		r = ufp(op1.I%op2,op1.D);

		for (uint16 j = 255 ; j > 0 ; j--)
		{
			r = mul(r,2);
			if (cmp(r,op2) >= 0)
			{
				r = sub(r,op2);
				boold[j] = true;
			}
		}

		t = 1;
		for (uint16 j = 0 ; j < 256 ; j++)
		{
			if (boold[j] == true)
			{
				d += t;
			}
			t *=2;
		}

		return ufp(i,d);
	}

	function div(ufp memory op1, ufp memory op2) public pure returns(ufp memory) // use incremental subtraction
	{
		require(cmp(op2,ufp(0,0)) > 0, "Math div by zero : div-01");
		if (cmp(op2,ufp(1,0)) == 0)
		{
			return op1;
		}

		uint256 			i = 0;
		ufp memory 			r = op1;
		bool[256] memory 	boold;
		uint256 			d = 0;
		uint256 			t = 0;

		while (cmp(r,op2) >= 0)
		{
			i += 1;
			r = sub(r,op2);
		}

		for (uint16 j = 255 ; j > 0 ; j--)
		{
			r = mul(r,2);
			if (cmp(r,op2) >= 0)
			{
				r = sub(r,op2);
				boold[j] = true;
			}
		}

		t = 1;
		for (uint16 j = 0 ; j < 256 ; j++)
		{
			if (boold[j] == true)
			{
				d += t;
			}
			t *=2;
		}
		return(ufp(i,d));
	}

	function exp(ufp memory op1, uint256 op2) public pure returns(ufp memory) // use square and multiply
	{
		uint256 		d = op2;
		uint256 		ti;
		uint256 		td;
		ufp memory 		m = op1;
		ufp memory 		r = ufp(1,0);

		while (d > 0)
		{
			if (d % 2 == 1)
			{
				r = mul(r,m);
			}
			m = mul(m,m);
			d = d/2;
		}
		return ufp(r.I , r.D);
	}
////////////////////////////////////////////////////////////////
}

