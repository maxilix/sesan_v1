pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;


contract fract
{

	struct fraction {
		uint256 						numerator;
		uint256 						divider;
	}

// FRACTION MANAGMENT

	function gcd(uint256 op1, uint256 op2) public pure returns (uint256)
	{
		uint256 	a = op1;
		uint256 	b = op2;
		uint256 	c = 1;
		while (c != 0)
		{
			c = a % b;
			a = b;
			b = c;
		}
		return a;
	}

	function lcm(uint256 op1, uint256 op2) public pure returns (uint256)
	{
		return op1*op2/gcd(op1,op2);
	}

	function add(fraction memory op1, fraction memory op2) public pure returns (uint256, uint256)
	{
		uint256 	n = op1.numerator * op2.divider + op2.numerator * op1.divider;
		uint256 	d = op1.divider * op2.divider;
		uint256 	g = gcd(n,d);
		return ( n/g , d/g );
	}

	function eval(fraction memory op) public  pure returns (uint256)
	{
		return (op.numerator/op.divider);
	}

	function mul(fraction memory op1, fraction memory op2) public pure returns (uint256, uint256)
	{
		uint256 	n = op1.numerator * op2.numerator;
		uint256 	d = op1.divider * op2.divider;
		if (n / op1.numerator != op2.numerator || d / op1.divider != op2.divider)
		{
			uint256 e1 = eval(op1);
			n = e1*op2.numerator;
			if (n / e1 != op2.numerator)
			{
				uint256 e2 = eval(op2);
				n = e1*e2;
				require(n/e1 == e2 , "multiplication overflow in mul");
				return(n, 1);
			}
			return(n, op2.divider);
		}
		uint256 g = gcd(n,d);
		return (n/g , d/g);
	}

	function exp1(fraction memory op, uint256 e) public pure returns(uint256 , uint256)
	{
		uint256 		d = e;
		uint256 		tn;
		uint256 		td;

		fraction memory m = op;
		fraction memory r = fraction(1,1);

		while (d > 0)
		{
			if (d % 2 == 1)
			{
				(tn,td) = mul(r,m);
				r = fraction(tn,td);
			}
			(tn,td) = mul(m,m);
			m = fraction(tn,td);
			d = d/2;
		}
		return ( r.numerator , r.divider );
	}


	function exp2(fraction memory op, uint256 e) public pure returns(uint256 , uint256)
	{
		uint256 		tn;
		uint256 		td;

		fraction memory r = fraction(1,1);
		uint256 		rMemory = 1;
		uint256 		rMemoryTemp;

		for (uint256 i = 0 ; i < e ; i++)
		{

			(tn,td) = mul(r,op);
			r = fraction(tn,td);
		}
		return (r.numerator , r.divider );
	}
	///////////////////////////
}